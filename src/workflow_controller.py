#1[
#1 TITULO: WORKFLOW CONTROLLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/08/2024
#1 VERSAO: 1
#1 FINALIDADE: FAZ AS CHAMADAS DE CLASSES DO GERADOR
#1 ENTRADAS: CAMINHO DO ARQUIVO E NOME DO NOVO ARQUIVO
#1 SAIDAS: ARQUIVO .PY COM CODIGO GERADO PELA LEITURA DE TDS
#1 ROTINAS CHAMADAS: READ_CODE, PROCESS_DECISION_TABLES, GENERATE_CODE, INSERT_CODE
#1]

from src.code_reader.code_reader import CodeReader
from src.decision_table.decision_table import DecisionTable
from src.code_generator.code_generator import CodeGenerator
from src.code_inserter.code_inserter import CodeInserter

class WorkflowController:

    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: DEFINE ATRIBUTOS
    #1 ENTRADAS: CAMINHO DO ARQUIVO E NOME DO NOVO ARQUIVO
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, file_path: str, file_name: str):
    #2 DEFINE CAMINHO DO ARQUIVO A SER LIDO
        self.file_path = file_path  
    #2 DEFINE NOME DO NOVO ARQUIVO A SER GERADO
        self.file_name = file_name  
    #2 INICIALIZA O LEITOR DE CODIGO
        self.code_reader = CodeReader(self.file_path)  
    #2 INICIALIZA LISTA DE TABELAS DE DECISAO ENCONTRADAS
        self.decision_tables_found = []  
    #2 INICIALIZA A LISTA DE TABELAS DE DECISAO PROCESSADAS
        self.processed_tables = []  
    #2 INICIALIZA O GERADOR DE CODIGO
        self.code_generator = CodeGenerator()
    #2 INICIALIZA A LISTA DE CODIGOS GERADOS
        self.generated_code = []
    #2 INICIALIZA O INSERIDOR DE CODIGO
        self.code_inserter = CodeInserter(self.file_path, self.file_name)
    #2]

    #1[
    #1 ROTINA: READ_CODE
    #1 FINALIDADE: LE O CODIGO E EXTRAI TABELAS DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: CODEREADER
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: CODEREADER.GET_EXTRACTED_DECISION_TABLES, CODEREADER.GET_EXTRACTED_DECISION_TABLES_POSITIONS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: read_code
    def read_code(self):
    #2 EXTRAI AS TABELAS DE DECISAO
        self.decision_tables_found = self.code_reader.get_extracted_decision_tables() 
    #2 EXTRAI POSICOES DAS TABELAS DE DECISAO
        self.position_of_decision_tables_found = self.code_reader.get_extracted_decision_tables_positions()
    #2]

    #1[
    #1 ROTINA: PROCESS_DECISION_TABLES
    #1 FINALIDADE: PROCESSA AS TABELAS DE DECISAO ENCONTRADAS
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: DECISIONTABLE
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: DECISIONTABLE.__INIT__
    #1]
    #2[
    #2 PSEUDOCODIGO DE: process_decision_tables
    def process_decision_tables(self):
    #2 INICIALIZA A LISTA DE TABELAS PROCESSADAS
        self.processed_tables = []
    #2 PERCORRE O CONJUNTO DE TABELAS DE DECISAO
        for index, table in enumerate(self.decision_tables_found):
    #2 PROCESSA CADA TABELA, ARMAZENANDO A TABELA PROCESSADA E A POSICAO ORIGINAL
            self.processed_tables.append(DecisionTable(table, self.position_of_decision_tables_found[index]))
    #2]

    #1[
    #1 ROTINA: GENERATE_CODE
    #1 FINALIDADE: GERA CODIGO A PARTIR DAS TABELAS DE DECISAO PROCESSADAS
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: CODEGENERATOR
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: CODEGENERATOR.GENERATE_CODE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: generate_code
    def generate_code(self):
    #2 PERCORRE O CONJUNTO DE TABELAS DE DECISAO PROCESSADAS
        for table in self.processed_tables:
    #2 GERA CODIGO PARA CADA TABELA PROCESSADA E O ARMAZENA
            self.generated_code.append(self.code_generator.generate_code(table))
    #2]

    #1[
    #1 ROTINA: INSERT_CODE
    #1 FINALIDADE: INSERE O CODIGO GERADO NO ARQUIVO ORIGINAL
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: CODEINSERTER
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: CODEINSERTER.INSERT
    #1]
    #2[
    #2 PSEUDOCODIGO DE: insert_code
    def insert_code(self):
    #2 CRIA UM DICIONARIO QUE MAPEIA AS POSICOES DAS TABELAS DE DECISAO E CODIGO GERADO
        decision_table_to_code_map = {k: v for k, v in zip([table.position_of_decision_table for table in self.processed_tables], self.generated_code)}
    #2 INSERE O CODIGO GERADO NO ARQUIVO ORIGINAL USANDO O MAPA CRIADO
        self.code_inserter.insert(decision_table_to_code_map)
    #2]

    #1[
    #1 ROTINA: EXECUTE
    #1 FINALIDADE: EXECUTA O FLUXO COMPLETO DE LEITURA, PROCESSAMENTO, GERACAO E INSERCAO DE CODIGO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: READ_CODE, PROCESS_DECISION_TABLES, GENERATE_CODE, INSERT_CODE
    #1 CHAMADO POR: N/A
    #1 CHAMA: READ_CODE, PROCESS_DECISION_TABLES, GENERATE_CODE, INSERT_CODE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: execute
    def execute(self):
    #2 LE O CODIGO E EXTRAI AS TABELAS DE DECISAO
        self.read_code()
    #2 PROCESSA AS TABELAS DE DECISAO ENCONTRADAS
        self.process_decision_tables()
    #2 GERA CODIGO A PARTIR DAS TABELAS PROCESSADAS
        self.generate_code()  
    #2 INSERE O CODIGO NO ARQUIVO INDICADO
        self.insert_code()
    #2]
