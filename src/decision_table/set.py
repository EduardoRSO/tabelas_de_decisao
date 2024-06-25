import re

class SetParser():
    def parse(self, extracted_decision_table:str) ->list:
        '''
        Trata os tipos de conjuntos passados
        '''
        sets = []
        match  = re.search(r'(#TD sets.*?#TD conditions)',extracted_decision_table, re.DOTALL)
        if match == None:
            raise ValueError(f' [-] Erro na busca pela definição do set: {match} e {extracted_decision_table}')
        for set_name, set_definition in [line.split()[1:] for line in match.group(0).split('\n')][1:-1]:
            if '{' in set_definition:
                sets.append([set_name , f"in set([{','.join(set_definition.strip('{}').split(','))}])"])
            elif '>' in set_definition:
                sets.append([set_name, set_definition])
            elif '=' in set_definition:
                sets.append([set_name, f"== {set_definition.strip('=')}"])
            elif '..' in set_definition:
                sets.append([set_name, f"in range({set_definition.split('..')[0]},{set_definition.split('..')[1]})"])
        return sets