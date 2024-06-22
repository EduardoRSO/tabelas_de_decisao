import re

class ActionParser():
    def __init__(self) -> None:
        pass 

    def parse(self, extracted_decision_table:str) ->list:
        '''
        Trata os tipos de ações passadas
        '''
        actions = []
        match  = re.search(r'(#TD actions.*?#TD end table)',extracted_decision_table, re.DOTALL)
        if match == None:
            raise ValueError(f' [-] Erro na busca pela definição da action: {match} e {extracted_decision_table}')
        for action_line in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
            actions.append([action_line[0], action_line[1:]])
        return actions