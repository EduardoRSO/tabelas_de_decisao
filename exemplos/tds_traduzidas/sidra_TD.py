import json
import logging
import numpy as np
import pandas as pd
import sidrapy as IBGE
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from unidecode import unidecode
from notion_client import Client as NotionClient
from notion_client.helpers import is_full_database, collect_paginated_api

# Set up the logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HandlerIBGE():
    
    def __init__(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.__init__ with no parameters')
        self.INDEX_NAMES = ['IPCA', 'IPCA-15']
        self.TABLE_ID = {'IPCA': '7060','IPCA-15': '7062'}
        self.VARIABLE_ID = {'IPCA': {'VARIAÇÃO MENSAL': '63','PESO MENSAL': '66'},'IPCA-15': {'VARIAÇÃO MENSAL': '355','PESO MENSAL': '357'}}
        # Obtido em : https://www.bcb.gov.br/conteudo/relatorioinflacao/EstudosEspeciais/EE069_Atualizacoes_da_estrutura_de_ponderacao_do_IPCA_e_repercussao_nas_suas_classificacoes.pdf
        self.COMPOSITIONS_BCB = {
            "monitorados": {
                "taxa de agua e esgoto": 1,
                "gas de botijao": 1,
                "gas encanado": 1,
                "energia eletrica residencial": 1,
                "onibus urbano": 1,
                "taxi": 1,
                "trem": 1,
                "onibus intermunicipal": 1,
                "onibus interestadual": 1,
                "metro": 1,
                "integracao transporte publico": 1,
                "emplacamento e licenca": 1,
                "multa": 1,
                "pedagio": 1,
                "gasolina": 1,
                "oleo diesel": 1,
                "gas veicular": 1,
                "produtos farmaceuticos": 1,
                "plano de saude": 1,
                "cartorio": 1,
                "conselho de classe": 1,
                "jogos de azar": 1,
                "correio": 1,
                "plano de telefonia fixa": 1
            },
            "livres": { 
                "indice geral": 1,
                "monitorados": -1,
                },
            "alimentos": { "alimentacao no domicilio": 1 },
            "alimentos in natura": {
                "tuberculos, raizes e legumes": 1,
                "hortalicas e verduras": 1,
                "frutas": 1,
                "ovo de galinha": 1
            },
            "alimentos semi-elaborados": {
                "cereais, leguminosas e oleaginosas": 1,
                "carnes": 1,
                "pescados": 1,
                "frango inteiro": 1,
                "frango em pedacos": 1,
                "leite longa vida": 1
            },
            "alimentos industrializados": {
                "farinhas, feculas e massas": 1,
                "acucares e derivados": 1,
                "carnes e peixes industrializados": 1,
                "leites e derivados": 1,
                "leite longa vida": -1,
                "panificados": 1,
                "oleos e gorduras": 1,
                "bebidas e infusoes": 1,
                "enlatados e conservas": 1,
                "sal e condimentos": 1
            },
            "servicos": {
                "alimentacao fora do domicilio": 1,
                "aluguel residencial": 1,
                "condominio": 1,
                "mudanca": 1,
                "mao de obra": 1,
                "consertos e manutencao": 1,
                "passagem aerea": 1,
                "transporte escolar": 1,
                "transporte por aplicativo": 1,
                "seguro voluntario de veiculo": 1,
                "conserto de automovel": 1,
                "estacionamento": 1,
                "pintura de veiculo": 1,
                "aluguel de veiculo": 1,
                "servicos medicos e dentarios": 1,
                "servicos laboratoriais e hospitalares": 1,
                "servicos pessoais": 1,
                "cartorio" : -1,
                "conselho de classe" : -1,
                "recreacao" : 1, 
                "jogos de azar": -1, 
                "instrumento musical" : -1, 
                "bicicleta":-1, 
                "alimento para animais" :-1, 
                "brinquedo":-1, 
                "material de caca e pesca": -1,
                "cursos regulares": 1,
                "cursos diversos": 1,
                "plano de telefonia movel": 1,
                "tv por assinatura": 1,
                "acesso a internet": 1,
                "servicos de streaming": 1,
                "combo de telefonia, internet e tv por assinatura": 1
            },
            "servicos subjacente": {
                "alimentacao fora do domicilio": 1,
                "aluguel residencial": 1,
                "condominio": 1,
                "mudanca": 1,
                "consertos e manutencao": 1,
                "transporte escolar": 1,
                "seguro voluntario de veiculo": 1,
                "conserto de automovel": 1,
                "estacionamento": 1,
                "pintura de veiculo": 1,
                "aluguel de veiculo": 1,
                "servicos medicos e dentarios": 1,
                "servicos laboratoriais e hospitalares": 1,
                "costureira": 1,
                "manicure": 1,
                "cabeleireiro e barbeiro": 1,
                "depilacao": 1,
                "despachante": 1,
                "servico bancario": 1,
                "sobrancelha": 1,
                "clube": 1,
                "tratamento de animais (clinica)": 1,
                "casa noturna": 1,
                "servico de higiene para animais": 1,
                "cinema, teatro e concertos": 1
            },
            "servicos ex-subjacente": { "servicos":1,"servicos subjacente": -1 },
            "duraveis": {
                "mobiliario": 1,
                "artigos de iluminacao": 1,
                "tapete": 1,
                "refrigerador": 1,
                "ar-condicionado": 1,
                "maquina de lavar roupa": 1,
                "fogao": 1,
                "chuveiro eletrico": 1,
                "televisor": 1,
                "aparelho de som": 1,
                "computador pessoal": 1,
                "joias e bijuterias": 1,
                "automovel novo": 1,
                "automovel usado": 1,
                "motocicleta": 1,
                "oculos de grau": 1,
                "instrumento musical": 1,
                "bicicleta": 1,
                "aparelho telefonico": 1
            },
            "semi-duraveis": {
                "cortina": 1,
                "utensilios de metal": 1,
                "utensilios de vidro e louca": 1,
                "utensilios de plastico": 1,
                "utensilios para bebe": 1,
                "cama, mesa e banho": 1,
                "ventilador": 1,
                "videogame (console)": 1,
                "roupas": 1,
                "calcados e acessorios": 1,
                "tecidos e armarinho": 1,
                "acessorios e pecas": 1,
                "pneu": 1,
                "brinquedo": 1,
                "material de caca e pesca": 1,
                "livro didatico": 1,
                "livro nao didatico": 1
            },
            "nao duraveis": {
                "alimentacao no domicilio": 1,
                "reparos" : 1,
                "mao de obra": -1,
                "artigos de limpeza": 1,
                "carvao vegetal": 1,
                "flores naturais": 1,
                "oleo lubrificante": 1,
                "etanol": 1,
                "higiene pessoal": 1,
                "alimento para animais": 1,
                "cigarro": 1,
                "jornal diario": 1,
                "revista": 1,
                "caderno": 1,
                "artigos de papelaria": 1
            },
            "nao comercializaveis": {
                "feijao - mulatinho" : 1,
                "feijao - preto" : 1,
                "feijao - macacar (fradinho)" : 1,
                "feijao - carioca (rajado)" : 1,
                "flocos de milho": 1,
                "farinha de mandioca": 1,
                "tuberculos, raizes e legumes": 1,
                "hortalicas e verduras": 1,
                "pescados":1,
                "peixe - salmao": -1,
                "leites e derivados":1,
                "leite em po": -1,
                "pao frances": 1,
                "pao doce": 1,
                "bolo": 1,
                "cimento": 1,
                "tijolo": 1,
                "areia": 1,
                "carvao vegetal": 1,
                "automovel usado": 1,
                "alimento para animais": 1,
                "leitura": 1,
                "servicos": 1
            },
            "comercializaveis": { "indice geral": 1, "nao comercializaveis": -1, "monitorados": -1 },
            "nucleo ex0": { "indice geral":1,"alimentacao no domicilio": -1, "monitorados": -1 },
            "nucleo ex1": {
                "cereais, leguminosas e oleaginosas": -1,
                "tuberculos, raizes e legumes": -1,
                "acucares e derivados": -1,
                "hortalicas e verduras": -1,
                "frutas": -1,
                "carnes": -1,
                "pescados": -1,
                "aves e ovos": -1,
                "leites e derivados": -1,
                "oleos e gorduras": -1,
                "combustiveis (domesticos)": -1,
                "combustiveis (veiculos)": -1
            },
            "nucleo ex2": {
                "cereais, leguminosas e oleaginosas": -1,
                "farinhas, feculas e massas": -1,
                "tuberculos, raizes e legumes": -1,
                "acucares e derivados": -1,
                "hortalicas e verduras": -1,
                "frutas": -1,
                "carnes": -1,
                "pescados": -1,
                "aves e ovos": -1,
                "leites e derivados": -1,
                "oleos e gorduras": -1,
                "sal e condimentos": -1,
                "aparelhos eletroeletronicos": -1,
                "automovel novo": -1,
                "automovel usado": -1,
                "etanol": -1,
                "fumo": -1,
                "servicos ex-subjacente": -1,
                "monitorados": -1
            },
            "nucleo ex3": {
                "indice geral": 1,
                "alimentacao no domicilio": -1,
                "aparelhos eletroeletronicos": -1,
                "automovel novo": -1,
                "automovel usado": -1,
                "etanol": -1,
                "fumo": -1,
                "servicos ex-subjacente": -1,
                "monitorados": -1
            }
            }

    def _generate_period_string(self):
        logger.info(f' [+] Executing {self.__class__.__name__}._generate_period_string with no parameters')
        current_date = datetime.now()
        end_year = current_date.year
        end_month = current_date.month
        
        date_list = []
        year = 2020
        month = 1
        
        while (year < end_year) or (year == end_year and month <= end_month):
            date_list.append(f"{year:04d}{month:02d}")
            month += 1
            if month > 12:
                month = 1
                year += 1
        
        return ','.join(date_list)

    def get_data(self, table_name: str, variable_name: str) -> pd.DataFrame:
        logger.info(f' [+] Executing {self.__class__.__name__}.get_data with parameters: table_name={table_name}, variable_name={variable_name}')
        return IBGE.get_table(
            table_code=self.TABLE_ID[table_name],
            territorial_level='1',
            ibge_territorial_code='all',
            variable=self.VARIABLE_ID[table_name][variable_name],
            classification='315/all',
            period=self._generate_period_string(),
            header='n',
            format='pandas'
        )

    def format_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info(f' [+] Executing {self.__class__.__name__}.format_data with DataFrame shape {df.shape}')
        df.drop(columns=['MN', 'NC', 'NN', 'MC', 'D1C', 'D1N', 'D2N', 'D3C', 'D3N', 'D4C'], inplace=True)
        df.rename(columns={'V': 'value', 'D2C': 'date', 'D4N': 'item'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'], format='%Y%m')
        df['item_code'] = df['item'].apply(lambda x: str(x).split('.')[0] if len(str(x).split('.')) > 1 else 0)
        df['item_desc'] = df['item'].apply(lambda x: unidecode(str(x).split('.')[1].lower()) if len(str(x).split('.')) > 1 else unidecode(str(x).lower()))
        df.drop(columns='item', inplace=True)
        return df

    def merge_formatted_data(self, variation: pd.DataFrame, weight: pd.DataFrame) -> pd.DataFrame:
        logger.info(f' [+] Executing {self.__class__.__name__}.merge_formatted_data with DataFrames variation shape {variation.shape} and weight shape {weight.shape}')
        variation.rename(columns={'value': 'item_variation'}, inplace=True)
        weight.rename(columns={'value': 'item_weight'}, inplace=True)
        df = pd.merge(variation, weight, how='inner', on=['date', 'item_code', 'item_desc'])
        return df[['date', 'item_code', 'item_desc', 'item_variation', 'item_weight']]

    def set_variation_and_weight(self, index_name: str) -> pd.DataFrame:
        logger.info(f' [+] Executing {self.__class__.__name__}.set_variation_and_weight with parameter: index_name={index_name}')
        variacao = self.format_data(self.get_data(index_name, 'VARIAÇÃO MENSAL'))
        peso = self.format_data(self.get_data(index_name, 'PESO MENSAL'))
        df = self.merge_formatted_data(variacao, peso)
        df['index_name'] = index_name
        return df

    def set_granular_data(self) -> None:
        logger.info(f' [+] Executing {self.__class__.__name__}.set_granular_data with no parameters')
        ipca = self.set_variation_and_weight('IPCA')
        ipca_15 = self.set_variation_and_weight('IPCA-15')
        self.granular_data = pd.concat([ipca, ipca_15], ignore_index=True, axis=0)
        self.granular_data = self.granular_data.groupby(['date', 'index_name']).apply(lambda x: x.drop_duplicates(subset='item_desc')).reset_index(drop=True)
        self.granular_data.to_csv('raw_ibge.csv', index=False)
        self.granular_data = pd.read_csv('raw_ibge.csv')  # this is the funniest bug i have ever seen

    def _aux_calculate_filtered_df(self, composition_name: str) -> pd.DataFrame:
        logger.info(f' [+] Executing {self.__class__.__name__}._aux_calculate_filtered_df with parameter: composition_name={composition_name}')
        current_composition = []
        for composition_item_name, composition_item_factor in self.COMPOSITIONS_BCB[composition_name].items():
            filtered_df = self.data[self.data.item_desc == composition_item_name].copy()
            filtered_df.item_variation *= composition_item_factor
            filtered_df.item_weight *= composition_item_factor
            current_composition.append(filtered_df)
        return pd.concat(current_composition, ignore_index=True, axis=0)

    def calculate_bcb_compositions(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.calculate_bcb_compositions with no parameters')
        self.data = self.granular_data.copy()
        for composition_name in self.COMPOSITIONS_BCB.keys():
            df = self._aux_calculate_filtered_df(composition_name)
            df = df.groupby(['date', 'index_name']).agg({'item_variation': 'sum', 'item_weight': 'sum'}).reset_index()
            df['item_desc'] = composition_name
            df['item_code'] = composition_name
            self.data = pd.concat([self.data, df], ignore_index=True, axis=0)
        self.data.to_csv('ibge.csv', index=False)

    def set_data(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.set_data with no parameters')
        self.set_granular_data()
        self.calculate_bcb_compositions()

class HandlerDatabase:
    def __init__(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.__init__ with no parameters')
        self._secrets = json.load(open('sidra_notion_secrets.json', 'r'))
        self._notion_client = NotionClient(auth=self._secrets['api_secret'])
        self._database_columns = {
            'index_register': ['id_index', 'index_name'],
            'group_register': ['id_group', 'id_parentGroup', 'group_name', 'group_desc'],
            'composition_register': ['id_group', 'id_child', 'factor'],
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
            'date': 'text',
            'item_value': 'number',
            'item_weight': 'number'
        }
        self._database_map_json_path = {
            'number': 'number',
            'text': 'rich_text.0.text.content'
        }
        self._request_counter = 0
        self.loaded_databases = False


    def _check_request_limit(self):
        self._request_counter+=1
        if self._request_counter % 3 == 0:
            sleep(2)

    def has_connection(self) -> bool:
        logger.info(f' [+] Executing {self.__class__.__name__}.has_connection with no parameters')
        try:
            for secret_name, database_id in self._secrets.items():
                if secret_name != 'api_secret':
                    self._check_request_limit()
                    self._notion_client.databases.retrieve(database_id)
            return True
        except Exception as e:
            logger.error(f' [+] Error in {self.__class__.__name__}.has_connection: {e}')
            return False

    def _set_all_databases(self) -> None:
        logger.info(f' [+] Executing {self.__class__.__name__}._set_all_databases with no parameters')
        self.index_register = self.set_database('index_register')
        self.group_register = self.set_database('group_register')
        self.composition_register = self.set_database('composition_register')
        self.index_history = self.set_database('index_history')
        self._name_to_db = {
            'index_register': self.index_register,
            'group_register': self.group_register,
            'composition_register': self.composition_register,
            'index_history': self.index_history
        }
        self.loaded_databases = True

    def set_database(self, database_name: str) -> pd.DataFrame:
        logger.info(f' [+] Executing {self.__class__.__name__}.set_database with parameters: database_name={database_name}')
        self._check_request_limit()
        database = collect_paginated_api(self._notion_client.databases.query, database_id=self._secrets[database_name])
        table = []
        for row in database:
            column_values = {}
            for column in self._database_columns[database_name]:
                column_values[column] = self._safe_get(row, f'properties.{column}.{self._database_map_json_path[self._database_column_type[column]]}')
            table.append(column_values)
        return pd.DataFrame(table).drop_duplicates()

    def insert(self, database_name: str, df: pd.DataFrame) -> None:
        logger.info(f' [+] Executing {self.__class__.__name__}.insert with parameters: database_name={database_name}, df=DataFrame with shape {df.shape}')
        df = self._get_unique_rows(database_name, df, self._name_to_db[database_name])
        for _, row in df.iterrows():
            properties = {}
            for column in self._database_columns[database_name]:
                properties[column] = self._safe_set(self._database_map_json_path[self._database_column_type[column]], row[column])
            logger.info(f' [+] Inserted row on database_name={database_name}, df=DataFrame with shape {df.shape}, row = {row.to_dict()}, properties = {properties}')
            self._check_request_limit()
            self._notion_client.pages.create(
                **{
                    "parent": {
                        'database_id': self._secrets[database_name]
                    },
                    "properties": properties
                }
            ) 
        self.loaded_databases = False  
    
    def increase_reconnection_tries(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.increase_reconnection_tries with no parameters')
        self.reconnection_tries += 1
        
    def _safe_get(self, data: dict, dot_chained_keys: str):
        logger.info(f' [+] Executing {self.__class__.__name__}._safe_get with parameters: data=dict, dot_chained_keys={dot_chained_keys}')
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

    def _safe_set(self, dot_chained_keys: str, value):
        logger.info(f' [+] Executing {self.__class__.__name__}._safe_set with parameters: dot_chained_keys={dot_chained_keys}, value={value}')
        keys = dot_chained_keys.split('.')
        obj = int(value) if isinstance(value, np.integer) else value
        for key in keys[::-1]:
            if key.isdigit():
                obj = [obj]
            else:
                obj = {key: obj}
        return obj
    
    def _get_unique_rows(self, database_name:str, df1:pd.DataFrame, df2:pd.DataFrame) ->pd.DataFrame:
        merged_df = df1.merge(df2, on=self._database_columns[database_name], how='left', indicator=True)
        unique_df1 = merged_df[merged_df['_merge'] == 'left_only'].drop(columns='_merge')
        logger.info(f' [+] Executed {self.__class__.__name__}.insert with parameters: database_name={database_name}, df=DataFrame with shape{df1.shape}. Returned= {unique_df1.shape}')
        return unique_df1

class HandlerUpdater():
    def __init__(self, ibge = None, database = None):
        logger.info(f' [+] Executing {self.__class__.__name__}.__init__ with no parameters')
        self.ibge = HandlerIBGE() if ibge == None else ibge
        self.database = HandlerDatabase() if database == None else database 
        
    def index_register_is_valid(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.index_register_is_valid with no parameters')
        logger.info(f'      [+] Executing {len(self.ibge.data.index_name.unique())} e {len(self.database.index_register)}')
        return len(self.ibge.data.index_name.unique()) <= len(self.database.index_register)
    
    def group_register_is_valid(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.group_register_is_valid with no parameters')
        logger.info(f'      [+] Executing {len(self.ibge.data.item_desc.unique())} e {len(self.database.group_register)}')
        return len(self.ibge.data.item_desc.unique()) <= len(self.database.group_register)

    def composition_register_is_valid(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.composition_register_is_valid with no parameters')
        logger.info(f'      [+] Executing {self._count_items(self.ibge.COMPOSITIONS_BCB)} e {len(self.database.composition_register)}')
        return self._count_items(self.ibge.COMPOSITIONS_BCB) <= len(self.database.composition_register)

    def index_history_is_valid(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.index_history_is_valid with no parameters')
        logger.info(f'      [+] Executing {len(self.ibge.data[self.ibge.data.item_code.isin(list(self.ibge.COMPOSITIONS_BCB.keys())+[0])])} e {len(self.database.index_history)}')
        return len(self.ibge.data[self.ibge.data.item_code.isin(list(self.ibge.COMPOSITIONS_BCB.keys())+[0])]) <= len(self.database.index_history)

    def repair_index_register(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.repair_index_register with no parameters')
        self.template_index_register = pd.DataFrame(columns=['id_index', 'index_name'])
        for index_name in self.ibge.data.index_name.unique():
            self.template_index_register.loc[len(self.template_index_register)] = {'id_index': self.id_mapping_index_register[index_name] , 'index_name': index_name}
        self.database.insert('index_register', self.template_index_register)

    def repair_group_register(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.repair_group_register with no parameters')
        self.template_group_register = pd.DataFrame(columns=['id_group', 'id_parentGroup', 'group_name', 'group_desc'])
        for _, row in self.ibge.data[(self.ibge.data.date == self.ibge.data.date.max()) & (self.ibge.data.index_name == 'IPCA')].iterrows():
            self.template_group_register.loc[len(self.template_group_register)] = {
                'id_group': self.id_mapping_group_register[str(row['item_code'])],
                'id_parentGroup': self._get_parentGroup(row['item_code']),
                'group_name': str(row['item_code']),
                'group_desc': str(row['item_desc'])
            }
        self.database.insert('group_register', self.template_group_register)

    def repair_composition_register(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.repair_composition_register with no parameters')
        self.template_composition_register = pd.DataFrame(columns = ['id_group', 'id_child', 'factor'],dtype=int)
        for composition_name in self.ibge.COMPOSITIONS_BCB.keys():
            for composition_item, composition_factor in self.ibge.COMPOSITIONS_BCB[composition_name].items():
                self.template_composition_register.loc[len(self.template_composition_register)] = {
                    'id_group': self.id_mapping_group_register[composition_name],
                    'id_child': self.id_mapping_group_register[self._get_itemCode_by_itemDesc(composition_item)],
                    'factor': composition_factor
                }
        self.database.insert('composition_register', self.template_composition_register)
        
    def repair_index_history(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.repair_index_history with no parameters')
        self.template_index_history = pd.DataFrame(columns=['id_index','id_group','date','item_value','item_weight'])
        filtered_ipca_item_history = self.ibge.data[self.ibge.data.item_code.isin(list(self.ibge.COMPOSITIONS_BCB.keys())+[0])]
        for _, row in filtered_ipca_item_history.iterrows():
            self.template_index_history.loc[len(self.template_index_history)] = {
                'id_index' : self.id_mapping_index_register[str(row['index_name'])],
                'id_group' : self.id_mapping_group_register[str(row['item_code'])],
                'date': row['date'].strftime('%Y-%m-%d'),
                'item_value': row['item_variation'],
                'item_weight': row['item_weight']
            }
        self.database.insert('index_history', self.template_index_history)
        
    def update_core(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.update_core with no parameters')
        print('> Updating the database...')
        self.ibge.set_data()
        self.ibge.data.date = pd.to_datetime(self.ibge.data.date, format='%Y-%m-%d') 
        self._create_id_mapping_itemCode()
        self._create_id_mapping_indexName()

        if self.database.has_connection():
            if not self.database.loaded_databases:
                self.database._set_all_databases()
            if not self.index_register_is_valid():
                self.repair_index_register()
            if not self.group_register_is_valid():
                self.repair_group_register()
            if not self.composition_register_is_valid():
                self.repair_composition_register()
            if not self.index_history_is_valid():
                self.repair_index_history()
            print('> Database update completed successfully.')
        else:
            if self.database.reconnection_tries > 5:
                logger.error(f' [+] Could not connect to the database!')
                return
            self.database.increase_reconnection_tries()
            self.update_core()

    def _count_items(self, d):
        logger.info(f' [+] Executing {self.__class__.__name__}._count_items with len(parameters): {len(d)}')
        count = 0
        for key, value in d.items():
            if isinstance(value, dict):
                count += self._count_items(value) 
            else:
                count += 1 
        return count
    
    def _create_id_mapping_indexName(self) ->None:
        self.id_mapping_index_register = {
            'IPCA':1,
            'IPCA-15':2
        }
    def _create_id_mapping_itemCode(self) ->None:
        logger.info(f' [+] Executing {self.__class__.__name__}._create_id_mapping with no parameters')
        self.id_mapping_group_register = {}
        for _, row in self.ibge.data[self.ibge.data.date == self.ibge.data.date.max()].iterrows():
            self.id_mapping_group_register[str(row['item_code'])] = self.id_mapping_group_register.get(str(row['item_code']),len(self.id_mapping_group_register)+1)

    def _get_parentGroup(self, item_code):
        logger.info(f' [+] Executing {self.__class__.__name__}._get_parentGroup with no parameters = {item_code}')
        item_code = str(item_code)
        if item_code.isdigit():
            if len(item_code) == 1:
                return self.id_mapping_group_register['0']
            elif len(item_code) == 2:
                return self.id_mapping_group_register[item_code[0]]
            elif len(item_code) == 4:
                if self.id_mapping_group_register.get(item_code[0:2]) == None:
                    return self._get_parentGroup(item_code[0:2])
                return self.id_mapping_group_register[item_code[0:2]]
            elif len(item_code) == 7:
                if self.id_mapping_group_register.get(item_code[0:4]) == None:
                    return self._get_parentGroup(item_code[0:4])
                return self.id_mapping_group_register[item_code[0:4]]
        return self.id_mapping_group_register['0']
    
    def _get_itemCode_by_itemDesc(self, item_desc) ->str:
        logger.info(f' [+] Executing {self.__class__.__name__}._get_itemCode_by_itemDesc with no parameters = {item_desc}')
        return self.ibge.data[self.ibge.data.item_desc == item_desc]['item_code'].iloc[0]        

class HandlerAnalysis:
    def __init__(self, database=None):
        self.database = HandlerDatabase() if database is None else database
        self.choosed_options = []

    def contribution_graph(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.contribution_graph with no parameters')
        for index_name in self.analysis_df.index_name.unique():
            logger.info(f'      [+] Generating contribution graph for index_name={index_name}')
            filtered_data = self.analysis_df[
                (self.analysis_df['id_group'].isin(self.choosed_options)) &
                (self.analysis_df['index_name'] == index_name)
            ].copy()

            filtered_data['contribution'] = filtered_data['item_value']/100 * filtered_data['item_weight']
            filtered_data['x_axis'] = filtered_data.index.strftime('%y-%b')
            pivot_data = filtered_data.pivot_table(
                index='x_axis', 
                columns='group_desc', 
                values='contribution', 
                aggfunc='sum'
            )
            ax = pivot_data.plot(kind='bar', stacked=True, figsize=(12, 8))
            ax.set_title(f'Contribution by Date ({index_name})')
            ax.set_xlabel('Date')
            ax.set_ylabel('Contribution')
            ax.legend(title='Items selected')

            plt.xticks(rotation=90)

            filename = f'{index_name}_contribution_graph.png'
            plt.savefig(filename)
            logger.info(f"      [+] Graph saved as '{filename}'")
            plt.clf()

    def variation_graph(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.variation_graph with no parameters')
        for index_name in self.analysis_df.index_name.unique():
            for id in self.choosed_options:
                logger.info(f'      [+] Generating variation graph for id={id}')
                filtered_data = self.analysis_df[
                    (self.analysis_df['id_group'] == id) &
                    (self.analysis_df['index_name'] == index_name)
                ].copy()
                filtered_data['date'] = pd.to_datetime(filtered_data.index)
                filtered_data['yoy'] = (filtered_data['item_value'] / 100 + 1).rolling(window=12).apply(lambda x: np.prod(x) - 1) * 100
                fig, ax1 = plt.subplots(figsize=(12, 8))
                bars = ax1.bar(filtered_data.index, filtered_data['item_value'], color='lightgray', width=20, label='MoM (%)')
                ax1.set_xlabel('Date')
                ax1.set_ylabel('MoM (%)')
                ax1.legend(loc='upper left')
                ax1.plot(filtered_data.index, filtered_data['yoy'], color='blue', label='YoY Variation', marker='o', linestyle='-')
                ax1.set_ylabel('MoM / YoY (%)')
                ax1.legend(loc='upper right')
                plt.title(f'MoM and YoY Variation ({index_name} - {filtered_data["group_desc"].iloc[0]})')
                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b-%y'))
                plt.xticks(rotation=90)
                filename = f'{index_name}_{filtered_data["group_desc"].iloc[0]}_variation_graph.png'
                plt.savefig(filename)
                logger.info(f"Graph saved as '{filename}'")
                plt.clf()

    def set_available_options(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.set_available_options with no parameters')
        merged_df = pd.merge(self.database.group_register, self.database.index_history, on='id_group', how='inner')
        unique_options = merged_df[['group_desc', 'id_group']].drop_duplicates().reset_index()
        self.available_options = []
        for index, row in unique_options.iterrows():
            self.available_options.append([chr(index+60), row['group_desc'], str(row['id_group'])])
        logger.info(f'      [+] Available options set')

    def set_choosed_options(self):
        ids = input('> Enter the char id, item name or item id of the items for the contribution graph, separated by commas:\n> ')
        logger.info(f' [+] Executing {self.__class__.__name__}.set_choosed_options with ids={ids}')
        self.choosed_options = []
        for option in [id.strip() for id in ids.split(',')]:
            found_option = False
            for row in self.available_options:
                if option in row:
                    self.choosed_options.append(int(row[2]))
                    found_option = True
                    break
            if not found_option:
                logger.error(f' [+] Error in {self.__class__.__name__}.set_choosed_options. Option {option} not found')

    def set_analysis_df(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.set_analysis_df with no parameters')
        self.analysis_df = pd.merge(self.database.index_history, self.database.index_register, on='id_index', how='inner')
        self.analysis_df = self.analysis_df.merge(self.database.group_register, on='id_group')
        self.analysis_df.date = pd.to_datetime(self.analysis_df.date, format='%Y-%m-%d')
        self.analysis_df = self.analysis_df.set_index('date')
        self.analysis_df = self.analysis_df.sort_index()
        logger.info(f'      [+] Analysis DataFrame set')

    def show_available_options(self):
        print('> Available options:')
        for option in self.available_options:
            print(f'  - {option[0]}: {option[1]}({option[2]})')

    def show_visualization_core_exit_message(self):
        print('> Exiting visualization. Returning to main menu.')

    def show_invalid_option_message(self, graph_option):
        print(f' [-] Error: Unrecognized option "{graph_option}". Please enter a valid option (1, 2, 3, or 4).')

    def show_sucess_message(self):
        print('> Data analysis and visualization completed successfully.')

    def visualization_core(self):
        logger.info(f' [+] Executing {self.__class__.__name__}.visualization_core with no parameters')
        print('> Initializing data analysis and visualization...')
        if not self.database.loaded_databases:
            self.database._set_all_databases()
        #self.database.composition_register = pd.read_csv('composition_register.csv')
        #self.database.group_register = pd.read_csv('group_register.csv')
        #self.database.index_register = pd.read_csv('index_register.csv')
        #self.database.index_history = pd.read_csv('index_history.csv')
        #self.database.index_history.date = pd.to_datetime(self.database.index_history.date, format='%Y-%m-%d')
        self.set_available_options()
        self.set_analysis_df()
        
        while True:
            graph_option = int(input('> Please choose a graph to plot:\n'
                                 '  1 - Contribution Graph (stacked bar graph by date)\n'
                                 '  2 - Variation Graph (line graph with bar graph behind)\n'
                                 '  3 - Show available options\n'
                                 '  4 - Exit visualization\n> '))
            #TD decision table td_analysis
            #TD sets
            #TD        1                                                {1}
            #TD        2                                                {2}
            #TD        3                                                {3}
            #TD        4                                                {4}
            #TD conditions
            #TD        option                                           1   2   3   4
            #TD actions
            #TD        self.set_choosed_options()                       1   0   0   0                                            
            #TD        self.contribution_graph()                        2   0   0   0                        
            #TD        self.variation_graph()                           0   0   0   0                        
            #TD        self.show_available_options()                    0   1   0   0                        
            #TD        self.show_visualization_core_exit_message()      0   0   1   1                        
            #TD        self.show_invalid_option_message(graph_option)   0   0   0   0                        
            #TD        self.show_success_message()                      3   0   0   0                        
            #TD end table

            if graph_option == "1":
                self.set_choosed_options()
                self.contribution_graph()
            elif graph_option == "2":
                self.set_choosed_options()
                self.variation_graph() 
            elif graph_option == "3":
                self.show_available_options()
            elif graph_option == "4":
                self.show_visualization_core_exit_message()
                break
            else:
                print(f' [-] Error: Unrecognized option "{graph_option}". Please enter a valid option (1, 2, 3, or 4).')
        
 

def quit_program():
    print('> Exiting the program. Goodbye!')
    exit()

def invalid_option(option):
    print(f' [-] Error: Unrecognized option "{option}". Please enter a valid option (1, 2, or 3).')


if __name__ == '__main__':
    print(f'> SIDRA.py is a program connected to a Notion database that can plot graphs of data collected from the IPCA (Índice Nacional de Preços ao Consumidor Amplo) by IBGE.\n'
          f'  It is recommended to update the database before performing any analysis.')
    ibge = HandlerIBGE()
    database = HandlerDatabase()
    updater = HandlerUpdater(ibge,database)
    analysis = HandlerAnalysis(database)
    while True:
        option = int(input('> Please choose an option:\n'
                       '  1 - Update the database\n'
                       '  2 - Perform data analysis and plot graphs\n'
                       '  3 - Quit the program\n> '))
        #TD decision table td_main
        #TD sets
        #          opcao_valida                     {1,2,3,12,13,123}
        #          atualiza                         {1}
        #          analisa                          {2}
        #          sai                              {3}
        #          atualiza_analisa                 {12}
        #          atualiza_sai                     {13}
        #          atualiza_analisa_sai             {123}
        #TD conditions
        #TD        option                           opcao_valida  opcao_valida opcao_valida opcao_valida        opcao_valida opcao_valida 
        #TD        option                           atualiza      analisa      sai          atualiza_analisa    atualiza_sai atualiza_analisa_sai
        #TD actions
        #TD        analysis.visualization_core()    0             1            0            2                   0            2
        #TD        updater.update_core()            1             0            0            1                   1            1  
        #TD        quit_program()                   0             0            1            0                   2            3
        #TD end table
            