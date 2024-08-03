#1[
#1 TITULO: set.py
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 26/07/2024
#1 VERSAO: 1
#1 FINALIDADE: Definir e tratar os tipos de conjuntos extraídos de uma tabela de decisão.
#1 ENTRADAS: extracted_decision_table (str) - String contendo a tabela de decisão extraída com definições de conjuntos e condições.
#1 SAIDAS: list - Lista de conjuntos formatados e tratados com base nas definições encontradas na tabela de decisão.
#1 ROTINAS CHAMADAS: re.search
#1]

import re

class SetParser():

    #1[
    #1 ROTINA: parse
    #1 FINALIDADE: Analisar e formatar conjuntos encontrados na tabela de decisão.
    #1 ENTRADAS: extracted_decision_table (str) - String contendo a tabela de decisão extraída.
    #1 DEPENDENCIAS: re
    #1 CHAMADO POR: N/A
    #1 CHAMA: re.search
    #1]
    #2[
    #2 PSEUDOCODIGO DE: parse
    def parse(self, extracted_decision_table:str) ->list:
    #2  Trata os tipos de conjuntos passados
        sets = []
    #2  Busca pela definição de conjuntos e condições na tabela de decisão
        match  = re.search(r'(#TD sets.*?#TD conditions)', extracted_decision_table, re.DOTALL)
    #2  Levanta uma exceção se não encontrar a definição do set
        if match == None:
            raise ValueError(f' [-] Erro na busca pela definição do set: {match} e {extracted_decision_table}')
    #2  Itera sobre as definições de conjuntos encontradas
        for set_name, set_definition in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
    #2      Trata as definições de conjuntos com base em seu formato
            if re.search(r'{.*}', set_definition):
                sets.append([set_name , f"in set([{','.join(set_definition.strip('{}').split(','))}])"])
            elif re.search(r'>|<|>=|<=', set_definition):
                sets.append([set_name, set_definition])
            elif re.search(r'=', set_definition):
                sets.append([set_name, f"== {set_definition.strip('=')}"])
            elif re.search(r'\.\.', set_definition):
                sets.append([set_name, f"in range({set_definition.split('..')[0]},{set_definition.split('..')[1]})"])
    #2  Retorna a lista de conjuntos tratados
        return sets
    #2]
