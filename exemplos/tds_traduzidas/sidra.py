import json
import logging
import pandas as pd
import sidrapy as IBGE
from time import sleep
from datetime import datetime
from unidecode import unidecode
from notion_client import Client as NotionClient

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class handlerIBGE():
    
    def __init__(self):
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
                "salmao": -1,
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


    def get_data(self, table_name:str, variable_name:str) ->pd.DataFrame:
        return IBGE.get_table(
            table_code = self.TABLE_ID[table_name],
            territorial_level='1',
            ibge_territorial_code='all',
            variable= self.VARIABLE_ID[table_name][variable_name],
            classification= '315/all',
            period=self._generate_period_string(),
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

    def set_variation_and_weight(self, index_name: str) ->pd.DataFrame:
        variacao = self.format_data(self.get_data(index_name,'VARIAÇÃO MENSAL'))
        peso = self.format_data(self.get_data(index_name,'PESO MENSAL'))
        df = self.merge_formatted_data(variacao,peso)
        df['index_name'] = index_name
        return df
    
    def set_granular_data(self) -> None:
        ipca = self.set_variation_and_weight('IPCA')
        ipca_15 = self.set_variation_and_weight('IPCA-15')
        self.granular_data = pd.concat([ipca,ipca_15],ignore_index=True, axis=0)
        self.granular_data = self.granular_data.groupby(['date', 'index_name']).apply(lambda x: x.drop_duplicates(subset='item_desc')).reset_index(drop=True)
        self.granular_data.to_csv('raw_ibge.csv',index=False)
        self.granular_data = pd.read_csv('raw_ibge.csv') #this is the funniest bug i have ever seen

    def _aux_calculate_filtered_df(self, composition_name:str) ->pd.DataFrame:
        current_composition = []
        for composition_item_name, composition_item_factor in self.COMPOSITIONS_BCB[composition_name].items():
            filtered_df = self.data[self.data.item_desc == composition_item_name].copy()
            filtered_df.item_variation *= composition_item_factor
            filtered_df.item_weight *= composition_item_factor
            current_composition.append(filtered_df)
        return pd.concat(
                    current_composition,
                    ignore_index=True,
                    axis=0
                )

    def calculate_bcb_compositions(self):
        self.data = self.granular_data.copy()
        for composition_name in self.COMPOSITIONS_BCB.keys():
            df = self._aux_calculate_filtered_df(composition_name)
            df = df.groupby(
                        [
                            'date',
                            'index_name'
                        ]
                    ).agg(
                            {
                                'item_variation': 'sum',
                                'item_weight': 'sum'
                            }
                        ).reset_index()
            df['item_desc'] = composition_name
            df['item_code'] = composition_name
            self.data = pd.concat(
                [
                    self.data, 
                    df
                ],
                ignore_index = True,
                axis = 0
            )
        self.data.to_csv('ibge.csv',index=False)

    def set_data(self):
        self.set_granular_data()
        self.calculate_bcb_compositions()

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

    def _set_all_databases(self) ->None:
        self.index_register = self.set_database('index_register') 
        self.group_register = self.set_database('group_register')
        self.composition_register = self.set_database('composition_register')
        self.index_history = self.set_database('index_history')

    def set_database(self, database_name:str) ->pd.DataFrame:
        database = self._notion_client.databases.query(self._secrets[database_name])
        table = []
        for row in database['results']:
            column_values = {}
            for column in self._database_columns[database_name]:
                column_values[column] = self._safe_get(row, f'properties.{column}.{self._database_map_json_path[self._database_column_type[column]]}') 
            table.append(column_values)
        return pd.DataFrame(table) 
        
    def insert(self,database_name:str, df:pd.DataFrame) ->None:
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
    
    def increase_reconnection_tries(self):
        self.reconnection_tries +=1

class HandlerUpdater():

    def __init__(self):
        self.ibge = handlerIBGE()
        #self.ibge.granular_data = pd.read_csv('raw_ibge.csv')
        self.database = HandlerDatabase()

    def index_register_is_valid(self):
        return len(self.ibge.data.index_name.unique()) == len(self.database.index_register)
    
    def group_register_is_valid(self):
        return len(self.ibge.data.item_desc.unique()) == len(self.database.group_register)

    def composition_register_is_valid(self):
        return self._count_items(self.ibge.COMPOSITIONS_BCB) == len(self.database.composition_register)

    def index_history_is_valid(self):
        return len(self.ibge.data) == len(self.database.index_history)

    def repair_index_register(self):
        #insert all on index_register
        pass
    
    def repair_group_register(self):
        #insert all on group_register
        pass

    def repair_composition_register(self):
        #insert all on composition_register
        pass

    def repair_index_history(self):
        #insert all on index_history
        pass

    def update_core(self):
        if self.database.has_connection():
            self.database._set_all_databases()
            self.ibge.set_data()
            if not self.index_register_is_valid():
                self.repair_index_register()
            if not self.group_register_is_valid():
                self.repair_group_register()
            if not self.composition_register_is_valid():
                self.repair_composition_register()
            if not self.index_history_is_valid():
                self.repair_index_history()
        else:
            if self.database.reconnection_tries > 5:
                logging.ERROR(f' [+] Could not connect to the database!')
                return
            self.database.increase_reconnection_tries()
            self.update_core()

    def _count_items(self,d):
        count = 0
        for key, value in d.items():
            if isinstance(value, dict):
                count += self._count_items(value) 
            else:
                count += 1 
        return count
    
up = HandlerUpdater()
up.update_core()

# se o db tem conexão
#   puxa os dados do ibge
#   se index_register invalido
#       atualiza index_register
#   se index_history invalido
#       atualiza index_history
#   se group_register invalido
#       atualiza group_register
#   se composition_regiser
#       atualiza composition_register
# senao
#   tenta novamente          

# acho que o dbHandler deve ter apenas essas poucas funções, o resto pode ficar no Handler Updater
# para deixar a tabela de decisao desse updater mais robusta, posso fazer com que ele cheque todas as datas em todas as execuções
# buscando por lacunas nas datas, por exemplo do index history
# buscando pela ausencia de grupos e aberturas em group_register
# buscando pela ausencia de itens em composition_register
# buscando pela ausencia de indices em index_register

# depois que o hanlder updater assegurar que que tudo está válido, então partimos para a analise
# vou replicar o dashboard:
# 12M, Metas BCB, 3M SAAR, 6M SAAR, MoM SAAR
# os gráficos podem ser feitos usando o matplot para facilitar. Não vou me ater a inserir essas séries na base

# assim que conseguir o resultado final, partimos para a replicação usando tabelas de decisão 
# usamos esse projeto como teste do code_inserter e code_generator
# teremos feito um exemplo bem robusto de aplicação de tabelas de decisão
# os outros exemplos podem ser mais bobinhos, então aí entra as trilhas do bcc fazendo chamadas recursivas de TDS
# e o primeiro exemplo pode ser o mais trivial, o teste de salário do Satoshi como referência
