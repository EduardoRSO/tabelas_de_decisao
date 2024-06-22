import re

class ConditionParser():
    def __init__(self) -> None:
        pass

    def parse(self, extracted_decision_table:str) ->list:
        '''
        Trata os tipos de condições passadas
        '''
        conditions = []
        match  = re.search(r'(#TD conditions.*?#TD actions)',extracted_decision_table, re.DOTALL)
        if match == None:
            raise ValueError(f' [-] Erro na busca pela definição do condition: {match} e {extracted_decision_table}')
        for condition_line in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
            conditions.append([condition_line[0], condition_line[1:]])
        return conditions