#1[
#1 TITULO: code_generator.py
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/08/2024
#1 VERSAO: 1
#1 FINALIDADE: GERAR CODIGO A PARTIR DE TABELAS DE DECISAO UTILIZANDO DIFERENTES METODOS DE TRADUCAO.
#1 ENTRADAS: TABELA DE DECISAO (DECISIONTABLE)
#1 SAIDAS: CODIGO PYTHON GERADO COM BASE NA TABELA DE DECISAO
#1 ROTINAS CHAMADAS: SET_METHOD, GET_METHOD, PRODUCT_OF_ENTRIES_BY_CONDITION, LIST_ENTRIES_BY_CONDITION, _GENERATE_DOCUMENTATION_CODE, _GENERATE_INITIALIZATION_CODE, _GENERATE_IF_OR_ELIF_CODE, _GENERATE_ACTION_ID_CALCULATION_CODE, _GENERATE_MATCH_CODE, _SWITCH_METHOD, _FATORACOES_SUCESSIVAS, _BUSCA_EXAUSTIVA, _PROGRAMACAO_DINAMICA, GENERATE_CODE
#1]

from src.decision_table.decision_table import DecisionTable

class CodeGenerator():

    #1[
    #1 ROTINA: __init__
    #1 FINALIDADE: INICIALIZAR A INSTANCIA DA CLASSE CODEGENERATOR.
    #1 ENTRADAS: INITIAL_SPACING (STR), DEFAULT_SPACING (STR)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: N/A
    #1 CHAMA: SET_METHOD
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, initial_spacing:str='<INITIAL_SPACING>', default_spacing:str='<DEFAULT_SPACING>'):
    #2  INICIALIZA O DICIONARIO DE METODOS DE TRADUCAO
        self._decision_table_tradution_methods = {
            'switch_method' : self._switch_method,
            'fatoracoes_sucessivas': self._fatoracoes_sucessivas,
            'busca_exaustiva' : self._busca_exaustiva,
            'programacao_dinamica' : self._programacao_dinamica
        }
    #2  DEFINE O ESPACAMENTO INICIAL E O ESPACAMENTO PADRAO
        self.initial_spacing = initial_spacing
        self.default_spacing = default_spacing
    #2  DEFINE O METODO PADRAO COMO 'SWITCH_METHOD'
        self.set_method('switch_method')
    #2]

    #1[
    #1 ROTINA: set_method
    #1 FINALIDADE: DEFINIR O METODO DE TRADUCAO A SER UTILIZADO.
    #1 ENTRADAS: METHOD_NAME (STR)
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: __init__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: set_method
    def set_method(self, method_name:str) ->None:
    #2  TENTA DEFINIR O METODO DE TRADUCAO COM BASE NO NOME FORNECIDO
        try:
    #2      DEFINE O NOME DO METODO
            self.method_name = method_name
    #2      DEFINE O METODO DE TRADUCAO
            self.method = self._decision_table_tradution_methods[method_name]
    #2  LEVANTA UMA EXCECAO SE O NOME DO METODO FOR INVALIDO
        except Exception as e:            
            raise ValueError(f' [-] Nome inválido. Nomes disponíveis: {self._decision_table_tradution_methods.keys()} Nome recebido: {method_name}. Exception: {e}')
    #2]

    #1[
    #1 ROTINA: get_method
    #1 FINALIDADE: RETORNAR O NOME E O METODO DE TRADUCAO ATUAL.
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: get_method
    def get_method(self) ->list:
    #2  RETORNA O NOME DO METODO E O METODO DE TRADUCAO ATUAL
        return self.method_name, self.method
    #2]

    #1[
    #1 ROTINA: product_of_entries_by_condition
    #1 FINALIDADE: CALCULAR O PRODUTO DA QUANTIDADE DE ENTRADAS PARA CADA CONDICAO EM UMA TABELA DE DECISAO.
    #1 ENTRADAS: TD (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: _GENERATE_ACTION_ID_CALCULATION_CODE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: product_of_entries_by_condition
    def product_of_entries_by_condition(self, td: DecisionTable) ->int:
    #2  INICIALIZA O PRODUTO DE ENTRADAS COMO 1
        produto_de_entradas = 1
    #2  ITERA SOBRE AS CONDICOES DA TABELA DE DECISAO
        for condicao in td.get_conditions():
    #2      REMOVE O SIMBOLO '-'
            if '-' in condicao[1]:
                condicao[1] = condicao[1] +['Y','N']   
    #2      MULTIPLICA O PRODUTO DE ENTRADAS PELO NUMERO DE ENTRADAS UNICAS DA CONDICAO
            produto_de_entradas *= len(set(condicao[1])) 
    #2  RETORNA O PRODUTO DE ENTRADAS
        return produto_de_entradas
    #2]

    #1[
    #1 ROTINA: list_entries_by_condition
    #1 FINALIDADE: RETORNAR UMA LISTA COM A QUANTIDADE DE ENTRADAS PARA CADA CONDICAO.
    #1 ENTRADAS: TD (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: _GENERATE_ACTION_ID_CALCULATION_CODE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: list_entries_by_condition
    def list_entries_by_condition(self, td: DecisionTable) ->list:
    #2  INICIALIZA UMA LISTA DE ENTRADAS
        lista_de_entradas = []
    #2  ITERA SOBRE AS CONDICOES DA TABELA DE DECISAO
        for condicao in td.get_conditions():
    #2      ADICIONA O NUMERO DE ENTRADAS UNICAS DA CONDICAO A LISTA DE ENTRADAS
            lista_de_entradas.append(len(set(condicao[1])))
    #2  RETORNA A LISTA DE ENTRADAS
        return lista_de_entradas
    #2]

    #1[
    #1 ROTINA: _generate_documentation_code
    #1 FINALIDADE: INSERIR A TABELA DE DECISAO COMO DOCUMENTACAO DE SEGUNDO NIVEL PARA O EXTRATOR DE AUTO-DOCUMENTACOES.
    #1 ENTRADAS: TD (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: _SWITCH_METHOD
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_documentation_code
    def _generate_documentation_code(self, td: DecisionTable) ->None:
    #2  INICIA O BLOCO DE DOCUMENTACAO DE SEGUNDO NIVEL
        self.generated_code += f'{self.initial_spacing}#2[\n'
    #2  EXTRAI A TABELA DE DECISAO E FORMATA COMO DOCUMENTACAO
        decision_table_str = td.get_extracted_decision_table()
    #2  ITERA SOBRE CADA LINHA DA TABELA DE DECISAO EXTRAIDA
        for linha in decision_table_str.split('\n'):
    #2      ADICIONA A LINHA FORMATADA AO CODIGO GERADO
            self.generated_code += linha.lstrip().replace('#TD',f'{self.initial_spacing}#2 #TD') + '\n'
    #2  FINALIZA O BLOCO DE DOCUMENTACAO DE SEGUNDO NIVEL
        self.generated_code += f'{self.initial_spacing}#2]\n'
    #2]

    #1[
    #1 ROTINA: _generate_initialization_code
    #1 FINALIDADE: GERAR O CODIGO DE INICIALIZACAO DAS VARIAVEIS AUXILIARES NECESSARIAS PARA A DEFINICAO DA ACAO BASEADA NOS VALORES DAS CONDICOES.
    #1 ENTRADAS: TD (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: _SWITCH_METHOD
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_initialization_code
    def _generate_initialization_code(self, td: DecisionTable) ->None:
    #2  ADICIONA A DEFINICAO DA FUNCAO DE TABELA DE DECISAO AO CODIGO GERADO
        self.generated_code += f'{self.initial_spacing}def decision_table_{td.get_name()}() ->None:\n'
    #2  ITERA SOBRE AS CONDICOES DA TABELA DE DECISAO
        for index, condicao in enumerate(td.get_conditions()):
    #2      ADICIONA A INICIALIZACAO DO AUXILIAR DA CONDICAO AO CODIGO GERADO
            self.generated_code += f'{self.initial_spacing+self.default_spacing}I_{index} = 0 #Inicialização do auxiliar da condição {condicao[0]}\n'
    #2  ADICIONA A INICIALIZACAO DO NUMERO DA REGRA AO CODIGO GERADO
        self.generated_code += f'{self.initial_spacing+self.default_spacing}I   = 0 #Inicialização do número da regra\n'
    #2]

    def _generate_invoke(self, td: DecisionTable) -> None:
    #2  GERA O CODIGO PARA INVOCAR A FUNCAO DA TABELA DE DECISAO
        self.generated_code += f'{self.initial_spacing}decision_table_{td.get_name()}()\n'

    #1[
    #1 ROTINA: _generate_if_or_elif_code
    #1 FINALIDADE: GERAR O CODIGO PARA O IF/ELIF EM PYTHON, DADO UMA CONDICAO, UM VALOR E UM INDICE DO AUXILIAR DA CONDICAO.
    #1 ENTRADAS: TD (DECISIONTABLE), CONDITION (STR), CONDITION_VALUE (STR), INDEX (INT), AUX_VARIABLE_VALUE (INT), IF_OR_ELIF (STR)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: _SWITCH_METHOD
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_if_or_elif_code
    def _generate_if_or_elif_code(self, td: DecisionTable, condition:str, condition_value: str, index:int, aux_variable_value:int,if_or_elif:str) ->None:
    #2  ADICIONA A LINHA DE CODIGO IF/ELIF COM A CONDICAO E O VALOR
        self.generated_code += f'{self.initial_spacing+self.default_spacing}{if_or_elif} {condition} {td.get_translated_set_by_name(condition_value)}:\n{self.initial_spacing+2*self.default_spacing}I_{index} = {aux_variable_value}\n'
    #2]

    #1[
    #1 ROTINA: _generate_action_id_calculation_code
    #1 FINALIDADE: GERAR O CODIGO QUE SOMA OS VALORES DAS VARIAVEIS AUXILIARES DAS CONDICOES PARA DEFINIR O INDICE DA ACAO NO MATCH.
    #1 ENTRADAS: TD (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: _SWITCH_METHOD
    #1 CHAMA: LIST_ENTRIES_BY_CONDITION
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_action_id_calculation_code
    def _generate_action_id_calculation_code(self, td: DecisionTable) -> None:
    #2  ADICIONA A INICIALIZACAO DO CALCULO DO INDICE DA ACAO AO CODIGO GERADO
        self.generated_code += f'{self.initial_spacing + self.default_spacing}I = '
    #2  OBTEM O NUMERO DE ENTRADAS POR CONDICAO
        entries_by_condition = self.list_entries_by_condition(td)
    #2  ITERA SOBRE AS CONDICOES PARA GERAR O CODIGO DE CALCULO DO ID
        for i in range(len(td.get_conditions())):
    #2      ADICIONA O PARENTESES DE ABERTURA AO CODIGO
            self.generated_code += '('
    #2      GERA O CODIGO DE MULTIPLICACAO PARA CALCULAR O INDICE
            for j in range(i+1, len(td.get_conditions())):
                self.generated_code += f'{entries_by_condition[j]}*'
    #2      FINALIZA O CALCULO PARA A CONDICAO ATUAL E ADICIONA AO CODIGO GERADO
            self.generated_code += f'1)*I_{i} + '
    #2  REMOVE O ULTIMO ' + ' DA EXPRESSAO GERADA
        self.generated_code = self.generated_code[:-3]+'\n'
    #2]

    #1[
    #1 ROTINA: _generate_match_code
    #1 FINALIDADE: GERAR O CODIGO QUE FAZ O MATCH DA INDEXACAO CALCULADA.
    #1 ENTRADAS: TD (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: _SWITCH_METHOD
    #1 CHAMA: PRODUCT_OF_ENTRIES_BY_CONDITION
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _generate_match_code
    def _generate_match_code(self, td: DecisionTable) -> None:
    #2  ADICIONA O INICIO DA ESTRUTURA MATCH AO CODIGO GERADO
        self.generated_code += f'{self.initial_spacing+self.default_spacing}match I:\n'    
    #2  ITERA SOBRE CADA ACAO PARA GERAR OS CASES DO MATCH
        for M in range(self.product_of_entries_by_condition(td)):
    #2      ADICIONA UM CASE AO MATCH PARA CADA POSSIVEL ACAO
            self.generated_code += f'{self.initial_spacing + 2*self.default_spacing}case {M}:'
    #2      ITERA SOBRE AS ACOES PARA O CASE ATUAL
            for action in td.get_sequence_of_actions_by_id(M):
    #2          ADICIONA A ACAO AO CODIGO GERADO
                self.generated_code += f'\n{self.initial_spacing + 3*self.default_spacing}{action}'
    #2      ADICIONA UMA QUEBRA DE LINHA APOS CADA CASE
            self.generated_code += '\n'
    #2  ADICIONA O CASO DEFAULT AO CODIGO GERADO
        self.generated_code += f'{self.initial_spacing + 2*self.default_spacing}case _:\n{self.initial_spacing + 3*self.default_spacing}exit()\n'   
    #2]

    #1[
    #1 ROTINA: _switch_method
    #1 FINALIDADE: IMPLEMENTAR O METODO DE TRADUCAO DE TABELAS DE DECISAO: SWITCH METHOD.
    #1 ENTRADAS: TD (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: GENERATE_CODE
    #1 CHAMA: _GENERATE_DOCUMENTATION_CODE, _GENERATE_INITIALIZATION_CODE, _GENERATE_IF_OR_ELIF_CODE, _GENERATE_ACTION_ID_CALCULATION_CODE, _GENERATE_MATCH_CODE
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _switch_method
    def _switch_method(self, td: DecisionTable) ->None:
    #2  INICIALIZA A VARIAVEL DE CODIGO GERADO COMO UMA STRING VAZIA
        self.generated_code = ''
    #2  GERA O CODIGO DE DOCUMENTACAO PARA A TABELA DE DECISAO
        self._generate_documentation_code(td)
    #2  GERA O CODIGO DE INICIALIZACAO DAS VARIAVEIS NECESSARIAS
        self._generate_initialization_code(td)
    #2  ITERA SOBRE AS CONDICOES DA TABELA DE DECISAO
        for index, linha_de_condicao in enumerate(td.get_conditions()):
            C = set()
            n_i = 0
            condicao = linha_de_condicao[0]
            entradas = linha_de_condicao[1:][0]
    #2      ITERA SOBRE AS ENTRADAS DA CONDICAO PARA GERAR O CODIGO IF/ELIF
            for C_ij in entradas:
                if C_ij not in C:
                    n_i += 1
                    c_ij = C_ij
    #2          GERA O CODIGO IF PARA A PRIMEIRA CONDICAO
                    if len(C) == 0:
                        self._generate_if_or_elif_code(td, condicao, c_ij, index, 0, 'if')
    #2          GERA O CODIGO ELIF PARA AS CONDICOES SUBSEQUENTES
                    else:
                        self._generate_if_or_elif_code(td, condicao, c_ij, index, n_i-1, 'elif')
    #2          ADICIONA A ENTRADA AO CONJUNTO DE ENTRADAS PROCESSADAS
                    if c_ij != '-':
                        C.add(c_ij)
    #2          ADICIONA AS ENTRADAS 'Y' E 'N' PARA O SIMBOLO '-'
                    else:
                        C.add('Y')
                        C.add('N')
    #2  GERA O CODIGO PARA CALCULO DO ID DA ACAO
        self._generate_action_id_calculation_code(td)
    #2  GERA O CODIGO MATCH PARA A INDEXACAO CALCULADA
        self._generate_match_code(td)
    #2  GERA O CODIGO PARA INVOCACAO DA FUNCAO DA TABELA DE DECISAO
        self._generate_invoke(td)
    #2]

    #1[
    #1 ROTINA: _fatoracoes_sucessivas
    #1 FINALIDADE: IMPLEMENTAR O METODO DE TRADUCAO DE TABELAS DE DECISAO: FATORACOES SUCESSIVAS.
    #1 ENTRADAS: DECISION_TABLE (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _fatoracoes_sucessivas
    def _fatoracoes_sucessivas(self, decision_table: DecisionTable) ->None:
    #2  METODO AINDA NAO IMPLEMENTADO
        pass
    #2]

    #1[
    #1 ROTINA: _busca_exaustiva
    #1 FINALIDADE: IMPLEMENTAR O METODO DE TRADUCAO DE TABELAS DE DECISAO: BUSCA EXAUSTIVA.
    #1 ENTRADAS: DECISION_TABLE (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _busca_exaustiva
    def _busca_exaustiva(self, decision_table: DecisionTable) ->None:
    #2  METODO AINDA NAO IMPLEMENTADO
        pass
    #2]

    #1[
    #1 ROTINA: _programacao_dinamica
    #1 FINALIDADE: IMPLEMENTAR O METODO DE TRADUCAO DE TABELAS DE DECISAO: PROGRAMACAO DINAMICA.
    #1 ENTRADAS: DECISION_TABLE (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _programacao_dinamica
    def _programacao_dinamica(self, decision_table: DecisionTable) ->None:
    #2  METODO AINDA NAO IMPLEMENTADO
        pass
    #2]

    #1[
    #1 ROTINA: generate_code
    #1 FINALIDADE: GERAR CODIGO A PARTIR DE UMA TABELA DE DECISAO COM O METODO DEFINIDO NA INSTANCIACAO.
    #1 ENTRADAS: DECISION_TABLE (DECISIONTABLE)
    #1 DEPENDENCIAS: DECISION_TABLE.DECISION_TABLE.DECISIONTABLE
    #1 CHAMADO POR: N/A
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: generate_code
    def generate_code(self, decision_table: DecisionTable) ->str:
    #2  EXECUTA O METODO DEFINIDO PARA GERAR O CODIGO
        self.method(decision_table)
    #2  RETORNA O CODIGO GERADO
        return self.generated_code
    #2]
