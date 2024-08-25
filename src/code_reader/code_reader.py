#1[
#1 TITULO: CODE_READER.PY
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/08/2024
#1 VERSAO: 1
#1 FINALIDADE: LER UM ARQUIVO PYTHON E EXTRAIR TABELAS DE DECISAO
#1 ENTRADAS: CAMINHO DO ARQUIVO (STRING)
#1 SAIDAS: TABELAS DE DECISAO EXTRAIDAS E SUAS POSICOES
#1 ROTINAS CHAMADAS: SET_PATH_CODE, SET_CODE, SET_EXTRACTED_DECISION_TABLES, _IS_VALID_PATH, _IS_VALID_CODE, _FIND_DECISION_TABLES, _GET_LINE_COL_FROM_POS_END, _GET_LINE_COL_FROM_POS_START
#1]

import os
import re  

class CodeReader:

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: INICIALIZAR A CLASSE E DEFINIR OS ATRIBUTOS INICIAIS
    #1 ENTRADAS: CAMINHO DO ARQUIVO (STR)
    #1 DEPENDENCIAS: SET_PATH_CODE, SET_CODE, SET_EXTRACTED_DECISION_TABLES
    #1 CHAMADO POR: EXTERNO
    #1 CHAMA: SET_PATH_CODE, SET_CODE, SET_EXTRACTED_DECISION_TABLES
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, path_code: str) -> None:
    #2  DEFINE O CAMINHO DO ARQUIVO
        self.set_path_code(path_code)
    #2  LE E ARMAZENA O CODIGO DO ARQUIVO
        self.set_code()
    #2  EXTRAI E ARMAZENA AS TABELAS DE DECISAO
        self.set_extracted_decision_tables()
    #2]

    #1[
    #1 ROTINA: __str__
    #1 FINALIDADE: RETORNAR UMA REPRESENTACAO STRING DO OBJETO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: GET_PATH_CODE, GET_CODE, GET_EXTRACTED_DECISION_TABLES
    #1 CHAMADO POR: EXTERNO
    #1 CHAMA: GET_PATH_CODE, GET_CODE, GET_EXTRACTED_DECISION_TABLES
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __str__
    def __str__(self) -> str:
    #2  RETORNA UMA REPRESENTACAO STRING DO OBJETO CODEREADER
        return (f' [+] CodeReader:\n'
                f'     path_code: {self.get_path_code()}\n'
                f'     len(code): {len(self.get_code())}\n'
                f'     len(extracted_decision_tables): {len(self.get_extracted_decision_tables())}')
    #2]

    #1[
    #1 ROTINA: SET_PATH_CODE
    #1 FINALIDADE: VALIDAR E DEFINIR O CAMINHO DO ARQUIVO
    #1 ENTRADAS: CAMINHO DO ARQUIVO (STR)
    #1 DEPENDENCIAS: _IS_VALID_PATH
    #1 CHAMADO POR: __init__
    #1 CHAMA: _IS_VALID_PATH
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_path_code
    def set_path_code(self, path_code: str) -> None:
    #2  VALIDA E ARMAZENA O CAMINHO DO ARQUIVO
        self.path_code = self._is_valid_path(path_code)
    #2]

    #1[
    #1 ROTINA: SET_CODE
    #1 FINALIDADE: LER O CODIGO DO ARQUIVO E ARMAZENAR
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: _IS_VALID_CODE
    #1 CHAMADO POR: __init__
    #1 CHAMA: _IS_VALID_CODE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_code
    def set_code(self) -> None:
    #2  LE O CODIGO DO ARQUIVO E ARMAZENA EM SELF.CODE
        self.code = self._is_valid_code()
    #2]

    #1[
    #1 ROTINA: SET_EXTRACTED_DECISION_TABLES
    #1 FINALIDADE: EXTRAR E ARMAZENAR AS TABELAS DE DECISAO E SUAS POSICOES
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: _FIND_DECISION_TABLES
    #1 CHAMADO POR: __init__
    #1 CHAMA: _FIND_DECISION_TABLES
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_extracted_decision_tables
    def set_extracted_decision_tables(self) -> None:
    #2  EXTRAI AS TABELAS DE DECISAO E SUAS POSICOES
        self.extracted_decision_tables, self.positions = self._find_decision_tables()
    #2]

    #1[
    #1 ROTINA: GET_PATH_CODE
    #1 FINALIDADE: RETORNAR O CAMINHO DO ARQUIVO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_path_code
    def get_path_code(self) -> str:
    #2  RETORNA O CAMINHO DO ARQUIVO
        return self.path_code
    #2]

    #1[
    #1 ROTINA: GET_CODE
    #1 FINALIDADE: RETORNAR O CODIGO LIDO DO ARQUIVO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_code
    def get_code(self) -> str:
    #2  RETORNA O CODIGO DO ARQUIVO
        return self.code
    #2]

    #1[
    #1 ROTINA: GET_EXTRACTED_DECISION_TABLES_POSITIONS
    #1 FINALIDADE: RETORNAR AS POSICOES DAS TABELAS DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: EXTERNO
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_extracted_decision_tables_positions
    def get_extracted_decision_tables_positions(self) -> list:
    #2  RETORNA AS POSICOES DAS TABELAS DE DECISAO
        return self.positions
    #2]

    #1[
    #1 ROTINA: GET_EXTRACTED_DECISION_TABLES
    #1 FINALIDADE: RETORNAR AS TABELAS DE DECISAO EXTRAIDAS
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: EXTERNO
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_extracted_decision_tables
    def get_extracted_decision_tables(self) -> list:
    #2  RETORNA AS TABELAS DE DECISAO EXTRAIDAS
        return self.extracted_decision_tables
    #2]

    #1[
    #1 ROTINA: GET_POSITIONS
    #1 FINALIDADE: RETORNAR AS POSICOES DAS TABELAS DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: EXTERNO
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_positions
    def get_positions(self) -> list:
    #2  RETORNA AS POSICOES DAS TABELAS DE DECISAO
        return self.positions
    #2]

    #1[
    #1 ROTINA: _IS_VALID_PATH
    #1 FINALIDADE: VALIDAR O CAMINHO DO ARQUIVO
    #1 ENTRADAS: CAMINHO DO ARQUIVO (STR)
    #1 DEPENDENCIAS: OS
    #1 CHAMADO POR: SET_PATH_CODE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_path
    def _is_valid_path(self, path_code: str) -> str:
    #2  VERIFICA SE O CAMINHO FORNECIDO E UM ARQUIVO VALIDO
        if not os.path.isfile(path_code):
            raise FileNotFoundError(f" [-] O PATH PASSADO {path_code} NAO E UM ARQUIVO.")
        
    #2  VERIFICA SE O ARQUIVO TEM EXTENSAO .PY
        if not path_code.endswith('.py'):
            raise ValueError(f" [-] O PATH DO ARQUIVO PASSADO {path_code} NAO E UM ARQUIVO PYTHON")
        
    #2  RETORNA O CAMINHO DO ARQUIVO SE FOR VALIDO
        return path_code
    #2]

    #1[
    #1 ROTINA: _IS_VALID_CODE
    #1 FINALIDADE: VALIDAR O CONTEUDO DO ARQUIVO DE CODIGO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: SET_CODE
    #1 CHAMA: GET_PATH_CODE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_code
    def _is_valid_code(self) -> str:
    #2  ABRE O ARQUIVO E LE O CONTEUDO
        with open(self.get_path_code(), 'r') as file:
            content = file.read().strip()
        
    #2  VERIFICA SE O CONTEUDO DO ARQUIVO NAO ESTA VAZIO
        if len(content) == 0:
            raise ValueError(f' [-] O ARQUIVO PASSADO {self.get_path_code()} ESTA VAZIO')
        
    #2  RETORNA O CONTEUDO DO ARQUIVO SE NAO ESTIVER VAZIO
        return content
    #2]

    #1[
    #1 ROTINA: _FIND_DECISION_TABLES
    #1 FINALIDADE: ENCONTRAR TABELAS DE DECISAO NO CODIGO E SUAS POSICOES
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: RE
    #1 CHAMADO POR: SET_EXTRACTED_DECISION_TABLES
    #1 CHAMA: GET_CODE, _GET_LINE_COL_FROM_POS_END, _GET_LINE_COL_FROM_POS_START
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _find_decision_tables
    def _find_decision_tables(self) -> tuple:
    #2  INICIALIZA UMA LISTA PARA ARMAZENAR AS TABELAS DE DECISAO ENCONTRADAS
        decisions_table_found = []
    #2  INICIALIZA UMA LISTA PARA ARMAZENAR AS POSICOES DAS TABELAS DE DECISAO
        positions = []
    #2  DEFINE UM PADRAO REGEX PARA ENCONTRAR TABELAS DE DECISAO
        pattern = re.compile(r'(#TD decision table.*?#TD end table)', re.DOTALL)

    #2  PROCURA POR OCORRENCIAS DO PADRAO REGEX NO CODIGO
        for match in pattern.finditer(self.get_code()):
    #2      OBTEM A POSICAO DE INICIO DA TABELA DE DECISAO
            start = match.start()
    #2      OBTEM A POSICAO DE FIM DA TABELA DE DECISAO
            end = match.end()
            
    #2      OBTEM A LINHA E COLUNA DA POSICAO DE FIM DA TABELA
            end_line, end_column = self._get_line_col_from_pos_end(end)
            
    #2      OBTEM A LINHA E COLUNA DA POSICAO DE INICIO DA TABELA
            start_line, start_column = self._get_line_col_from_pos_start(start)
            
    #2      ARMAZENA A TABELA DE DECISAO ENCONTRADA
            decision_table = match.group(0)
    #2      ADICIONA A TABELA ENCONTRADA A LISTA DE TABELAS
            decisions_table_found.append(decision_table)
    #2      ARMAZENA A POSICAO DA TABELA
            positions.append(((start_line, start_column), (end_line, end_column)))

    #2  LEVANTA UMA EXCECAO SE NENHUMA TABELA DE DECISAO FOR ENCONTRADA
        if not decisions_table_found:
            raise ValueError(f' [-] O ARQUIVO NAO POSSUI NENHUMA TABELA DE DECISAO')

    #2  RETORNA AS TABELAS DE DECISAO E SUAS POSICOES
        return decisions_table_found, positions
    #2]

    #1[
    #1 ROTINA: _GET_LINE_COL_FROM_POS_END
    #1 FINALIDADE: OBTER A LINHA E COLUNA DA POSICAO FINAL DE UMA TABELA DE DECISAO
    #1 ENTRADAS: POSICAO (INT)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: _FIND_DECISION_TABLES
    #1 CHAMA: GET_PATH_CODE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _get_line_col_from_pos_end
    def _get_line_col_from_pos_end(self, pos: int) -> tuple:
    #2  ABRE O ARQUIVO E LE O CONTEUDO ATE A POSICAO FINAL
        with open(self.get_path_code(), 'r') as file:
            content = file.read()

    #2  SEPARA O CONTEUDO EM LINHAS ATE A POSICAO ESPECIFICADA
        lines = content[:pos].splitlines()
        
    #2  OBTEM O NUMERO DA LINHA E DA COLUNA PARA A POSICAO FINAL
        line_number = len(lines)
        column_number = len(lines[-1].replace('#TD end table','')) if lines else 0

    #2  RETORNA O NUMERO DA LINHA E COLUNA PARA A POSICAO FINAL
        return line_number, column_number
    #2]

    #1[
    #1 ROTINA: _GET_LINE_COL_FROM_POS_START
    #1 FINALIDADE: OBTER A LINHA E COLUNA DA POSICAO INICIAL DE UMA TABELA DE DECISAO
    #1 ENTRADAS: POSICAO (INT)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: _FIND_DECISION_TABLES
    #1 CHAMA: GET_PATH_CODE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _get_line_col_from_pos_start
    def _get_line_col_from_pos_start(self, pos: int) -> tuple:
    #2  ABRE O ARQUIVO E LE O CONTEUDO ATE A POSICAO INICIAL
        with open(self.get_path_code(), 'r') as file:
            content = file.read()

    #2  SEPARA O CONTEUDO EM LINHAS ATE A POSICAO ESPECIFICADA
        lines = content[:pos].splitlines()
        
    #2  OBTEM O NUMERO DA LINHA E DA COLUNA PARA A POSICAO INICIAL
        line_number = len(lines)
        column_number = len(lines[-1].replace('#TD decision table','')) if lines else 0

    #2  RETORNA O NUMERO DA LINHA E COLUNA PARA A POSICAO INICIAL
        return line_number - 1, column_number
    #2]