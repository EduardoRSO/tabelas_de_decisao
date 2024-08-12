#1[
#1 TITULO: WORKFLOW CONTROLLER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 12/08/2024
#1 VERSAO: 1
#1 FINALIDADE: FAZ AS CHAMADAS DE CLASSES DO GERADOR
#1 ENTRADAS: CAMINHO DO ARQUIVO E NOME DO NOVO ARQUIVO
#1 SAIDAS: ARQUIVO .PY COM CÓDIGO GERADO PELA LEITURA DE TDS
#1 ROTINAS CHAMADAS: read_code, process_decision_tables, generate_code, insert_code
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
        #2 INICIALIZA O GERADOR DE CÓDIGO
        self.code_generator = CodeGenerator()
        #2 INICIALIZA A LISTA DE CÓDIGOS GERADOS
        self.generated_code = []
        #2 INICIALIZA O INSERTOR DE CÓDIGO
        self.code_inserter = CodeInserter(self.file_path, self.file_name)
    #2]

    #1[
    #1 ROTINA: READ_CODE
    #1 FINALIDADE: LÊ O CÓDIGO E EXTRAI TABELAS DE DECISÃO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: CodeReader
    #1 CHAMADO POR: execute
    #1 CHAMA: CodeReader.get_extracted_decision_tables, CodeReader.get_extracted_decision_tables_positions
    #1]
    #2[
    #2 PSEUDOCODIGO DE: read_code
    def read_code(self):
        #2 EXTRAI AS TABELAS DE DECISÃO
        self.decision_tables_found = self.code_reader.get_extracted_decision_tables() 
        #2 EXTRAI POSICOES DAS TABELAS DE DECISÃO
        self.position_of_decision_tables_found = self.code_reader.get_extracted_decision_tables_positions()
    #2]

    #1[
    #1 ROTINA: PROCESS_DECISION_TABLES
    #1 FINALIDADE: PROCESSA AS TABELAS DE DECISÃO ENCONTRADAS
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: DecisionTable
    #1 CHAMADO POR: execute
    #1 CHAMA: DecisionTable.__init__
    #1]
    #2[
    #2 PSEUDOCÓDIGO DE: process_decision_tables
    def process_decision_tables(self):
        #2 INICIALIZA A LISTA DE TABELAS PROCESSADAS
        self.processed_tables = []
        #2 PERCORRE O CONJUNTO DE TABELAS DE DECISAO
        for index, table in enumerate(self.decision_tables_found):
            #2 PROCESSA CADA TABELA, ARMAZENADO A TABELA PROCESSADA E A POSIÇÃO ORIGINAL
            self.processed_tables.append(DecisionTable(table, self.position_of_decision_tables_found[index]))
    #2]

    #1[
    #1 ROTINA: GENERATE_CODE
    #1 FINALIDADE: GERA CÓDIGO A PARTIR DAS TABELAS DE DECISÃO PROCESSADAS
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: CodeGenerator
    #1 CHAMADO POR: execute
    #1 CHAMA: CodeGenerator.generate_code
    #1]
    #2[
    #2 PSEUDOCÓDIGO DE: generate_code
    def generate_code(self):
        #2 PERCORRE O CONJUNTO DE TABELAS DE DECISAO PROCESSADAS
        for table in self.processed_tables:
            #2 GERA CÓDIGO PARA CADA TABELA PROCESSADA E O ARMAZENA
            self.generated_code.append(self.code_generator.generate_code(table))

    #1[
    #1 ROTINA: INSERT_CODE
    #1 FINALIDADE: INSERE O CÓDIGO GERADO NO ARQUIVO ORIGINAL
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: CodeInserter
    #1 CHAMADO POR: execute
    #1 CHAMA: CodeInserter.insert
    #1]
    #2[
    #2 PSEUDOCÓDIGO DE: insert_code
    def insert_code(self):
        #2 CRIA UM DICIONÁRI OQUE MAPEIA AS POSIÇÕES DAS TABELAS DE DECISÃO E CÓDIGO GERADO
        #2 INVOCA O MÉTODO DE INSERÇÃO
        self.code_inserter.insert({k: v for k, v in zip([table.position_of_decision_table for table in self.processed_tables], self.generated_code)})
    #2]

    #1[
    #1 ROTINA: EXECUTE
    #1 FINALIDADE: EXECUTA O FLUXO COMPLETO DE LEITURA, PROCESSAMENTO, GERAÇÃO E INSERÇÃO DE CÓDIGO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: read_code, process_decision_tables, generate_code, insert_code
    #1 CHAMADO POR: N/A
    #1 CHAMA: read_code, process_decision_tables, generate_code, insert_code
    #1]
    #2[
    #2 PSEUDOCÓDIGO DE: execute
    def execute(self):
        #2 LÊ O CÓDIGO E EXTRAI AS TABELAS DE DECISÃO
        self.read_code()
        #2 PROCESSA AS TABELAS DE DECISÃO ENCONTRADAS
        self.process_decision_tables()
        #2 GERA CÓDIGO A PARTIR DAS TABELAS PROCESSADAS
        self.generate_code()  
        #2 INSERE O CÓDIGO NO ARQUIVO INDICADO
        self.insert_code()
    #2]
