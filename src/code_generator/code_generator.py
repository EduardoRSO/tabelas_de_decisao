import operator
from functools import reduce
from decision_table.decision_table import DecisionTable

class CodeGenerator():

    def __init__(self):
        
        self._decision_table_tradution_methods = {
            'switch_method' : self._switch_method,
            'fatoracoes_sucessivas': self._fatoracoes_sucessivas,
            'busca_exaustiva' : self._busca_exaustiva,
            'programacao_dinamica' : self._programacao_dinamica
        }
        self.set_method('switch_method')

    def set_method(self, method_name:str) ->None:
        '''
        Setter do atributo method
        '''
        try:
            self.method_name = method_name
            self.method = self._decision_table_tradution_methods[method_name]
        except Exception as e:            
            raise ValueError(f' [-] Nome inválido. Nomes disponíveis: {self._decision_table_tradution_methods.keys()} Nome recebido: {method_name}. Exception: {e}')

    def get_method(self) ->list:
        '''
        Getter do atributo method
        ''' 
        return self.method_name, self.method
    
    def _switch_method(self, td: DecisionTable) ->None:
        '''
        Implementação do método de tradução de tabelas de decisão: Switch Method
        '''
        self.generated_code = "\n".join([f'I_{index} = 0 #Inicialização do auxiliar da condição {condicao}' for index, condicao in enumerate(td.get_conditions())])+'\nI   = 0 #Inicialização do número da regra\n'
        for index, linha_de_condicao in enumerate(td.get_conditions()):
            C = set()
            n_i = 0
            condicao = linha_de_condicao[0]
            entradas = linha_de_condicao[1:]
            for C_ij in entradas:
                if C_ij not in C:
                    n_i +=1
                    c_ij = C_ij
                    if len(C) == 0:
                        self.generated_code += f'if {condicao} {td.get_translated_set_by_name(c_ij)}:\n    I_{index} = 0\n'
                    else:
                        self.generated_code += f'elif {condicao} {td.get_translated_set_by_name(c_ij)}:\n    I_{index} = {n_i-1}\n'
                    C.add(c_ij) if c_ij != '-' else C.add(['Y','N'])
    
            entradas_por_condicao = [len(set(condicao))-1 for condicao in td.get_conditions()] 
            self.generated_code += f"I = {'+'.join(['*'.join(['1']+[f'{entradas_por_condicao[j]}' for j in range(i+1,len(td.get_conditions()))])+f'*I_{i}' for i in range(len(td.get_conditions()))])}\n"
            self.generated_code += f'match I:\n'
            for M in range(reduce(operator.mul, entradas_por_condicao, 1)):
                codigo_gerado += f'    case {M}:\n{trata_acao(td,M,"        ")}\n'
            codigo_gerado += f'    case _:\n        exit()\n'    
            return codigo_gerado

    def _fatoracoes_sucessivas(self, decision_table: DecisionTable) ->None:
        '''
        Implementação do método de tradução de tabelas de decisão: Fatorações sucessivas
        '''
        pass

    def _busca_exaustiva(self, decision_table: DecisionTable) ->None:
        '''
        Implementação do método de tradução de tabelas de decisão: Busca exaustiva
        '''
        pass

    def _programacao_dinamica(self, decision_table: DecisionTable) ->None:
        '''
        Implementação do método de tradução de tabelas de decisão: Programação dinâmica
        '''
        pass

    def generate_code(self, decision_table: DecisionTable) ->str:
        '''
        Gera código a partir de uma tabelade decisão com o método definido na instanciação
        '''
        self.method(decision_table)
        return self.generated_code 