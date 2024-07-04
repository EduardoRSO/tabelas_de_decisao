from decision_table.decision_table import DecisionTable

class CodeGenerator():

    def __init__(self, initial_spacing:str=' ', default_spacing:str='   '):
        
        self._decision_table_tradution_methods = {
            'switch_method' : self._switch_method,
            'fatoracoes_sucessivas': self._fatoracoes_sucessivas,
            'busca_exaustiva' : self._busca_exaustiva,
            'programacao_dinamica' : self._programacao_dinamica
        }
        self.initial_spacing = initial_spacing
        self.default_spacing = default_spacing

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
    
    def product_of_entries_by_condition(self, td: DecisionTable) ->int:
        '''
        Retorna o produto da quantidade de entradas para cada condição
        '''
        produto_de_entradas = 1
        for condicao in td.get_conditions():
           produto_de_entradas *= len(set(condicao[1]))
        return produto_de_entradas
    
    def list_entries_by_condition(self, td: DecisionTable) ->list:
        '''
        Retorna uma lista com a quantidade de entradas para cada condição
        '''
        lista_de_entradas = []
        for condicao in td.get_conditions():
           lista_de_entradas.append(len(set(condicao[1])))
        return lista_de_entradas
    

    def _generate_initialization_code(self, td: DecisionTable) ->None:
        '''
        Gera o código de inicialização das variáveis auxiliares necessárias para a definição da ação baseada nos valores das condições
        '''
        self.generated_code = ''
        for index, condicao in enumerate(td.get_conditions()):
            self.generated_code += f'{self.initial_spacing}I_{index} = 0 #Inicialização do auxiliar da condição {condicao[0]}\n'
        self.generated_code += f'{self.initial_spacing}I   = 0 #Inicialização do número da regra\n'

    def _generate_if_or_elif_code(self, td: DecisionTable, condition:str, condition_value: str, index:int, aux_variable_value:int,if_or_elif:str) ->None:
        '''
        Gera o código para o if/elif em python, dado uma condição, um valor e um índice do auxiliar da condição
        '''
        self.generated_code += f'{self.initial_spacing}{if_or_elif} {condition} {td.get_translated_set_by_name(condition_value)}:\n{self.initial_spacing+self.default_spacing}I_{index} = {aux_variable_value}\n'

    def _generate_action_id_calculation_code(self, td: DecisionTable) -> None:
        '''
        Gera o código que soma os valores das variáveis auxiliares das condições para definir o índice da ação no match
        '''
        self.generated_code += f'{self.initial_spacing}I = '
        entries_by_condition = self.list_entries_by_condition(td)
        for i in range(len(td.get_conditions())):
            self.generated_code += '('
            for j in range(i+1, len(td.get_conditions())):
                self.generated_code += f'{entries_by_condition[j]}*'
            self.generated_code += f'1)*I_{i} + '
        self.generated_code += '1\n'
    
    def _generate_match_code(self, td: DecisionTable) -> None:
        '''
        Gera o código que faz o match da indexação calculada
        '''
        self.generated_code += f'{self.initial_spacing}match I:\n'    
        for M in range(self.product_of_entries_by_condition(td)):
            self.generated_code += f'{self.initial_spacing + self.default_spacing}case {M}:'
            for action in td.get_sequence_of_actions_by_id(M):
                self.generated_code += f'\n{self.initial_spacing + 2*self.default_spacing}{action}'
            self.generated_code += '\n'
        self.generated_code += f'{self.initial_spacing + self.default_spacing}case _:\n{self.initial_spacing + 2*self.default_spacing}exit()\n'   
         
    def _switch_method(self, td: DecisionTable) ->None:
        '''
        Implementação do método de tradução de tabelas de decisão: Switch Method
        '''
        self._generate_initialization_code(td)
        for index, linha_de_condicao in enumerate(td.get_conditions()):
            C = set()
            n_i = 0
            condicao = linha_de_condicao[0]
            entradas = linha_de_condicao[1:][0]
            for C_ij in entradas:
                if C_ij not in C:
                    n_i +=1
                    c_ij = C_ij
                    if len(C) == 0:
                        self._generate_if_or_elif_code(td,condicao,c_ij,index,0,'if')
                    else:
                        self._generate_if_or_elif_code(td,condicao,c_ij,index,n_i-1,'elif')
                    C.add(c_ij) if c_ij != '-' else C.add(['Y','N'])
        self._generate_action_id_calculation_code(td)
        self._generate_match_code(td)
        print(self.generated_code)

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

    def generate_code(self, decision_table: DecisionTable) ->None:
        '''
        Gera código a partir de uma tabelade decisão com o método definido na instanciação
        '''
        self.method(decision_table)

#agora está finalizada a minha reestruturação do código para orientação a objetos
#eu consegui obter o comportamento que eu desejava, que era a flexbilidade e facilidade para alteração e implementação de novas funções
#agora resta continuar desenvolvendo o que havia sido proposto pelo Val na ultima reunião:

# o código gerado deve carregar a TD documentada no início dele, convertendo a auto documentacao para o nível 2
# implementar a possiblidade de invocar uma TD dentro de uma TD.
#   Para isso, imagino que a solução mais fácil seria definir que toda TD é construída como uma função no código, porque a invocação seria uma mera chamada de função: td_<Nome>()
#   Usar essa estratégia de funções permite até que a inserção seja mais simples: Posso optar por definir as funções no topo do código e inserir a chamada da função onde ela havia sido construída
#   um outro exemplo comentado pelo Val era que, se fosse possivel invocar uma TD, tambem fosse posivel decidir se quero que volte para a 1a após a conclusão da 2a ou não.
# construir exemplos de aplicação de TD: Trilhas BCC | ações como funções
# implementar o codeInserter e assegurar que funciona

