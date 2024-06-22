from decision_table.set import SetParser
from decision_table.condition import ConditionParser
from decision_table.action import ActionParser

class DecisionTable:
    
    keywords = ['DECISION TABLE','SETS','CONDITIONS','ACTIONS', 'END TABLE']
    _set_parser = SetParser()
    _condition_parser = ConditionParser()
    _action_parser = ActionParser()

    def __init__(self, extracted_desion_table:str):
        self.set_extracted_decision_table(extracted_desion_table)
        self.set_name()
        self.set_sets()
        self.set_conditions()
        self.set_actions()

    def __str__(self) ->str:
        '''
        Representação em string do objeto Decision Table
        '''
        return f' [+] DecisionTable:\n     extracted_decision_table: {self.get_extracted_decision_table()}\n     name: {self.get_name()}\n     sets: {self.get_sets()}\n     conditions: {self.get_conditions()}\n     actions: {self.get_actions()}'
        
    def set_extracted_decision_table(self, extracted_decision_table:str) ->None:
        '''
        Setter do atributo extracted_decision_table
        '''
        self.extracted_decision_table = self._is_valid_decision_table(extracted_decision_table)

    def set_name(self) ->None:
        '''
        Setter do atributo name
        '''
        self.name = self._is_valid_name()

    def set_sets(self) ->None:
        '''
        Setter do atributo sets
        '''
        self.sets = self._set_parser.parse(self.get_extracted_decision_table())

    def set_conditions(self) ->None:
        '''
        Setter do atributo conditions
        '''        
        self.conditions = self._condition_parser.parse(self.get_extracted_decision_table())

    def set_actions(self) ->None:
        '''
        Setter do atributo actions
        '''
        self.actions = self._action_parser.parse(self.get_extracted_decision_table())

    def get_extracted_decision_table(self) ->str:
        '''
        Getter do atributo extracted_decision_table
        '''
        return self.extracted_decision_table

    def get_keywords(self) ->list:
        '''
        Getter do atributo keywords
        '''
        return self.keywords

    def get_name(self) ->str:
        '''
        Getter do atributo name
        '''
        return self.name
    
    def get_sets(self) ->list:
        '''
        Getter do atributo sets
        '''
        return self.sets

    def get_conditions(self) ->list:
        '''
        Getter do atributo conditions
        '''
        return self.conditions
    
    def get_actions(self) ->list:
        '''
        Getter do atributo actions
        '''
        return self.actions
    
    def get_decision_table(self) ->dict:
        '''
        Retorna um dicionário com todos os valores extraídos da tabela de decisão
        '''
        return {
            'name' : self.get_name(),
            'sets' : self.get_sets(),
            'conditions' : self.get_conditions(),
            'actions' : self.get_actions()
        }

    def _is_valid_decision_table(self, extracted_decision_table:str) ->str:
        '''
        Verifica se uma tabela de decisão é válida através da presença de keywords
        '''
        for keyword in self.get_keywords():
            if keyword not in extracted_decision_table.upper():
                raise ValueError(f' [-] Tabela de decisão não possui {keyword}: {extracted_decision_table}')
        return extracted_decision_table        
    
    def _is_valid_name(self) ->str:
        '''
        Verifica se um nome é valido através da presença de uma string não vazia
        '''
        decision_table_lines = self.get_extracted_decision_table().split('\n')[0].strip()
        first_line_splitted_by_empty_spaces = decision_table_lines.split(' ')[3:] 
        if first_line_splitted_by_empty_spaces == []:
            raise ValueError(f' [-] Tabela de decisão não possui nome {first_line_splitted_by_empty_spaces}: {decision_table_lines}')
        return ' '.join(first_line_splitted_by_empty_spaces)          