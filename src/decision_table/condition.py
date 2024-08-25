#1[
#1 TITULO: CONDITION.PY
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/08/2024
#1 VERSAO: 1
#1 FINALIDADE: PROCESSAR E EXTRAIR CONDICOES DE UMA TABELA DE DECISAO FORMATADA COMO STRING
#1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR) - STRING CONTENDO A TABELA DE DECISAO EXTRAIDA
#1 SAIDAS: CONDITIONS (LIST) - LISTA DE CONDICOES EXTRAIDAS DA TABELA DE DECISAO
#1 ROTINAS CHAMADAS: __INIT__, PARSE
#1]

import re

class ConditionParser():
    
    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: INICIALIZAR A INSTANCIA DA CLASSE CONDITIONPARSER
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self) -> None:
    #2  INICIALIZA A INSTANCIA SEM CONFIGURACOES ADICIONAIS
        pass
    #2]

    #1[
    #1 ROTINA: PARSE
    #1 FINALIDADE: EXTRAIR E PROCESSAR AS CONDICOES DA TABELA DE DECISAO FORNECIDA COMO STRING
    #1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR) - STRING CONTENDO A TABELA DE DECISAO EXTRAIDA
    #1 DEPENDENCIAS: RE (MODULO DE EXPRESOES REGULARES)
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: parse
    def parse(self, extracted_decision_table: str) -> list:
    #2  TRATA OS TIPOS DE CONDICOES PASSADAS
        conditions = []
    #2  PROCURA A SECAO DA TABELA DE DECISAO QUE CONTEM AS CONDICOES E ACOES
        match = re.search(r'(#TD conditions.*?#TD actions)', extracted_decision_table, re.DOTALL)
    #2  LEVANTA UMA EXCECAO SE A DEFINICAO DE CONDICOES NAO FOR ENCONTRADA
        if match is None:
            raise ValueError(f' [-] Erro na busca pela definicao do condition: {match} e {extracted_decision_table}')
    #2  ITERA SOBRE AS LINHAS DE CONDICOES EXTRAIDAS E AS ADICIONA A LISTA
        for condition_line in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
            conditions.append([condition_line[0], condition_line[1:]])
    #2  RETORNA A LISTA DE CONDICOES
        return conditions
    #2]
