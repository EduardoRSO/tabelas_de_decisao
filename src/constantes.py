FRASE_INPUT_PATH = "INSIRA O PATH DO DIRETÓRIO: "

REGEX_NIVEIS_DE_DOCUMENTACAO = r'#[0-9]\[((.|\n)*?)#[0-9]\]'

SEPARADOR = ':'

COMENTARIO = 'DESCRICAO'

NIVEL_0 = ['TITULO','AUTOR','DATA','VERSAO','FINALIDADE','ENTRADAS','SAIDAS','ROTINAS CHAMADAS']

NIVEL_1 = ['ROTINA','FINALIDADE','ENTRADAS','DEPENDENCIAS','CHAMADO POR','CHAMA']

NIVEL_2 = ['PSEUDOCODIGO DE', 'DESCRICAO']

NIVEL_3 = ['DETALHES DE', 'DESCRICAO']

NIVEIS = [NIVEL_0, NIVEL_1, NIVEL_2, NIVEL_3]

SINTAXE = ['#1', '#2', '#3']

IDENTIFICADORES = ['ROTINA','PSEUDOCODIGO DE','DETALHES DE']

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