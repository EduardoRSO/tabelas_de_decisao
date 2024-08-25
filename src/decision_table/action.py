#1[
#1 TITULO: ACTION.PY
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/08/2024
#1 VERSAO: 1
#1 FINALIDADE: ANALISAR E EXTRAIR ACOES DE UMA TABELA DE DECISAO PASSADA COMO STRING
#1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR) - STRING CONTENDO A TABELA DE DECISAO EXTRAIDA COM DEFINICOES DE ACOES
#1 SAIDAS: LIST - LISTA DE ACOES EXTRAIDAS DA TABELA DE DECISAO
#1 ROTINAS CHAMADAS: RE.SEARCH
#1]

import re

class ActionParser():

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: INICIALIZAR A INSTANCIA DA CLASSE ACTIONPARSER
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self) -> None:
    #2  INICIALIZA A INSTANCIA SEM PARAMETROS
        pass 
    #2]

    #1[
    #1 ROTINA: PARSE
    #1 FINALIDADE: EXTRAIR E TRATAR ACOES DE UMA TABELA DE DECISAO PASSADA COMO STRING
    #1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR) - STRING CONTENDO A TABELA DE DECISAO COM DEFINICOES DE ACOES
    #1 DEPENDENCIAS: RE (BIBLIOTECA PADRAO DO PYTHON)
    #1 CHAMADO POR: N/A
    #1 CHAMA: RE.SEARCH
    #1]
    #2[
    #2 PSEUDOCODIGO DE: parse
    def parse(self, extracted_decision_table: str) -> list:
    #2  TRATA OS TIPOS DE ACOES PASSADAS
        actions = []
    #2  BUSCA A SECAO DE ACOES NA TABELA DE DECISAO USANDO EXPRESSAO REGULAR
        match = re.search(r'(#TD actions.*?#TD end table)', extracted_decision_table, re.DOTALL)
    #2  LEVANTA UM ERRO SE A BUSCA NAO ENCONTRAR UMA CORRESPONDENCIA
        if match is None:
            raise ValueError(f' [-] Erro na busca pela definicao da action: {match} e {extracted_decision_table}')
    #2  ITERA SOBRE CADA LINHA DE ACAO EXTRAIDA E ORGANIZA OS DADOS
        for action_line in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
            actions.append([action_line[0], action_line[1:]])
    #2  RETORNA A LISTA DE ACOES EXTRAIDAS
        return actions
    #2]