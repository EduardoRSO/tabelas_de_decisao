#1[
#1 TITULO: decision_table.py
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 26/07/2024
#1 VERSAO: 1
#1 FINALIDADE: Gerenciar e processar tabelas de decisão, incluindo parsing e validação dos dados.
#1 ENTRADAS: Tabela de decisão em formato de string
#1 SAIDAS: Atributos da tabela de decisão, incluindo nome, conjuntos, condições e ações
#1 ROTINAS CHAMADAS: SetParser, ConditionParser, ActionParser
#1]

from .set import SetParser
from .condition import ConditionParser
from .action import ActionParser

class DecisionTable:

    IGNORE = '!= None'
    keywords = ['DECISION TABLE','SETS','CONDITIONS','ACTIONS', 'END TABLE']
    _set_parser = SetParser()
    _condition_parser = ConditionParser()
    _action_parser = ActionParser()

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: Inicializa a tabela de decisão com os atributos extraídos da tabela fornecida.
    #1 ENTRADAS: extracted_desion_table (str)
    #1 DEPENDENCIAS: decision_table.set.SetParser, decision_table.condition.ConditionParser, decision_table.action.ActionParser
    #1 CHAMADO POR: N/A
    #1 CHAMA: set_extracted_decision_table, set_name, set_sets, set_conditions, set_actions
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, extracted_desion_table:str, position:list):
    #2  Define o atributo extracted_decision_table e extrai o nome, conjuntos, condições e ações
        self.set_position_of_decision_table_detected(position)
        self.set_extracted_decision_table(extracted_desion_table)
        self.set_name()
        self.set_sets()
        self.set_conditions()
        self.set_actions()
    #2]

    #1[
    #1 ROTINA: __str__
    #1 FINALIDADE: Fornecer uma representação em string do objeto DecisionTable.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: print
    #1 CHAMA: get_extracted_decision_table, get_name, get_sets, get_conditions, get_actions
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __str__
    def __str__(self) ->str:
    #2  Retorna uma string formatada com os atributos da tabela de decisão
        return f' [+] DecisionTable:\n     extracted_decision_table: {self.get_extracted_decision_table()}\n     name: {self.get_name()}\n     sets: {self.get_sets()}\n     conditions: {self.get_conditions()}\n     actions: {self.get_actions()}'
    #2]

    #1[
    #1 ROTINA: set_end_position_of_decision_table_detected
    #1 FINALIDADE: Definir o atributo end_position_of_decision_table.
    #1 ENTRADAS: position (tuple)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2 PSEUDOCODIGO DE: set_extracted_decision_table
    def set_position_of_decision_table_detected(self, position:list) ->None:
        #2  Define o atributo end_position_of_decision_table
        self.position_of_decision_table = position
    #2]

    #1[
    #1 ROTINA: set_extracted_decision_table
    #1 FINALIDADE: Definir o atributo extracted_decision_table após validar a tabela fornecida.
    #1 ENTRADAS: extracted_decision_table (str)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: _is_valid_decision_table
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_extracted_decision_table
    def set_extracted_decision_table(self, extracted_decision_table:str) ->None:
    #2  Define o atributo extracted_decision_table com base na validação
        self.extracted_decision_table = self._is_valid_decision_table(extracted_decision_table)
    #2]

    #1[
    #1 ROTINA: set_name
    #1 FINALIDADE: Definir o atributo name com base na primeira linha da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: _is_valid_name
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_name
    def set_name(self) ->None:
    #2  Define o atributo name após validação
        self.name = self._is_valid_name()
    #2]

    #1[
    #1 ROTINA: set_sets
    #1 FINALIDADE: Definir o atributo sets com base no parsing da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: decision_table.set.SetParser
    #1 CHAMADO POR: __init__
    #1 CHAMA: _set_parser.parse
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_sets
    def set_sets(self) ->None:
    #2  Define o atributo sets utilizando o parser de conjuntos
        self.sets = self._set_parser.parse(self.get_extracted_decision_table())
    #2]

    #1[
    #1 ROTINA: set_conditions
    #1 FINALIDADE: Definir o atributo conditions com base no parsing da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: decision_table.condition.ConditionParser
    #1 CHAMADO POR: __init__
    #1 CHAMA: _condition_parser.parse
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_conditions
    def set_conditions(self) ->None:
    #2  Define o atributo conditions utilizando o parser de condições
        self.conditions = self._condition_parser.parse(self.get_extracted_decision_table())
    #2]

    #1[
    #1 ROTINA: set_actions
    #1 FINALIDADE: Definir o atributo actions com base no parsing da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: decision_table.action.ActionParser
    #1 CHAMADO POR: __init__
    #1 CHAMA: _action_parser.parse
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_actions
    def set_actions(self) ->None:
    #2  Define o atributo actions utilizando o parser de ações
        self.actions = self._action_parser.parse(self.get_extracted_decision_table())
    #2]

    #1[
    #1 ROTINA: get_extracted_decision_table
    #1 FINALIDADE: Retornar o atributo extracted_decision_table.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__, get_decision_table
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_extracted_decision_table
    def get_extracted_decision_table(self) ->str:
    #2  Retorna o atributo extracted_decision_table
        return self.extracted_decision_table
    #2]

    #1[
    #1 ROTINA: get_keywords
    #1 FINALIDADE: Retornar a lista de palavras-chave utilizadas na tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_keywords
    def get_keywords(self) ->list:
    #2  Retorna a lista de palavras-chave
        return self.keywords
    #2]

    #1[
    #1 ROTINA: get_name
    #1 FINALIDADE: Retornar o nome da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__, get_decision_table
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_name
    def get_name(self) ->str:
    #2  Retorna o atributo name
        return self.name
    #2]

    #1[
    #1 ROTINA: get_sets
    #1 FINALIDADE: Retornar uma cópia da lista de conjuntos da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__, get_decision_table
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_sets
    def get_sets(self) ->list:
    #2  Retorna uma cópia do atributo sets
        return self.sets.copy()
    #2]

    #1[
    #1 ROTINA: get_conditions
    #1 FINALIDADE: Retornar uma cópia da lista de condições da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__, get_decision_table
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_conditions
    def get_conditions(self) ->list:
    #2  Retorna uma cópia do atributo conditions
        return self.conditions.copy()
    #2]

    #1[
    #1 ROTINA: get_actions
    #1 FINALIDADE: Retornar uma cópia da lista de ações da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __str__, get_decision_table
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_actions
    def get_actions(self) ->list:
    #2  Retorna uma cópia do atributo actions
        return self.actions.copy()
    #2]

    #1[
    #1 ROTINA: get_decision_table
    #1 FINALIDADE: Retornar um dicionário com todos os valores extraídos da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: get_name, get_sets, get_conditions, get_actions
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_decision_table
    def get_decision_table(self) ->dict:
    #2  Cria e retorna um dicionário com todos os atributos da tabela de decisão
        return {
            'name' : self.get_name(),
            'sets' : self.get_sets(),
            'conditions' : self.get_conditions(),
            'actions' : self.get_actions()
        }
    #2]

    #1[
    #1 ROTINA: _is_valid_decision_table
    #1 FINALIDADE: Verificar a validade da tabela de decisão através da presença de palavras-chave.
    #1 ENTRADAS: extracted_decision_table (str)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: set_extracted_decision_table
    #1 CHAMA: get_keywords
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_decision_table
    def _is_valid_decision_table(self, extracted_decision_table:str) ->str:
    #2  Verifica se a tabela de decisão contém todas as palavras-chave necessárias
        for keyword in self.get_keywords():
            if keyword not in extracted_decision_table.upper():
                raise ValueError(f' [-] Tabela de decisão não possui {keyword}: {extracted_decision_table}')
        return extracted_decision_table        
    #2]

    #1[
    #1 ROTINA: _is_valid_name
    #1 FINALIDADE: Verificar a validade do nome da tabela de decisão.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: set_name
    #1 CHAMA: get_extracted_decision_table
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_name
    def _is_valid_name(self) ->str:
    #2  Verifica se a primeira linha da tabela contém um nome válido
        decision_table_lines = self.get_extracted_decision_table().split('\n')[0].strip()
        first_line_splitted_by_empty_spaces = decision_table_lines.split(' ')[3:] 
        if first_line_splitted_by_empty_spaces == []:
            raise ValueError(f' [-] Tabela de decisão não possui nome {first_line_splitted_by_empty_spaces}: {decision_table_lines}')
        return ' '.join(first_line_splitted_by_empty_spaces)        
    #2]

    #1[
    #1 ROTINA: _set_translated_set_by_name
    #1 FINALIDADE: Criar um dicionário para traduzir os nomes dos conjuntos em código.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: get_translated_set_by_name
    #1 CHAMA: get_sets
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _set_translated_set_by_name
    def _set_translated_set_by_name(self) ->None:
    #2  Define as traduções padrão para 'Y' e 'N' e adiciona as traduções dos conjuntos
        self._translated_set_by_name = {
            'Y': '== True',
            'N': '== False',
            '-': self.IGNORE
            }
        for td_set_name, td_set_value in self.get_sets():
            self._translated_set_by_name[td_set_name] = td_set_value
    #2]

    #1[
    #1 ROTINA: _set_sequence_of_actions
    #1 FINALIDADE: Criar um dicionário que mapeia índices para listas de ações.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: get_sequence_of_actions_by_id
    #1 CHAMA: get_actions
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _set_sequence_of_actions
    def _set_sequence_of_actions(self) ->None:
    #2  Cria um dicionário que mapeia índices para listas de ações ordenadas
        self._sequence_of_actions = {}
        for action_name, action_ordering in self.get_actions():
            for index, action_order in enumerate(action_ordering):
                self._sequence_of_actions[index] = self._sequence_of_actions.get(index,[])
                if action_order != '0':
                    self._sequence_of_actions[index].append((int(action_order),action_name))
        for index in self._sequence_of_actions.keys():
            if len(self._sequence_of_actions[index]) > 1:
                self._sequence_of_actions[index].sort(key= lambda x: x[0]) 
    #2]

    #1[
    #1 ROTINA: get_sequence_of_actions_by_id
    #1 FINALIDADE: Retornar a sequência de ações para um dado ID.
    #1 ENTRADAS: action_id (int)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: _set_sequence_of_actions
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_sequence_of_actions_by_id
    def get_sequence_of_actions_by_id(self, action_id:int) ->list:
    #2  Retorna a lista de ações para o índice fornecido, criando a sequência se necessário
        if not hasattr(self, '_sequence_of_actions'):
            self._set_sequence_of_actions()
        if self._sequence_of_actions.get(action_id) == None:
            raise ValueError(f' [-] Índice da sequência de ações inválido. Dicionário de sequência de ações: {self._sequence_of_actions} Índice recebido: {action_id}')
        elif len(self._sequence_of_actions[action_id]) == 0:
            return []
        else:
            return [action_tuple[1] for action_tuple in self._sequence_of_actions[action_id]]
    #2]

    #1[
    #1 ROTINA: get_translated_set_by_name
    #1 FINALIDADE: Retornar a tradução do nome do conjunto em código.
    #1 ENTRADAS: set_name (str)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: _set_translated_set_by_name
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_translated_set_by_name
    def get_translated_set_by_name(self, set_name:str) ->str:
    #2  Retorna a tradução do nome do conjunto em código
        if not hasattr(self, '_translated_set_by_name'):
            self._set_translated_set_by_name()
        if self._translated_set_by_name.get(set_name) == None:
            raise ValueError(f' [-] Nome do conjunto inválido. Dicionário de traduções por nome do conjunto {self._translated_set_by_name} Nome recebido: {set_name}') 
        else:
            return self._translated_set_by_name[set_name]
    #2]
