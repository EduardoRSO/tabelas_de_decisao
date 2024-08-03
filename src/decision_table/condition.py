#1[
#1 TITULO: condition.py
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 26/07/2024
#1 VERSAO: 1
#1 FINALIDADE: Processar e extrair condições de uma tabela de decisão formatada como string.
#1 ENTRADAS: extracted_decision_table (str) - String contendo a tabela de decisão extraída.
#1 SAIDAS: conditions (list) - Lista de condições extraídas da tabela de decisão.
#1 ROTINAS CHAMADAS: __init__, parse
#1]

import re

class ConditionParser():
    
    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: Inicializar a instância da classe ConditionParser.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self) -> None:
    #2  Inicializa a instância sem configurações adicionais
        pass
    #2]

    #1[
    #1 ROTINA: parse
    #1 FINALIDADE: Extrair e processar as condições da tabela de decisão fornecida como string.
    #1 ENTRADAS: extracted_decision_table (str) - String contendo a tabela de decisão extraída.
    #1 DEPENDENCIAS: re (módulo de expressões regulares)
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: parse
    def parse(self, extracted_decision_table:str) ->list:
    #2  Trata os tipos de condições passadas
        conditions = []
    #2  Procura a seção da tabela de decisão que contém as condições e ações
        match  = re.search(r'(#TD conditions.*?#TD actions)', extracted_decision_table, re.DOTALL)
    #2  Levanta uma exceção se a definição de condições não for encontrada
        if match == None:
            raise ValueError(f' [-] Erro na busca pela definição do condition: {match} e {extracted_decision_table}')
    #2  Itera sobre as linhas de condições extraídas e as adiciona à lista
        for condition_line in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
            conditions.append([condition_line[0], condition_line[1:]])
    #2  Retorna a lista de condições
        return conditions
    #2]
