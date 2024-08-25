#1[
#1 TITULO: SET.PY
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/08/2024
#1 VERSAO: 1
#1 FINALIDADE: DEFINIR E TRATAR OS TIPOS DE CONJUNTOS EXTRAIDOS DE UMA TABELA DE DECISAO
#1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR) - STRING CONTENDO A TABELA DE DECISAO EXTRAIDA COM DEFINICOES DE CONJUNTOS E CONDICOES
#1 SAIDAS: LIST - LISTA DE CONJUNTOS FORMATADOS E TRATADOS COM BASE NAS DEFINICOES ENCONTRADAS NA TABELA DE DECISAO
#1 ROTINAS CHAMADAS: RE.SEARCH
#1]

import re

class SetParser():

    #1[
    #1 ROTINA: PARSE
    #1 FINALIDADE: ANALISAR E FORMATAR CONJUNTOS ENCONTRADOS NA TABELA DE DECISAO
    #1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR) - STRING CONTENDO A TABELA DE DECISAO EXTRAIDA
    #1 DEPENDENCIAS: RE
    #1 CHAMADO POR: N/A
    #1 CHAMA: RE.SEARCH
    #1]
    #2[
    #2 PSEUDOCODIGO DE: parse
    def parse(self, extracted_decision_table: str) -> list:
    #2  TRATA OS TIPOS DE CONJUNTOS PASSADOS
        sets = []
    #2  BUSCA PELA DEFINICAO DE CONJUNTOS E CONDICOES NA TABELA DE DECISAO
        match = re.search(r'(#TD sets.*?#TD conditions)', extracted_decision_table, re.DOTALL)
    #2  LEVANTA UMA EXCECAO SE NAO ENCONTRAR A DEFINICAO DO SET
        if match is None:
            raise ValueError(f' [-] Erro na busca pela definicao do set: {match} e {extracted_decision_table}')
    #2  ITERA SOBRE AS DEFINICOES DE CONJUNTOS ENCONTRADAS
        for set_name, set_definition in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
    #2      VERIFICA SE A DEFINICAO E UM CONJUNTO DELIMITADO POR CHAVES (EX: {a,b,c})
            if re.search(r'{.*}', set_definition):
    #2          FORMATA A DEFINICAO PARA O FORMATO DE UM CONJUNTO EM PYTHON
                sets.append([set_name, f"in set([{','.join(set_definition.strip('{}').split(','))}])"])
    #2      VERIFICA SE A DEFINICAO CONTEM OPERADORES RELACIONAIS (EX: >, <, >=, <=)
            elif re.search(r'>|<|>=|<=', set_definition):
    #2          MANTEM A DEFINICAO ORIGINAL PARA OPERADORES RELACIONAIS
                sets.append([set_name, set_definition])
    #2      VERIFICA SE A DEFINICAO CONTEM UM OPERADOR DE IGUALDADE SIMPLES (EX: =)
            elif re.search(r'=', set_definition):
    #2          FORMATA A DEFINICAO PARA UMA COMPARACAO DE IGUALDADE EM PYTHON (==)
                sets.append([set_name, f"== {set_definition.strip('=')}"])
    #2      VERIFICA SE A DEFINICAO E UM INTERVALO DE VALORES (EX: 1..10)
            elif re.search(r'\.\.', set_definition):
    #2          FORMATA A DEFINICAO PARA UM INTERVALO USANDO RANGE EM PYTHON
                sets.append([set_name, f"in range({set_definition.split('..')[0]},{set_definition.split('..')[1]})"])
    #2  RETORNA A LISTA DE CONJUNTOS TRATADOS
        return sets
    #2]
