import json
import logging
import datetime
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
        # Obtido em : https://www.bcb.gov.br/conteudo/relatorioinflacao/EstudosEspeciais/EE069_Atualizacoes_da_estrutura_de_ponderacao_do_IPCA_e_repercussao_nas_suas_classificacoes.pdf
        self.COMPOSITIONS_BCB = {
            "livres": { "monitorados": -1 },
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
                "leite e derivados": 1,
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
                "mao de obra (reparos)": 1,
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
            "servicos ex-subjacente": { "servicos subjacente": -1 },
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
                "tecidos e armarinhos": 1,
                "acessorios e pecas (veiculos)": 1,
                "pneu": 1,
                "brinquedo": 1,
                "material de caca e pesca": 1,
                "livro didatico": 1,
                "livro nao didatico": 1
            },
            "nao duraveis": {
                "alimentacao no domicilio": 1,
                "reparos" : 1,
                "mao-de-obra": -1,
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
            "comercializaveis": { "nao comercializaveis": -1, "monitorados": -1 },
            "nao comercializaveis": {
                "todos os tipos de feijao": 1,
                "flocos de milho": 1,
                "farinha de mandioca": 1,
                "tuberculos, raizes e legumes": 1,
                "hortalicas e verduras": 1,
                "pescados":1,
                "salmao)": -1,
                "leite e derivados":1,
                "leite em po)": -1,
                "pao frances": 1,
                "pao doce": 1,
                "bolo": 1,
                "cimento (reparos)": 1,
                "tijolo": 1,
                "areia": 1,
                "carvao vegetal": 1,
                "automovel usado": 1,
                "alimento para animais": 1,
                "leitura": 1,
                "servicos": 1
            },
            "nucleo ex0": { "alimentacao no domicilio": -1, "monitorados": -1 },
            "nucleo ex1": {
                "cereais, leguminosas e oleaginosas": -1,
                "tuberculos, raizes e legumes": -1,
                "acucares e derivados": -1,
                "hortalicas e verduras": -1,
                "frutas": -1,
                "carnes": -1,
                "pescados": -1,
                "aves e ovos": -1,
                "leite e derivados": -1,
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
                "leite e derivados": -1,
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
        self.granular_data = self.merge_formatted_data(df1,df2)

    def calculate_bcb_compositions(self):
        for composition_name, composition_items in self.COMPOSITIONS_BCB.items():
            for composition_item_name, composition_item_factor in composition_items.items():
                if composition_item_name not in self.granular_data.item_desc.to_list():
                    print(f' [-] {composition_name} {composition_item_name} {composition_item_factor}')

ibge = handlerIBGE()    
ibge.granular_data = pd.read_csv('ibge.csv')
#print(ibge.granular_data)
#exit()
ibge.calculate_bcb_compositions()

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
        self.composition_register = self.set_database('composition_register ')
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
        self.database = HandlerDatabase()

    def set_max_date(self, df:pd.DataFrame):
        self.current_max_date = df['date'].max()

    def set_index_history(self, index_name:str):
        self.current_index_history = self.database.get_index_history(index_name)
        
    def set_variation_and_weight(self,index_name:str):
        self.variation_and_weight = pd.DataFrame([])

    def is_updated(self, date: datetime) ->bool:
        return self.index_history.date.max() <= date

    def has_index(self, index_name:str):
        return index_name in self.index_register.index_name.to_list()
    
    def add_index(self, index_name:str) -> None:
        pass

    def add_index_history(self):
        pass

    def add_group(self):
        pass

    def add_composition(self):
        pass

    def update_core(self):
        for index_name in self.ibge.INDEX_NAMES:
            if self.database.has_connection():
                self.set_ibge_data()
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

# antes de continuar desenvolvendo o core updater.
# vou fazer com que o HandlerIBGE calcule as aberturas <variação e peso>
# assim o handlerUpdater apenas irá copiar o dataframe gerado pelo handlerIBGE e fazer as reparações necessárias

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
