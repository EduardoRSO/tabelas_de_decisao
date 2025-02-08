#1[
#1 TITULO: DECISION_TABLE.PY
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/08/2024
#1 VERSAO: 1
#1 FINALIDADE: GERENCIAR E PROCESSAR TABELAS DE DECISAO, INCLUINDO PARSING E VALIDACAO DOS DADOS
#1 ENTRADAS: TABELA DE DECISAO EM FORMATO DE STRING
#1 SAIDAS: ATRIBUTOS DA TABELA DE DECISAO, INCLUINDO NOME, CONJUNTOS, CONDICOES E ACOES
#1 ROTINAS CHAMADAS: SETPARSER, CONDITIONPARSER, ACTIONPARSER
#1]

from .set import SetParser
from .condition import ConditionParser
from .action import ActionParser #USO DE PATH RELATIVO

class DecisionTable:

    #2 IGNORE: CONSTANTE QUE REPRESENTA A IGNORANCIA DE UMA CONDICAO
    IGNORE = '!= None'
    
    #2 LISTA DE PALAVRAS-CHAVE QUE DEVEM ESTAR PRESENTES NA TABELA DE DECISAO
    keywords = ['DECISION TABLE','SETS','CONDITIONS','ACTIONS', 'END TABLE']
    
    #2 INSTANCIA UM OBJETO DO PARSER DE CONJUNTOS
    _set_parser = SetParser()
    
    #2 INSTANCIA UM OBJETO DO PARSER DE CONDICOES
    _condition_parser = ConditionParser()
    
    #2 INSTANCIA UM OBJETO DO PARSER DE ACOES
    _action_parser = ActionParser()

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: INICIALIZAR A TABELA DE DECISAO COM OS ATRIBUTOS EXTRAIDOS DA TABELA FORNECIDA
    #1 ENTRADAS: EXTRACTED_DESION_TABLE (STR), POSITION (LIST)
    #1 DEPENDENCIAS: DECISION_TABLE.SET.SETPARSER, DECISION_TABLE.CONDITION.CONDITIONPARSER, DECISION_TABLE.ACTION.ACTIONPARSER
    #1 CHAMADO POR: N/A
    #1 CHAMA: SET_POSITION_OF_DECISION_TABLE_DETECTED, SET_EXTRACTED_DECISION_TABLE, SET_NAME, SET_SETS, SET_CONDITIONS, SET_ACTIONS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, extracted_desion_table: str, position: list): #AS POSIÇÕES INDICAM A LINHA DE INICIO
    #2  DEFINE A POSICAO DETECTADA DA TABELA DE DECISAO
        self.set_position_of_decision_table_detected(position) 
    #2  DEFINE O ATRIBUTO EXTRACTED_DECISION_TABLE
        self.set_extracted_decision_table(extracted_desion_table)
    #2  DEFINE O NOME DA TABELA DE DECISAO
        self.set_name()
    #2  DEFINE OS CONJUNTOS DA TABELA DE DECISAO
        self.set_sets()
    #2  DEFINE AS CONDICOES DA TABELA DE DECISAO
        self.set_conditions()
    #2  DEFINE AS ACOES DA TABELA DE DECISAO
        self.set_actions()
    #2]

    #1[
    #1 ROTINA: __str__
    #1 FINALIDADE: FORNECER UMA REPRESENTACAO EM STRING DO OBJETO DECISIONTABLE
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: PRINT
    #1 CHAMA: GET_EXTRACTED_DECISION_TABLE, GET_NAME, GET_SETS, GET_CONDITIONS, GET_ACTIONS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __str__
    def __str__(self) -> str:
    #2  RETORNA UMA STRING FORMATADA COM OS ATRIBUTOS DA TABELA DE DECISAO
        return f' [+] DecisionTable:\n     extracted_decision_table: {self.get_extracted_decision_table()}\n     name: {self.get_name()}\n     sets: {self.get_sets()}\n     conditions: {self.get_conditions()}\n     actions: {self.get_actions()}'
    #2]

    #1[
    #1 ROTINA: SET_POSITION_OF_DECISION_TABLE_DETECTED
    #1 FINALIDADE: DEFINIR O ATRIBUTO POSITION_OF_DECISION_TABLE_DETECTED
    #1 ENTRADAS: POSITION (LIST)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_position_of_decision_table_detected
    def set_position_of_decision_table_detected(self, position: list) -> None:
    #2  DEFINE O ATRIBUTO POSITION_OF_DECISION_TABLE_DETECTED
        self.position_of_decision_table = position
    #2]

    #1[
    #1 ROTINA: SET_EXTRACTED_DECISION_TABLE
    #1 FINALIDADE: DEFINIR O ATRIBUTO EXTRACTED_DECISION_TABLE APOS VALIDACAO
    #1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: _IS_VALID_DECISION_TABLE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_extracted_decision_table
    def set_extracted_decision_table(self, extracted_decision_table: str) -> None:
    #2  DEFINE O ATRIBUTO EXTRACTED_DECISION_TABLE COM BASE NA VALIDACAO
        self.extracted_decision_table = self._is_valid_decision_table(extracted_decision_table)
    #2]

    #1[
    #1 ROTINA: SET_NAME
    #1 FINALIDADE: DEFINIR O ATRIBUTO NAME COM BASE NA PRIMEIRA LINHA DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: _IS_VALID_NAME
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_name
    def set_name(self) -> None:
    #2  DEFINE O ATRIBUTO NAME APOS VALIDACAO
        self.name = self._is_valid_name()
    #2]

    #1[
    #1 ROTINA: SET_SETS
    #1 FINALIDADE: DEFINIR O ATRIBUTO SETS COM BASE NO PARSING DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: DECISION_TABLE.SET.SETPARSER
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: _SETPARSER.PARSE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_sets
    def set_sets(self) -> None:
    #2  DEFINE O ATRIBUTO SETS UTILIZANDO O PARSER DE CONJUNTOS
        self.sets = self._set_parser.parse(self.get_extracted_decision_table())
    #2]

    #1[
    #1 ROTINA: SET_CONDITIONS
    #1 FINALIDADE: DEFINIR O ATRIBUTO CONDITIONS COM BASE NO PARSING DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: DECISION_TABLE.CONDITION.CONDITIONPARSER
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: _CONDITIONPARSER.PARSE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_conditions
    def set_conditions(self) -> None:
    #2  DEFINE O ATRIBUTO CONDITIONS UTILIZANDO O PARSER DE CONDICOES
        self.conditions = self._condition_parser.parse(self.get_extracted_decision_table())
    #2]

    #1[
    #1 ROTINA: SET_ACTIONS
    #1 FINALIDADE: DEFINIR O ATRIBUTO ACTIONS COM BASE NO PARSING DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: DECISION_TABLE.ACTION.ACTIONPARSER
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: _ACTIONPARSER.PARSE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_actions
    def set_actions(self) -> None:
    #2  DEFINE O ATRIBUTO ACTIONS UTILIZANDO O PARSER DE ACOES
        self.actions = self._action_parser.parse(self.get_extracted_decision_table())
    #2]

    #1[
    #1 ROTINA: GET_EXTRACTED_DECISION_TABLE
    #1 FINALIDADE: RETORNAR O ATRIBUTO EXTRACTED_DECISION_TABLE
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __STR__, GET_DECISION_TABLE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_extracted_decision_table
    def get_extracted_decision_table(self) -> str:
    #2  RETORNA O ATRIBUTO EXTRACTED_DECISION_TABLE
        return self.extracted_decision_table
    #2]

    #1[
    #1 ROTINA: GET_KEYWORDS
    #1 FINALIDADE: RETORNAR A LISTA DE PALAVRAS-CHAVE UTILIZADAS NA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_keywords
    def get_keywords(self) -> list:
    #2  RETORNA A LISTA DE PALAVRAS-CHAVE
        return self.keywords
    #2]

    #1[
    #1 ROTINA: GET_NAME
    #1 FINALIDADE: RETORNAR O NOME DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __STR__, GET_DECISION_TABLE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_name
    def get_name(self) -> str:
    #2  RETORNA O ATRIBUTO NAME
        return self.name
    #2]

    #1[
    #1 ROTINA: GET_SETS
    #1 FINALIDADE: RETORNAR UMA COPIA DA LISTA DE CONJUNTOS DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __STR__, GET_DECISION_TABLE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_sets
    def get_sets(self) -> list:
    #2  RETORNA UMA COPIA DO ATRIBUTO SETS
        return self.sets.copy()
    #2]

    #1[
    #1 ROTINA: GET_CONDITIONS
    #1 FINALIDADE: RETORNAR UMA COPIA DA LISTA DE CONDICOES DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __STR__, GET_DECISION_TABLE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_conditions
    def get_conditions(self) -> list:
    #2  RETORNA UMA COPIA DO ATRIBUTO CONDITIONS
        return self.conditions.copy()
    #2]

    #1[
    #1 ROTINA: GET_ACTIONS
    #1 FINALIDADE: RETORNAR UMA COPIA DA LISTA DE ACOES DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __STR__, GET_DECISION_TABLE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_actions
    def get_actions(self) -> list:
    #2  RETORNA UMA COPIA DO ATRIBUTO ACTIONS
        return self.actions.copy()
    #2]

    #1[
    #1 ROTINA: GET_DECISION_TABLE
    #1 FINALIDADE: RETORNAR UM DICIONARIO COM TODOS OS VALORES EXTRAIDOS DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: GET_NAME, GET_SETS, GET_CONDITIONS, GET_ACTIONS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_decision_table
    def get_decision_table(self) -> dict:
    #2  CRIA E RETORNA UM DICIONARIO COM TODOS OS ATRIBUTOS DA TABELA DE DECISAO
        return {
            'name': self.get_name(),
            'sets': self.get_sets(),
            'conditions': self.get_conditions(),
            'actions': self.get_actions()
        }
    #2]

    #1[
    #1 ROTINA: _IS_VALID_DECISION_TABLE
    #1 FINALIDADE: VERIFICAR A VALIDADE DA TABELA DE DECISAO ATRAVES DA PRESENCA DE PALAVRAS-CHAVE
    #1 ENTRADAS: EXTRACTED_DECISION_TABLE (STR)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: SET_EXTRACTED_DECISION_TABLE
    #1 CHAMA: GET_KEYWORDS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_decision_table
    def _is_valid_decision_table(self, extracted_decision_table: str) -> str:
    #2  VERIFICA SE A TABELA DE DECISAO CONTEM TODAS AS PALAVRAS-CHAVE NECESSARIAS
        for keyword in self.get_keywords():
            if keyword not in extracted_decision_table.upper():
                raise ValueError(f' [-] Tabela de decisao nao possui {keyword}: {extracted_decision_table}')
    #2  RETORNA A TABELA DE DECISAO VALIDADA
        return extracted_decision_table
    #2]

    #1[
    #1 ROTINA: _IS_VALID_NAME
    #1 FINALIDADE: VERIFICAR A VALIDADE DO NOME DA TABELA DE DECISAO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: SET_NAME
    #1 CHAMA: GET_EXTRACTED_DECISION_TABLE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _is_valid_name
    def _is_valid_name(self) -> str:
    #2  OBTEM A PRIMEIRA LINHA DA TABELA DE DECISAO E REMOVE ESPACOS EM BRANCO
        decision_table_lines = self.get_extracted_decision_table().split('\n')[0].strip()
    #2  DIVIDE A PRIMEIRA LINHA DA TABELA DE DECISAO PELOS ESPACOS EM BRANCO E IGNORA OS 3 PRIMEIROS ELEMENTOS
        first_line_splitted_by_empty_spaces = decision_table_lines.split(' ')[3:]
    #2  VERIFICA SE O NOME DA TABELA E VALIDO
        if first_line_splitted_by_empty_spaces == []:
            raise ValueError(f' [-] Tabela de decisao nao possui nome {first_line_splitted_by_empty_spaces}: {decision_table_lines}')
    #2  RETORNA O NOME VALIDADO
        return ' '.join(first_line_splitted_by_empty_spaces)
    #2]

    #1[
    #1 ROTINA: _SET_TRANSLATED_SET_BY_NAME
    #1 FINALIDADE: CRIAR UM DICIONARIO PARA TRADUZIR OS NOMES DOS CONJUNTOS EM CODIGO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: GET_TRANSLATED_SET_BY_NAME
    #1 CHAMA: GET_SETS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _set_translated_set_by_name
    def _set_translated_set_by_name(self) -> None:
    #2  DEFINE AS TRADUCOES PADRAO PARA 'Y', 'N', E '-'
        self._translated_set_by_name = {
            'Y': '== True',
            'N': '== False',
            '-': self.IGNORE
            }
    #2  ADICIONA AS TRADUCOES DOS CONJUNTOS OBTIDOS DA TABELA DE DECISAO
        for td_set_name, td_set_value in self.get_sets():
            self._translated_set_by_name[td_set_name] = td_set_value
    #2]

    #1[
    #1 ROTINA: _SET_SEQUENCE_OF_ACTIONS
    #1 FINALIDADE: CRIAR UM DICIONARIO QUE MAPEIA INDICES PARA LISTAS DE ACOES
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: GET_SEQUENCE_OF_ACTIONS_BY_ID
    #1 CHAMA: GET_ACTIONS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _set_sequence_of_actions
    def _set_sequence_of_actions(self) -> None:
    #2  CRIA UM DICIONARIO QUE MAPEIA INDICES PARA LISTAS DE ACOES ORDENADAS
        self._sequence_of_actions = {}
    #2  ITERA SOBRE CADA ACAO E SEU ORDENAMENTO OBTIDOS DA TABELA DE DECISAO
        for action_name, action_ordering in self.get_actions():
    #2      ITERA SOBRE CADA INDICE E ORDEM DA ACAO
            for index, action_order in enumerate(action_ordering):
    #2          CRIA UMA ENTRADA PARA O INDICE NO DICIONARIO, CASO NAO EXISTA
                self._sequence_of_actions[index] = self._sequence_of_actions.get(index, [])
    #2          ADICIONA A ACAO AO INDICE SE A ORDEM NAO FOR '0'
                if action_order != '0':
                    self._sequence_of_actions[index].append((int(action_order), action_name))
    #2  ORDENA AS ACOES POR ORDEM NO DICIONARIO
        for index in self._sequence_of_actions.keys():
            if len(self._sequence_of_actions[index]) > 1:
                self._sequence_of_actions[index].sort(key=lambda x: x[0])
    #2]

    #1[
    #1 ROTINA: GET_SEQUENCE_OF_ACTIONS_BY_ID
    #1 FINALIDADE: RETORNAR A SEQUENCIA DE ACOES PARA UM DADO ID
    #1 ENTRADAS: ACTION_ID (INT)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: _SET_SEQUENCE_OF_ACTIONS
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_sequence_of_actions_by_id
    def get_sequence_of_actions_by_id(self, action_id: int) -> list:
    #2  VERIFICA SE A SEQUENCIA DE ACOES JA FOI DEFINIDA, SE NAO, CRIA-A
        if not hasattr(self, '_sequence_of_actions'):
            self._set_sequence_of_actions()
    #2  VERIFICA SE O INDICE RECEBIDO E VALIDO
        if self._sequence_of_actions.get(action_id) is None:
            raise ValueError(f' [-] Indice da sequencia de acoes invalido. Dicionario de sequencia de acoes: {self._sequence_of_actions} Indice recebido: {action_id}')
    #2  RETORNA UMA LISTA VAZIA SE NAO HOUVER ACOES PARA O INDICE
        elif len(self._sequence_of_actions[action_id]) == 0:
            return []
    #2  RETORNA A SEQUENCIA DE ACOES ASSOCIADAS AO INDICE
        else:
            return [action_tuple[1] for action_tuple in self._sequence_of_actions[action_id]]
    #2]

    #1[
    #1 ROTINA: GET_TRANSLATED_SET_BY_NAME
    #1 FINALIDADE: RETORNAR A TRADUCAO DO NOME DO CONJUNTO EM CODIGO
    #1 ENTRADAS: SET_NAME (STR)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: _SET_TRANSLATED_SET_BY_NAME
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_translated_set_by_name
    def get_translated_set_by_name(self, set_name: str) -> str:
    #2  VERIFICA SE O DICIONARIO DE TRADUCOES JA FOI DEFINIDO, SE NAO, CRIA-O
        if not hasattr(self, '_translated_set_by_name'):
            self._set_translated_set_by_name()
    #2  VERIFICA SE O NOME DO CONJUNTO RECEBIDO E VALIDO
        if self._translated_set_by_name.get(set_name) is None:
            raise ValueError(f' [-] Nome do conjunto invalido. Dicionario de traducoes por nome do conjunto {self._translated_set_by_name} Nome recebido: {set_name}')
    #2  RETORNA A TRADUCAO DO NOME DO CONJUNTO
        else:
            return self._translated_set_by_name[set_name]
    #2]