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
        # Granularizar todos que contem "exceto"
        self.ABERTURAS_BCB = {
            "Livres": {
                "monitorados": -1
                },
            "Alimentos": {
                "Alimentação no domicílio": 1
                },
            "Alimentos in natura": {
                "Tubérculos, raízes e legumes": 1,
                "Hortaliças e verduras": 1,
                "Frutas": 1,
                "Ovo de galinha": 1
                }
            ,
            "Alimentos semi-elaborados": {
                "Cereais, leguminosas e oleaginosas": 1,
                "Carnes": 1,
                "Pescados": 1,
                "Frango inteiro": 1,
                "Frango em pedaços": 1,
                "Leite longa vida": 1
                }
            ,
            "Alimentos industrializados": {
                "Farinhas, féculas e massas": 1,
                "Açúcares e derivados": 1,
                "Carnes e peixes industrializados": 1,
                "Leite e derivados (exceto Leite longa vida)": 1,
                "Panificados": 1,
                "Óleos e gorduras": 1,
                "Bebidas e infusões": 1,
                "Enlatados e conservas": 1,
                "Sal e condimentos": 1}
            ,
            "Serviços": {
                "Alimentação fora do domicílio": 1,
                "Aluguel residencial": 1,
                "Condomínio": 1,
                "Mudança": 1,
                "Mão de obra (Reparos)": 1,
                "Consertos e manutenção": 1,
                "Passagem aérea": 1,
                "Transporte escolar": 1,
                "Transporte por aplicativo": 1,
                "Seguro voluntário de veículo": 1,
                "Conserto de automóvel": 1,
                "Estacionamento": 1,
                "Pintura de veículo": 1,
                "Aluguel de veículo": 1,
                "Serviços médicos e dentários": 1,
                "Serviços laboratoriais e hospitalares": 1,
                "Serviços pessoais (exceto Cartório e Conselho de classe)": 1,
                "Recreação (exceto Jogos de azar, Instrumento musical, Bicicleta, Alimento para animais, Brinquedo e Material de caça e pesca)": 1,
                "Cursos regulares": 1,
                "Cursos diversos": 1,
                "Plano de telefonia móvel": 1,
                "TV por assinatura": 1,
                "Acesso à internet": 1,
                "Serviços de streaming": 1,
                "Combo de telefonia, internet e TV por assinatura": 1
                }
            ,
            "Serviços Subjacente": {
                "Alimentação fora do domicílio": 1,
                "Aluguel residencial": 1,
                "Condomínio": 1,
                "Mudança": 1,
                "Consertos e manutenção": 1,
                "Transporte escolar": 1,
                "Seguro voluntário de veículo": 1,
                "Conserto de automóvel": 1,
                "Estacionamento": 1,
                "Pintura de veículo": 1,
                "Aluguel de veículo": 1,
                "Serviços médicos e dentários": 1,
                "Serviços laboratoriais e hospitalares": 1,
                "Costureira": 1,
                "Manicure": 1,
                "Cabeleireiro e barbeiro": 1,
                "Depilação": 1,
                "Despachante": 1,
                "Serviço bancário": 1,
                "Sobrancelha": 1,
                "Clube": 1,
                "Tratamento de animais (clínica)": 1,
                "Casa noturna": 1,
                "Serviço de higiene para animais": 1,
                "Cinema, teatro e concertos": 1
            }
            ,
            "Serviços Ex-Subjacente": {
                "Serviços Subjacente": -1
                },
            "Duráveis": {
                "Mobiliário": 1,
                "Artigos de iluminação": 1,
                "Tapete": 1,
                "Refrigerador": 1,
                "Ar-condicionado": 1,
                "Máquina de lavar roupa": 1,
                "Fogão": 1,
                "Chuveiro elétrico": 1,
                "Televisor": 1,
                "Aparelho de som": 1,
                "Computador pessoal": 1,
                "Joias e bijuterias": 1,
                "Automóvel novo": 1,
                "Automóvel usado": 1,
                "Motocicleta": 1,
                "Óculos de grau": 1,
                "Instrumento musical": 1,
                "Bicicleta": 1,
                "Aparelho telefônico": 1
                }
            ,
            "Semi-duráveis": {
                "Cortina": 1,
                "Utensílios de metal": 1,
                "Utensílios de vidro e louça": 1,
                "Utensílios de plástico": 1,
                "Utensílios para bebê": 1,
                "Cama, mesa e banho": 1,
                "Ventilador": 1,
                "Videogame (console)": 1,
                "Roupas": 1,
                "Calçados e acessórios": 1,
                "Tecidos e armarinhos": 1,
                "Acessorios e peças (Veículos)": 1,
                "Pneu": 1,
                "Brinquedo": 1,
                "Material de caça e pesca": 1,
                "Livro didático": 1,
                "Livro não didático": 1
                }
            ,
            "Não duráveis": {
                "Alimentação no domicílio": 1,
                "Reparos (habitação) exceto mão-de-obra": 1,
                "Artigos de limpeza": 1,
                "Carvão vegetal": 1,
                "Flores naturais": 1,
                "Óleo lubrificante": 1,
                "Etanol": 1,
                "Higiene pessoal": 1,
                "Alimento para animais": 1,
                "Cigarro": 1,
                "Jornal diário": 1,
                "Revista": 1,
                "Caderno": 1,
                "Artigos de papelaria": 1
                }
            ,
            "Monitorados": {
                "Taxa de água e esgoto": 1,
                "Gás de botijão": 1,
                "Gás encanado": 1,
                "Energia elétrica residencial": 1,
                "Ônibus urbano": 1,
                "Táxi": 1,
                "Trem": 1,
                "Ônibus intermunicipal": 1,
                "Ônibus interestadual": 1,
                "Metrô": 1,
                "Integração transporte público": 1,
                "Emplacamento e licença": 1,
                "Multa": 1,
                "Pedágio": 1,
                "Gasolina": 1,
                "Óleo diesel": 1,
                "Gás veicular": 1,
                "Produtos farmacêuticos": 1,
                "Plano de saúde": 1,
                "Cartório": 1,
                "Conselho de classe": 1,
                "Jogos de azar": 1,
                "Correio": 1,
                "Plano de telefonia fixa": 1
                }
            ,
            "Comercializáveis": {
                "Não comercializáveis": -1,
                "Monitorados": -1
                },
            "Não comercializáveis": {
                "Todos os tipos de feijão": 1,
                "Flocos de milho": 1,
                "Farinha de mandioca": 1,
                "Tubérculos, raízes e legumes": 1,
                "Hortaliças e verduras": 1,
                "Pescados (exceto salmão)": 1,
                "Leite e derivados (exceto leite em pó)": 1,
                "Pão francês": 1,
                "Pão doce": 1,
                "Bolo": 1,
                "Cimento (Reparos)": 1,
                "Tijolo": 1,
                "Areia": 1,
                "Carvão vegetal": 1,
                "Automóvel usado": 1,
                "Alimento para animais": 1,
                "Leitura": 1,
                "Serviços": 1
                },
            "Núcleo EX0": {
                "Alimentação no domicílio": -1,
                "Monitorados": -1
                },
            "Núcleo EX1": {
                "Cereais, leguminosas e oleaginosas": -1,
                "Tubérculos, raízes e legumes": -1,
                "Açúcares e derivados": -1,
                "Hortaliças e Verduras": -1,
                "Frutas": -1,
                "Carnes": -1,
                "Pescados": -1,
                "Aves e ovos": -1,
                "Leite e derivados": -1,
                "Óleos e gorduras": -1,
                "Combustíveis (domésticos)": -1,
                "Combustíveis (veículos)": -1}
            ,
            "Núcleo EX2": {
                "Cereais, leguminosas e oleaginosas": -1,
                "Farinhas, féculas e massas": -1,
                "Tubérculos, raízes e legumes": -1,
                "Açúcares e derivados": -1,
                "Hortaliças e Verduras": -1,
                "Frutas": -1,
                "Carnes": -1,
                "Pescados": -1,
                "Aves e ovos": -1,
                "Leite e derivados": -1,
                "Óleos e gorduras": -1,
                "Sal e condimentos": -1,
                "Aparelhos eletroeletrônicos": -1,
                "Automóvel novo": -1,
                "Automóvel usado": -1,
                "Etanol": -1,
                "Fumo": -1,
                "Serviços Ex-Subjacente": -1,
                "Monitorados": -1}
            ,
            "Núcleo EX3": {
                "Alimentação no domicílio": -1,
                "Aparelhos eletroeletrônicos": -1,
                "Automóvel novo": -1,
                "Automóvel usado": -1,
                "Etanol": -1,
                "Fumo": -1,
                "Serviços Ex-subjacente": -1,
                "Monitorados": -1}
            
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

db = HandlerDatabase()

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
