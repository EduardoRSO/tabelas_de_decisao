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
        secrets = open('sidra_notion_secrets.text','r').read().split('\n')
        self._notion_api_secret = secrets[0]
        self._notion_database_id = secrets[1]
        self._notion_client = NotionClient(auth=self._notion_api_secret)

    def has_connection(self) ->bool:
        print(self._notion_client.pages.retrieve(self._notion_database_id))

    def get_index_history(index_name:str):
        pass

    def insert(self):
        pass

    def is_updated(self):
        pass

    def has_index(self, index_name:str):
        pass

    def add_index(self, index_name:str):
        pass

    def retry_connection(self, repetition_counter:int):
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
db.has_connection()
#def analysis_core():
#    pass
