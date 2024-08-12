#1[
#1 TITULO: CODE INSERTER
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 12/08/2024
#1 VERSAO: 1
#1 FINALIDADE: INSERIR CÓDIGO EM UM ARQUIVO EM POSIÇÕES ESPECÍFICAS
#1 ENTRADAS: CAMINHO DO ARQUIVO, NOME DO ARQUIVO, MAPA DE POSIÇÕES DE CÓDIGO
#1 SAIDAS: ARQUIVO MODIFICADO COM O CÓDIGO INSERIDO
#1 ROTINAS CHAMADAS: SET_DEFAULT_SPACING, SET_FILE_PATH, SET_FILE_NAME, SET_FILE_STRING, SET_NEW_FILE_PATH, SET_CODE_SPACING, INSERT
#1]
import os

class CodeInserter:

    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA A CLASSE E DEFINE OS ATRIBUTOS INICIAIS
    #1 ENTRADAS: CAMINHO DO ARQUIVO E NOME DO NOVO ARQUIVO
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: SET_DEFAULT_SPACING, SET_FILE_PATH, SET_FILE_NAME, SET_FILE_STRING, SET_NEW_FILE_PATH
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, file_path: str, file_name: str):
        #2 DEFINE O ESPAÇAMENTO PADRÃO COMO 4 ESPAÇOS
        self.set_default_spacing(" " * 4)
        #2 DEFINE O CAMINHO DO ARQUIVO
        self.set_file_path(file_path)
        #2 DEFINE O NOME DO ARQUIVO
        self.set_file_name(file_name)  
        #2 LÊ O CONTEÚDO DO ARQUIVO E ARMAZENA EM SELF.FILE_STRING
        self.set_file_string()  
        #2 DEFINE O NOVO CAMINHO DO ARQUIVO
        self.set_new_file_path()  
    #2]

    #1[
    #1 ROTINA: SET_DEFAULT_SPACING
    #1 FINALIDADE: DEFINE O ESPAÇAMENTO PADRÃO PARA O CÓDIGO INSERIDO
    #1 ENTRADAS: ESPAÇAMENTO PADRÃO (STRING)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE:
    def set_default_spacing(self, default_spacing: str):
        #2 ARMAZENA O ESPAÇAMENTO ESPAÇAMENTO
        self.default_spacing = default_spacing  
    #2]

    #1[
    #1 ROTINA: SET_FILE_PATH
    #1 FINALIDADE: DEFINE O CAMINHO DO ARQUIVO A SER MODIFICADO
    #1 ENTRADAS: CAMINHO DO ARQUIVO (STRING)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_file_path
    def set_file_path(self, file_path: str):
        #2 ARMAZENA O CAMINHO DO ARQUIVO
        self.file_path = file_path  
    #2]

    #1[
    #1 ROTINA: SET_FILE_NAME
    #1 FINALIDADE: DEFINE O NOME DO ARQUIVO A SER GERADO OU MODIFICADO
    #1 ENTRADAS: NOME DO ARQUIVO (STRING)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_file_name
    def set_file_name(self, file_name: str):
        #2 ARMAZENA O NOME DO ARQUIVO
        self.file_name = file_name  
    #2]

    #1[
    #1 ROTINA: SET_FILE_STRING
    #1 FINALIDADE: LÊ O CONTEÚDO DO ARQUIVO E ARMAZENA EM UMA LISTA DE LINHAS
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_file_string
    def set_file_string(self):
        with open(self.file_path, 'r') as file:
            #2 LÊ TODAS AS LINHAS DO ARQUIVO
            self.file_string = file.readlines()  
    #2]

    #1[
    #1 ROTINA: SET_NEW_FILE_PATH
    #1 FINALIDADE: DEFINE O NOVO CAMINHO DO ARQUIVO COM O NOME ATUALIZADO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: OS, PATH
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_new_file_path
    def set_new_file_path(self):
        #2 CONSTRÓI O NOVO CAMINHO DO ARQUIVO
        self.new_file_path = os.path.join(os.path.dirname(self.file_path), self.file_name)  
    #2]

    #1[
    #1 ROTINA: SET_CODE_SPACING
    #1 FINALIDADE: AJUSTA O ESPAÇAMENTO DO CÓDIGO INSERIDO COM BASE NA COLUNA INICIAL
    #1 ENTRADAS: CÓDIGO A SER INSERIDO (STRING), COLUNA INICIAL (INT)
    #1 DEPENDENCIAS: RE
    #1 CHAMADO POR: INSERT
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_code_spacing
    def set_code_spacing(self, code, column):
        #2 SUBSTITUI O ESPAÇAMENTO INICIAL PELO NÚMERO DE ESPAÇOS CORRESPONDENTES À COLUNA
        code = code.replace('<INITIAL_SPACING>', ' ' * column)  
        #2 SUBSTITUI O ESPAÇAMENTO PADRÃO NO CÓDIGO
        code = code.replace('<DEFAULT_SPACING>', self.default_spacing)  
        #2 RETORNA O CÓDIGO COM ESPAÇAMENTO AJUSTADO
        return code  
    #2]

    #1[
    #1 ROTINA: INSERT
    #1 FINALIDADE: INSERE O CÓDIGO GERADO NAS POSIÇÕES ESPECÍFICAS DO ARQUIVO
    #1 ENTRADAS: MAPA DE POSIÇÕES DE CÓDIGO (DICT)
    #1 DEPENDENCIAS: OS, SET_CODE_SPACING, SET_NEW_FILE_PATH
    #1 CHAMADO POR: EXTERNAL
    #1 CHAMA: SET_CODE_SPACING
    #1]
    #2[
    #2 PSEUDOCODIGO DE: insert
    def insert(self, dt_position_to_code_map: dict):
        #2 PERCORRE OS ELEMENTOS DO CONJUNTO DE POSIÇÕES E CÓDIGO GERADO
        for (start, end), generated_code in dt_position_to_code_map.items():
            #2 DESESTRUTURA A LINHA E COLUNA DE INÍCIO
            start_line, start_column = start  
            #2 DESESTRUTURA A LINHA E COLUNA DE FIM
            end_line, end_column = end  

            #2 REMOVE O CONTEÚDO ENTRE AS LINHAS DE INÍCIO E FIM
            for row in range(start_line, end_line):
                self.file_string[row] = ''

            #2 INSERE O CÓDIGO GERADO NA POSIÇÃO CORRETA
            new_line = self.set_code_spacing(generated_code, start[1])
            self.file_string[start_line] = new_line

        #2 SALVA O CONTEÚDO MODIFICADO NO NOVO ARQUIVO
        with open(self.new_file_path, 'w') as file:
            file.writelines(self.file_string)
    #2]