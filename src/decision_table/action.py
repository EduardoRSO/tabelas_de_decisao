#1[
#1 TITULO: action.py
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 26/07/2024
#1 VERSAO: 1
#1 FINALIDADE: Analisar e extrair ações de uma tabela de decisão passada como string.
#1 ENTRADAS: extracted_decision_table (str) - String contendo a tabela de decisão extraída com definições de ações.
#1 SAIDAS: List - Lista de ações extraídas da tabela de decisão.
#1 ROTINAS CHAMADAS: re.search
#1]

import re

class ActionParser():

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: Inicializar a instância da classe ActionParser.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self) -> None:
    #2  Inicializa a instância sem parâmetros
        pass 
    #2]

    #1[
    #1 ROTINA: parse
    #1 FINALIDADE: Extrair e tratar ações de uma tabela de decisão passada como string.
    #1 ENTRADAS: extracted_decision_table (str) - String contendo a tabela de decisão com definições de ações.
    #1 DEPENDENCIAS: re (biblioteca padrão do Python)
    #1 CHAMADO POR: N/A
    #1 CHAMA: re.search
    #1]
    #2[
    #2 PSEUDOCODIGO DE: parse
    def parse(self, extracted_decision_table:str) ->list:
    #2  Trata os tipos de ações passadas
        actions = []
    #2  Busca a seção de ações na tabela de decisão usando expressão regular
        match  = re.search(r'(#TD actions.*?#TD end table)', extracted_decision_table, re.DOTALL)
    #2  Levanta um erro se a busca não encontrar uma correspondência
        if match == None:
            raise ValueError(f' [-] Erro na busca pela definição da action: {match} e {extracted_decision_table}')
    #2  Itera sobre cada linha de ação extraída e organiza os dados
        for action_line in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
            actions.append([action_line[0], action_line[1:]])
    #2  Retorna a lista de ações extraídas
        return actions
    #2]
