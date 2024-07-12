import json
import logging
import pandas as pd
import sidrapy as IBGE
from time import sleep
from unidecode import unidecode
from notion_client import Client as NotionClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class handlerIBGE():
    
    def __init__(self):
        self.INDEX_NAMES = ['IPCA', 'IPCA-15']
        self.TABLE_ID = {'IPCA': '7060','IPCA-15': '7062'}
        self.VARIABLE_ID = {'IPCA': {'VARIAÇÃO MENSAL': '63','PESO MENSAL': '66'},'IPCA-15': {'VARIAÇÃO MENSAL': '355','PESO MENSAL': '357'}}

    def get_data(self, table_name:str, variable_name:str, date:str) ->pd.DataFrame:
        return IBGE.get_table(
            table_code = self.TABLE_ID[table_name],
            territorial_level='1',
            ibge_territorial_code='all',
            variable= self.VARIABLE_ID[table_name][variable_name],
            classification= '315/all',
            period=date,
            header='n',
            format='pandas'
        )

    def format_data(self, df:pd.DataFrame) ->pd.DataFrame:
        df.drop(columns=['MN','NC', 'NN', 'MC','D1C', 'D1N', 'D2N', 'D3C', 'D3N', 'D4C'],inplace=True)
        df.rename(columns={'V':'value', 'D2C': 'date', 'D4N': 'item'}, inplace= True)
        df['date'] = pd.to_datetime(df['date'],format='%Y%m')
        df['item_code'] = df['item'].apply(lambda x: str(x).split('.')[0] if len(str(x).split('.')) > 1 else 0 ) 
        df['item_desc'] = df['item'].apply(lambda x: unidecode(str(x).split('.')[1].lower()) if len(str(x).split('.')) > 1 else unidecode(str(x).lower()))
        df.drop(columns='item',inplace=True)
        return df

    def merge_formatted_data(self, variation: pd.DataFrame, weight: pd.DataFrame) ->pd.DataFrame:
        variation.rename(columns={'value': 'item_variation'}, inplace=True)
        weight.rename(columns={'value': 'item_weight'}, inplace=True)
        df = pd.merge(variation, weight, how='inner',on=['date','item_code','item_desc'])
        return df[['date','item_code', 'item_desc','item_variation','item_weight']]

    def set_variation_and_weight(self, index_name: str, period:str) ->pd.DataFrame:
        df1 = self.format_data(self.get_data(index_name,'VARIAÇÃO MENSAL', period))
        df2 = self.format_data(self.get_data(index_name,'PESO MENSAL', period))
        return self.merge_formatted_data(df1,df2)

class HandlerDatabase():

    def __init__(self):
        self._secrets = json.load(open('sidra_notion_secrets.json','r'))
        self._notion_client = NotionClient(auth=self._secrets['api_secret'])
        self._database_columns = {
            'index_register': ['id_index', 'index_name'],
            'group_register': ['id_group', 'id_parentGroup', 'group_name', 'group_desc'],
            'composition_register': ['id_group','id_child','factor'],
            'index_history': ['id_index', 'id_group', 'date', 'item_value', 'item_weight']
        }
        self._database_column_type = {
            'id_index': 'number',
            'index_name': 'text',
            'id_group': 'number',
            'id_parentGroup': 'number',
            'group_name': 'text',
            'group_desc': 'text',
            'id_child': 'number',
            'factor': 'number',
            'date' : 'text',
            'item_value' : 'number',
            'item_weight' : 'text'
        }
        self._database_map_json_path = {
            'number' : 'number',
            'text': 'rich_text.0.text.content'
        }


    def has_connection(self) ->bool:
        try:
            for secret_name, database_id in self._secrets.items():
                if secret_name != 'api_secret':
                    self._notion_client.databases.retrieve(database_id)
            return True
        except Exception as e:
            print(e)
            return False

    def get_database(self, database_name:str):
        database = self._notion_client.databases.query(self._secrets[database_name])
        table = []
        for row in database['results']:
            column_values = {}
            for column in self._database_columns[database_name]:
                column_values[column] = self._safe_get(row, f'properties.{column}.{self._database_map_json_path[self._database_column_type[column]]}') 
            table.append(column_values)
        return pd.DataFrame(table) 
        
    def insert(self,database_name:str, df:pd.DataFrame):
        for _, row in df.iterrows():
            properties = {}
            for column in self._database_columns[database_name]:
                properties[column] = self._safe_set(self._database_map_json_path[self._database_column_type[column]],row[column])
            self._notion_client.pages.create(
                **{
                    "parent": {
                        'database_id': self._secrets[database_name]
                    },
                    "properties": properties
                }
            )

    def is_updated(self):
        pass

    def has_index(self, index_name:str):
        pass

    def add_index(self, index_name:str):
        pass

    def _safe_get(self, data:dict, dot_chained_keys:str):
        keys = dot_chained_keys.split('.')
        for key in keys:
            try:
                if isinstance(data, list):
                    data = data[int(key)]
                else:
                    data = data[key]
            except (KeyError, TypeError, IndexError):
                return None
        return data
    
    def _safe_set(self, dot_chained_keys:str, value):
        keys = dot_chained_keys.split('.')
        obj = value
        for key in keys[::-1]:
            if key.isdigit():
                obj = [obj]
            else:
                obj = {key: obj}
        return obj
    
    def retry_connection(self):
        self.reconnection_tries +=1

class HandlerUpdater():

    def __init__(self):
        self.ibge = handlerIBGE()
        self.database = HandlerDatabase()

    def set_max_date(self, df:pd.DataFrame):
        self.current_max_date = df['date'].max()

    def set_index_history(self, index_name:str):
        self.current_index_history = self.database.get_index_history(index_name)
        
    def set_variation_and_weight(self,index_name:str):
        self.variation_and_weight = pd.DataFrame([])

    def update_core(self):
        for index_name in self.ibge.INDEX_NAMES:
            if self.database.has_connection():
                if self.database.has_index(index_name):
                    self.set_index_history(index_name)
                    if self.database.is_updated():
                        continue
                    else:
                        self.set_max_date()
                        self.set_variation_and_weight()
                        self.database.insert(self.variation_and_weight)
                else:
                    self.database.add_index(index_name)
                    self.update_core()
            else:
                if self.database.reconnection_tries > 5:
                    logging.ERROR(f' [+] Could not connect to the database!')
                    return
                self.database.retry_connection()
                self.update_core()


db = HandlerDatabase()

#print(db.get_database('index_register'))

#def analysis_core():
#    pass
