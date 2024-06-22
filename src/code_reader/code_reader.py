import os 
import re

class CodeReader:

    def __init__(self, path_code:str) ->None:
        self.set_path_code(path_code)
        self.set_code()
        self.set_extracted_decision_tables() 

    def __str__(self) -> str:
        '''
        Representação em string do objeto CodeReader
        '''
        return f' [+] CodeReader:\n     path_code: {self.get_path_code()}\n     len(code): {len(self.get_code())}\n     len(extracted_decision_tables): {len(self.get_extracted_decision_tables())}'

    def set_path_code(self, path_code:str) ->None:
        '''
        Setter do atributo path_code
        '''
        self.path_code = self._is_valid_path(path_code)

    def set_code(self) ->None:
        '''
        Setter do atributo code
        '''
        self.code = self._is_valid_code()

    def set_extracted_decision_tables(self) ->None:
        '''
        Setter do atributo extracted_decision_tables
        '''
        self.extracted_decision_tables = self._find_decision_tables()

    def get_path_code(self) ->str:
        '''
        Getter do atributo path_code
        '''
        return self.path_code
    
    def get_code(self) ->str:
        '''
        Getter do atributo code
        '''
        return self.code

    def get_extracted_decision_tables(self) -> list:
        '''
        Getter do atributo extracted_decision_tables
        '''
        return self.extracted_decision_tables

    def _is_valid_path(self, path_code:str) ->str:
        '''
        Verifica se o path passado é um arquivo python.
        '''
        if not os.path.isfile(path_code):
            raise FileNotFoundError(f" [-] O path passado {path_code} não é um arquivo.")
        if not path_code.endswith('.py'):
            raise ValueError(f" [-] O path do arquivo passado {path_code} não é um arquivo python") 
        return path_code
    
    def _is_valid_code(self) ->str:
        '''
        Verifica se o arquivo está vazio
        '''
        with open(self.get_path_code(),'r') as file:
            content = file.read().strip()
            if len(content) == 0:
                raise ValueError(f' [-] O arquivo passado {self.get_path_code()} está vazio')
            return content
        
    def _find_decision_tables(self) ->list:
        '''
        Busca por tabelas de decisão no arquivo indicado 
        '''
        decisions_table_found = re.findall(r'(#TD decision table.*?#TD end table)',self.get_code(), re.DOTALL)
        if len(decisions_table_found) == 0:
            raise ValueError(f' [-] O arquivo não possui nenhuma tabela de decisão')
        return decisions_table_found   
