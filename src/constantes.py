FRASE_INPUT_PATH = "INSIRA O PATH DO DIRETÓRIO: "

REGEX_NIVEIS_DE_DOCUMENTACAO = r'#[0-9]\[((.|\n)*?)#[0-9]\]'

REGEX_TD_TRADUZIDA  = r'(%decision table(.|\n)*?%end table)'

REGEX_EXTRAI_NOME = r'%decision table (.*)'

REGEX_EXTRAI_PREPARACAO = r'%preparation\n\s*((.|\n)*?)\n\s*%'

REGEX_EXTRAI_CONJUNTOS = r'%sets\n\s*((.|\n)*?)\n\s*%'

REGEX_EXTRAI_CONDICOES = r'%conditions\n\s*((.|\n)*?)\n\s*%'

REGEX_EXTRAI_ACOES = r'%actions\n\s*((.|\n)*?)\n\s*%'

PALAVRAS_RESERVADAS = ['%generate','%decision table','%preparation','%sets','%conditions','%actions','%end table']

IGNORADAS = ['%-','%Numero da Regra']

SIMBOLOS_RESERVADOS = ['-','$','*']

SEPARADOR = ':'

COMENTARIO = 'DESCRICAO'

NIVEL_0 = ['TITULO','AUTOR','DATA','VERSAO','FINALIDADE','ENTRADAS','SAIDAS','ROTINAS CHAMADAS']

NIVEL_1 = ['ROTINA','FINALIDADE','ENTRADAS','DEPENDENCIAS','CHAMADO POR','CHAMA']

NIVEL_2 = ['PSEUDOCODIGO DE', 'DESCRICAO']

NIVEL_3 = ['DETALHES DE', 'DESCRICAO']

NIVEIS = [NIVEL_0, NIVEL_1, NIVEL_2, NIVEL_3]

SINTAXE = ['#1', '#2', '#3']

IDENTIFICADORES = ['ROTINA','PSEUDOCODIGO DE','DETALHES DE']

PONTEIROS = ['DEPENDENCIAS', 'CHAMADO POR', 'CHAMA', 'ROTINAS CHAMADAS']

METADADOS = 'METADADOS'

ROTINAS = 'ROTINAS'

TEMPLATE_ESTRUTURADA_1 = {METADADOS:{},ROTINAS:{}}

TEMPLATE_ESTRUTURADA_2 = {"NIVEL 1":{},"NIVEL 2":{}, "NIVEL 3":{}}

PEGA_NIVEL = {
    ''.join(NIVEL_1): 'NIVEL 1',
    ''.join(NIVEL_2): 'NIVEL 2',
    ''.join(NIVEL_3): 'NIVEL 3',
}

'''
estrutura do arquivo json
    {
    "NOME DO PROGRAMA": 
        {
        "METADADOS": {NIVEL_0}
        },
        "ROTINAS":
        {
            "NOME DA ROTINA":
            {
                "NIVEL 1": {NIVEL_1},
                "NIVEL 2": {NIVEL_2},
                "NIVEL 3": {NIVEL_3}
            },
            (...)
        }
    }
'''

PATH_DOCUMENTACAO = '/home/erso/Documents/tcc/tabelas_de_decisao/exemplos/documentacoes_extraidas/documentacoes.json'

#1[
#1 ROTINA: 
#1 FINALIDADE: 
#1 ENTRADAS:
#1 DEPENDENCIAS: 
#1 CHAMADO POR: 
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: 
#2]

#3[
#3 DETALHES DE: 
#3]
