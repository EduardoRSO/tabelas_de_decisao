#1[
#1 TITULO: code_reader.py
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 26/07/2024
#1 VERSAO: 1
#1 FINALIDADE: Ler e processar código Python, verificando a validade do caminho do arquivo, lendo o código e extraindo tabelas de decisão.
#1 ENTRADAS: Caminho para o arquivo de código Python.
#1 SAIDAS: Código Python como string e listas de tabelas de decisão extraídas.
#1 ROTINAS CHAMADAS: 
#1     - __init__
#1     - __str__
#1     - set_path_code
#1     - set_code
#1     - set_extracted_decision_tables
#1     - get_path_code
#1     - get_code
#1     - get_extracted_decision_tables
#1     - _is_valid_path
#1     - _is_valid_code
#1     - _find_decision_tables
#1]

import os 
import re

class CodeReader:

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: Inicializar a instância da classe CodeReader e configurar os atributos.
    #1 ENTRADAS: path_code (str)
    #1 DEPENDENCIAS: os, re
    #1 CHAMADO POR: N/A
    #1 CHAMA: set_path_code, set_code, set_extracted_decision_tables
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, path_code:str) ->None:
    #2  Configura o caminho do código
        self.set_path_code(path_code)
    #2  Configura o código
        self.set_code()
    #2  Configura as tabelas de decisão extraídas
        self.set_extracted_decision_tables()
    #2]

    #1[
    #1 ROTINA: __str__
    #1 FINALIDADE: Fornecer uma representação em string do objeto CodeReader.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: get_path_code, get_code, get_extracted_decision_tables
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __str__
    def __str__(self) -> str:
    #2  Retorna uma string representativa do estado atual do objeto
        return f' [+] CodeReader:\n     path_code: {self.get_path_code()}\n     len(code): {len(self.get_code())}\n     len(extracted_decision_tables): {len(self.get_extracted_decision_tables())}'
    #2]

    #1[
    #1 ROTINA: set_path_code
    #1 FINALIDADE: Definir o atributo path_code após validar o caminho fornecido.
    #1 ENTRADAS: path_code (str)
    #1 DEPENDENCIAS: os
    #1 CHAMADO POR: __init__
    #1 CHAMA: _is_valid_path
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_path_code
    def set_path_code(self, path_code:str) ->None:
    #2  Define o caminho do código após validação
        self.path_code = self._is_valid_path(path_code)
    #2]

    #1[
    #1 ROTINA: set_code
    #1 FINALIDADE: Definir o atributo code após verificar a validade do conteúdo do arquivo.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: os
    #1 CHAMADO POR: __init__
    #1 CHAMA: _is_valid_code
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_code
    def set_code(self) ->None:
    #2  Define o código lido do arquivo após validação
        self.code = self._is_valid_code()
    #2]

    #1[
    #1 ROTINA: set_extracted_decision_tables
    #1 FINALIDADE: Definir o atributo extracted_decision_tables com as tabelas de decisão encontradas no código.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: re
    #1 CHAMADO POR: __init__
    #1 CHAMA: _find_decision_tables
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_extracted_decision_tables
    def set_extracted_decision_tables(self) ->None:
    #2  Define as tabelas de decisão extraídas do código
        self.extracted_decision_tables = self._find_decision_tables()
    #2]

    #1[
    #1 ROTINA: get_path_code
    #1 FINALIDADE: Retornar o valor do atributo path_code.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_path_code
    def get_path_code(self) ->str:
    #2  Retorna o caminho do código
        return self.path_code
    #2]

    #1[
    #1 ROTINA: get_code
    #1 FINALIDADE: Retornar o valor do atributo code.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_code
    def get_code(self) ->str:
    #2  Retorna o código lido do arquivo
        return self.code
    #2]

    #1[
    #1 ROTINA: get_extracted_decision_tables
    #1 FINALIDADE: Retornar o valor do atributo extracted_decision_tables.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_extracted_decision_tables
    def get_extracted_decision_tables(self) -> list:
    #2  Retorna as tabelas de decisão extraídas
        return self.extracted_decision_tables
    #2]

    #1[
    #1 ROTINA: _is_valid_path
    #1 FINALIDADE: Verificar se o caminho fornecido é um arquivo Python válido.
    #1 ENTRADAS: path_code (str)
    #1 DEPENDENCIAS: os
    #1 CHAMADO POR: set_path_code
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_path
    def _is_valid_path(self, path_code:str) ->str:
    #2  Verifica se o caminho do arquivo é válido e retorna o caminho
        if not os.path.isfile(path_code):
            raise FileNotFoundError(f" [-] O path passado {path_code} não é um arquivo.")
        if not path_code.endswith('.py'):
            raise ValueError(f" [-] O path do arquivo passado {path_code} não é um arquivo python") 
        return path_code
    #2]

    #1[
    #1 ROTINA: _is_valid_code
    #1 FINALIDADE: Verificar se o conteúdo do arquivo não está vazio.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: os
    #1 CHAMADO POR: set_code
    #1 CHAMA: get_path_code
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_code
    def _is_valid_code(self) ->str:
    #2  Verifica se o arquivo não está vazio e retorna seu conteúdo
        with open(self.get_path_code(),'r') as file:
            content = file.read().strip()
            if len(content) == 0:
                raise ValueError(f' [-] O arquivo passado {self.get_path_code()} está vazio')
            return content
    #2]

    #1[
    #1 ROTINA: _find_decision_tables
    #1 FINALIDADE: Encontrar e retornar as tabelas de decisão no código.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: re
    #1 CHAMADO POR: set_extracted_decision_tables
    #1 CHAMA: get_code
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _find_decision_tables
    def _find_decision_tables(self) ->list:
    #2  Busca e retorna as tabelas de decisão encontradas no código
        decisions_table_found = re.findall(r'(#TD decision table.*?#TD end table)',self.get_code(), re.DOTALL)
        if len(decisions_table_found) == 0:
            raise ValueError(f' [-] O arquivo não possui nenhuma tabela de decisão')
        return decisions_table_found
    #2]
