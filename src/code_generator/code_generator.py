#1[
#1 TITULO: code_generator.py
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 26/07/2024
#1 VERSAO: 1
#1 FINALIDADE: Gerar código a partir de tabelas de decisão utilizando diferentes métodos de tradução.
#1 ENTRADAS: Tabela de decisão (DecisionTable)
#1 SAIDAS: Código Python gerado com base na tabela de decisão
#1 ROTINAS CHAMADAS: set_method, get_method, product_of_entries_by_condition, list_entries_by_condition, _generate_documentation_code, _generate_initialization_code, _generate_if_or_elif_code, _generate_action_id_calculation_code, _generate_match_code, _switch_method, _fatoracoes_sucessivas, _busca_exaustiva, _programacao_dinamica, generate_code
#1]

from src.decision_table.decision_table import DecisionTable

class CodeGenerator():

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: Inicializar a instância da classe CodeGenerator.
    #1 ENTRADAS: initial_spacing (str), default_spacing (str)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: N/A
    #1 CHAMA: set_method, porque é o único método implementado
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, initial_spacing:str='<INITIAL_SPACING>', default_spacing:str='<DEFAULT_SPACING>'):
    #2  Inicializa o dicionário de métodos de tradução
        self._decision_table_tradution_methods = {
            'switch_method' : self._switch_method,
            'fatoracoes_sucessivas': self._fatoracoes_sucessivas,
            'busca_exaustiva' : self._busca_exaustiva,
            'programacao_dinamica' : self._programacao_dinamica
        }
    #2  Define o espaçamento inicial e o espaçamento padrão
        self.initial_spacing = initial_spacing
        self.default_spacing = default_spacing
    #2  Define o método padrão como 'switch_method'
        self.set_method('switch_method')
    #2]

    #1[
    #1 ROTINA: set_method
    #1 FINALIDADE: Definir o método de tradução a ser utilizado.
    #1 ENTRADAS: method_name (str)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_method
    def set_method(self, method_name:str) ->None:
    #2  Tenta definir o método de tradução com base no nome fornecido
        try:
    #2      Define o nome do método
            self.method_name = method_name
    #2      Define o método de tradução
            self.method = self._decision_table_tradution_methods[method_name]
    #2  Levanta uma exceção se o nome do método for inválido
        except Exception as e:            
            raise ValueError(f' [-] Nome inválido. Nomes disponíveis: {self._decision_table_tradution_methods.keys()} Nome recebido: {method_name}. Exception: {e}')
    #2]

    #1[
    #1 ROTINA: get_method
    #1 FINALIDADE: Retornar o nome e o método de tradução atual.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_method
    def get_method(self) ->list:
    #2  Retorna o nome do método e o método de tradução atual
        return self.method_name, self.method
    #2]

    #1[
    #1 ROTINA: product_of_entries_by_condition
    #1 FINALIDADE: Calcular o produto da quantidade de entradas para cada condição em uma tabela de decisão.
    #1 ENTRADAS: td (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: _generate_action_id_calculation_code
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: product_of_entries_by_condition
    def product_of_entries_by_condition(self, td: DecisionTable) ->int:
    #2  Inicializa o produto de entradas como 1
        produto_de_entradas = 1
    #2  Itera sobre as condições da tabela de decisão
        for condicao in td.get_conditions():
    #2      Remove o símbolo '-'
            if '-' in condicao[1]:
                condicao[1] = condicao[1] +['Y','N']   
    #2      Multiplica o produto de entradas pelo número de entradas únicas da condição
            produto_de_entradas *= len(set(condicao[1])) 
    #2  Retorna o produto de entradas
        return produto_de_entradas
    #2]

    #1[
    #1 ROTINA: list_entries_by_condition
    #1 FINALIDADE: Retornar uma lista com a quantidade de entradas para cada condição.
    #1 ENTRADAS: td (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: _generate_action_id_calculation_code
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: list_entries_by_condition
    def list_entries_by_condition(self, td: DecisionTable) ->list:
    #2  Inicializa uma lista de entradas
        lista_de_entradas = []
    #2  Itera sobre as condições da tabela de decisão
        for condicao in td.get_conditions():
    #2      Adiciona o número de entradas únicas da condição à lista de entradas
            lista_de_entradas.append(len(set(condicao[1])))
    #2  Retorna a lista de entradas
        return lista_de_entradas
    #2]

    #1[
    #1 ROTINA: _generate_documentation_code
    #1 FINALIDADE: Inserir a tabela de decisão como documentação de segundo nível para o extrator de auto-documentações.
    #1 ENTRADAS: td (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: _switch_method
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_documentation_code
    def _generate_documentation_code(self, td: DecisionTable) ->None:
    #2  Extrai a tabela de decisão e adiciona a documentação gerada ao código
        self.generated_code += f'{self.initial_spacing}#2[\n'
        decision_table_str = td.get_extracted_decision_table()
        for linha in decision_table_str.split('\n'):
            self.generated_code += linha.lstrip().replace('#TD',f'{self.initial_spacing}#2 #TD') + '\n'
        self.generated_code += f'{self.initial_spacing}#2]\n'
    #2]

    #1[
    #1 ROTINA: _generate_initialization_code
    #1 FINALIDADE: Gerar o código de inicialização das variáveis auxiliares necessárias para a definição da ação baseada nos valores das condições.
    #1 ENTRADAS: td (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: _switch_method
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_initialization_code
    def _generate_initialization_code(self, td: DecisionTable) ->None:
    #2  Adiciona a definição da função de tabela de decisão ao código gerado
        self.generated_code += f'{self.initial_spacing}def decision_table_{td.get_name()}() ->None:\n'
    #2  Itera sobre as condições da tabela de decisão
        for index, condicao in enumerate(td.get_conditions()):
    #2      Adiciona a inicialização do auxiliar da condição ao código gerado
            self.generated_code += f'{self.initial_spacing+self.default_spacing}I_{index} = 0 #Inicialização do auxiliar da condição {condicao[0]}\n'
    #2  Adiciona a inicialização do número da regra ao código gerado
        self.generated_code += f'{self.initial_spacing+self.default_spacing}I   = 0 #Inicialização do número da regra\n'
    #2]

    def _generate_invoke(self, td: DecisionTable) -> None:
        self.generated_code += f'{self.initial_spacing}decision_table_{td.get_name()}()\n'

    #1[
    #1 ROTINA: _generate_if_or_elif_code
    #1 FINALIDADE: Gerar o código para o if/elif em Python, dado uma condição, um valor e um índice do auxiliar da condição.
    #1 ENTRADAS: td (DecisionTable), condition (str), condition_value (str), index (int), aux_variable_value (int), if_or_elif (str)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: _switch_method
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_if_or_elif_code
    def _generate_if_or_elif_code(self, td: DecisionTable, condition:str, condition_value: str, index:int, aux_variable_value:int,if_or_elif:str) ->None:
    #2  Adiciona a linha de código if/elif com a condição e o valor
        self.generated_code += f'{self.initial_spacing+self.default_spacing}{if_or_elif} {condition} {td.get_translated_set_by_name(condition_value)}:\n{self.initial_spacing+2*self.default_spacing}I_{index} = {aux_variable_value}\n'
    #2]

    #1[
    #1 ROTINA: _generate_action_id_calculation_code
    #1 FINALIDADE: Gerar o código que soma os valores das variáveis auxiliares das condições para definir o índice da ação no match.
    #1 ENTRADAS: td (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: _switch_method
    #1 CHAMA: list_entries_by_condition
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_action_id_calculation_code
    def _generate_action_id_calculation_code(self, td: DecisionTable) -> None:
    #2  Adiciona a inicialização do cálculo do índice da ação ao código gerado
        self.generated_code += f'{self.initial_spacing + self.default_spacing}I = '
    #2  Obtém o número de entradas por condição
        entries_by_condition = self.list_entries_by_condition(td)
    #2  Adiciona o cálculo das variáveis auxiliares ao código gerado
        for i in range(len(td.get_conditions())):
            self.generated_code += '('
            for j in range(i+1, len(td.get_conditions())):
                self.generated_code += f'{entries_by_condition[j]}*'
            self.generated_code += f'1)*I_{i} + '
    #2  Adiciona o fechamento da expressão e o cálculo final
        self.generated_code = self.generated_code[:-3]+'\n'
    #2]

    #1[
    #1 ROTINA: _generate_match_code
    #1 FINALIDADE: Gerar o código que faz o match da indexação calculada.
    #1 ENTRADAS: td (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: _switch_method
    #1 CHAMA: product_of_entries_by_condition
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_match_code
    def _generate_match_code(self, td: DecisionTable) -> None:
    #2  Adiciona o início da estrutura match ao código gerado
        self.generated_code += f'{self.initial_spacing+self.default_spacing}match I:\n'    
    #2  Itera sobre cada ação e adiciona o código correspondente ao match
        for M in range(self.product_of_entries_by_condition(td)):
            self.generated_code += f'{self.initial_spacing + 2*self.default_spacing}case {M}:'
            for action in td.get_sequence_of_actions_by_id(M):
                self.generated_code += f'\n{self.initial_spacing + 3*self.default_spacing}{action}'
            self.generated_code += '\n'
    #2  Adiciona o caso default ao código gerado
        self.generated_code += f'{self.initial_spacing + 2*self.default_spacing}case _:\n{self.initial_spacing + 3*self.default_spacing}exit()\n'   
    #2]

    #1[
    #1 ROTINA: _switch_method
    #1 FINALIDADE: Implementar o método de tradução de tabelas de decisão: Switch Method.
    #1 ENTRADAS: td (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: generate_code
    #1 CHAMA: _generate_documentation_code, _generate_initialization_code, _generate_if_or_elif_code, _generate_action_id_calculation_code, _generate_match_code
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _switch_method
    def _switch_method(self, td: DecisionTable) ->None:
    #2  Gera a documentação e a inicialização do código
        self.generated_code = ''
        self._generate_documentation_code(td)
        self._generate_initialization_code(td)
    #2  Itera sobre as condições e gera o código if/elif para cada condição
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
                    if c_ij != '-':
                        C.add(c_ij)
                    else:
                        C.add('Y')
                        C.add('N')
    #2  Gera o cálculo do ID da ação e o código de match
        self._generate_action_id_calculation_code(td)
        self._generate_match_code(td)
        self._generate_invoke(td)
    #2]

    #1[
    #1 ROTINA: _fatoracoes_sucessivas
    #1 FINALIDADE: Implementar o método de tradução de tabelas de decisão: Fatorações sucessivas.
    #1 ENTRADAS: decision_table (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _fatoracoes_sucessivas
    def _fatoracoes_sucessivas(self, decision_table: DecisionTable) ->None:
    #2  Método ainda não implementado
        pass
    #2]

    #1[
    #1 ROTINA: _busca_exaustiva
    #1 FINALIDADE: Implementar o método de tradução de tabelas de decisão: Busca exaustiva.
    #1 ENTRADAS: decision_table (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _busca_exaustiva
    def _busca_exaustiva(self, decision_table: DecisionTable) ->None:
    #2  Método ainda não implementado
        pass
    #2]

    #1[
    #1 ROTINA: _programacao_dinamica
    #1 FINALIDADE: Implementar o método de tradução de tabelas de decisão: Programação dinâmica.
    #1 ENTRADAS: decision_table (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _programacao_dinamica
    def _programacao_dinamica(self, decision_table: DecisionTable) ->None:
    #2  Método ainda não implementado
        pass
    #2]

    #1[
    #1 ROTINA: generate_code
    #1 FINALIDADE: Gerar código a partir de uma tabela de decisão com o método definido na instanciação.
    #1 ENTRADAS: decision_table (DecisionTable)
    #1 DEPENDENCIAS: decision_table.decision_table.DecisionTable
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: generate_code
    def generate_code(self, decision_table: DecisionTable) ->str:
    #2  Executa o método definido para gerar o código
        self.method(decision_table)
        return self.generated_code
    #2]
