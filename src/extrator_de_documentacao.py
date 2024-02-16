#1[
#1 TITULO: EXTRATOR DE DOCUMENTACAO
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 15/02/2024
#1 VERSAO: 1
#1 FINALIDADE: GERAR RELATÓRIO CONTENDO A DOCUMENTAÇÃO DE DETERMINADO PROGRAMA
#1 ENTRADAS: ARQUIVO QUE CONTEM O CÓDIGO FONTE COMENTADO POR NÍVEIS; CÓDIGO DO NÍVEL DE COMENTÁRIO DESEJADO;
#1 SAIDAS: ARQUIVO JSON COM A DOCUMENTAÇÃO EXTRAÍDA DO ARQUIVO FONTE;
#1 ROTINAS CHAMADAS: MAIN, CONSTROI_DOCUMENTACOES, AGREGA_DOCUMENTACOES, ESTRUTURA_DOCUMENTACAO, FORMATA_DOCUMENTACAO, EXTRAI_DOCUMENTACAO, PEGA_ARQUIVOS
#1]

import os
import re
import json
import copy
import sys
from constantes import *

#1[
#1 ROTINA: PEGA_ARQUIVOS
#1 FINALIDADE: RETORNA UM CONJUNTO COM O PATH DE CADA ARQUIVO DE UMA PASTA
#1 ENTRADAS: PATH DA PASTA
#1 DEPENDENCIAS: OS
#1 CHAMADO POR: AGREGA_DOCUMENTACOES
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: PEGA_ARQUIVOS
def pega_arquivos(path:str):
    arquivos = []
    #2 CRIA UM CONJUNTO VAZIO A
    for arquivo in os.listdir(path):
        #2 VARRE OS ELEMENTOS DO CONJUNTO DE ARQUIVOS NA PASTA FORNECIDA
        arquivos.append(os.path.join(path,arquivo))
        #2 ADICIONA O SUFIXO DO PATH PARA CADA ELEMENTO
        #2 ADICIONA O ITEM NO CONJUNTO A
    return arquivos
    #2 RETORNA O CONJUNTO A
#2]
    
#3[
#3 DETALHES DE: PEGA_ARQUIVOS
#3 LISTAS EM PYTHON SÃO IMPLEMENTADAS COMO PILHAS, ENTÃO AS INSERÇÕES SÃO INSERIDAS NO FIM DA LISTA
#3 OS.LISTDIR RETORNA OS ARQUIVOS EM UMA ORDEM ARBITRÁRIA
#3]

#1[
#1 ROTINA: EXTRAI_DOCUMENTACAO
#1 FINALIDADE: RETORNA UM CONJUNTO COM TODAS AS DOCUMENTAÇÕES, DE TODOS OS NÍVEIS, DE UM ARQUIVO
#1 ENTRADAS: PATH DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: AGREGA_DOCUMENTACOES
#1 CHAMA: 
#1]
    
#2[
#2 PSEUDOCODIGO DE: EXTRAI_DOCUMENTACAO
def extrai_documentacao(path_do_arquivo:str):
    documentacao = []
    #2 CRIA UM CONJUNTO VAZIO A
    with open(path_do_arquivo,'r',encoding='utf-8') as arquivo:
        #2 ABRE O ARQUIVO
        arquivo_str = arquivo.read()
        #2 FAZ A LEITURA DO ARQUIVO
        documentacao = [tupla[0] for tupla in re.findall(REGEX_NIVEIS_DE_DOCUMENTACAO,arquivo_str)]
        #2 VARRE O ARQUIVO LIDO BUSCANDO POR DOCUMENTACOES
        #2 CASO SEJA UMA DOCUMENTACAO, ADICIONA AO CONJUNTO A
    return documentacao
    #2 RETORNA O CONJUNTO A
#2]

#3[
#3 DETALHES DE: EXTRAI_DOCUMENTACAO
#3 RE.FINDALL NÃO RETORNA MATCHS QUE SE SOBREPOEM
#3 O MATCH EM REGEX É UM TUPLA COM VALOR E NÚMERO DO MATCH, EXTRAIMOS APENAS O VALOR 
#3]

#1[
#1 ROTINA: FORMATA_DOCUMENTACAO
#1 FINALIDADE: ORGANIZA UM CONJUNTO DE DOCUMENTACOES EM UM CONJUNTO DE PARES (RÓTULO,VALOR) PARA CADA NÍVEL DE DOCUMENTACAO FEITA.
#1 ENTRADAS: CONJUNTO COM TODAS AS DOCUMENTACOES
#1 DEPENDENCIAS: NENHUMA
#1 CHAMADO POR: AGREGA_DOCUMENTACOES
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: FORMATA_DOCUMENTACAO
def formata_documentacao(lista_de_documentacoes:list):
    documentacao_formatada = []
    #2 CRIA UM CONJUNTO VAZIO A
    for documentacao in lista_de_documentacoes:
        #2 VARRE O CONJUNTO DE DOCUMENTACOES
        dicionario = {}
        for linha in documentacao.split('\n'):
            #2 VARRE O CONJUNTO DE LINHAS DE CADA DOCUMENTACAO
            pula_linha = True
            for nivel in SINTAXE:
                if nivel in linha:
                    linha = linha.replace(nivel,'')
                    pula_linha = False
                    break
            if pula_linha or linha == "":
                continue
            #2 SE NÃO FOR COMENTÁRIO DE AUTO-DOCUMENTACAO, PASSA PARA O PRÓXIMO ELEMENTO DO CONJUNTO DE LINHAS
            elif SEPARADOR in linha:
                #2 SE FOR COMENTÁRIO DE AUTO-DOCUMENTACAO, ADICIONA AO CONJUNTO A O PAR (RÓTULO,VALOR)
                linha = linha.split(SEPARADOR)
                rotulo = linha[0].strip()
                valor = linha[1].strip()
                if rotulo in PONTEIROS:
                    dicionario[rotulo] = [item.strip() for item in valor.split(',')]
                else:
                    dicionario[rotulo] = valor
            elif dicionario.get(COMENTARIO) == None:
                dicionario[COMENTARIO] = [linha]
            else:
                dicionario[COMENTARIO].append(linha)
        documentacao_formatada.append(dicionario)
    return documentacao_formatada
    #2 RETORNA O CONJUNTO A
#2]

#3[
#3 DETALHES DE: FORMATA_DOCUMENTACAO
#3 A REMOÇÃO DA PARTE QUE INDICA O NÍVEL DA DOCUMENTACAO É FEITA IGNORANDO OS 2 PRIMEIROS CARACTERES
#3 SE HOUVER UM SEPARADOR, UTILIZO STRIP() PARA REMOVER ESPAÇOS LATERAIS DE UMA STRING
#3 SE NÃO HÁ SEPARADOR, NAO USO O STRIP() PARA NÃO REMOVER A IDENTAÇÃO
#3]

#1[
#1 ROTINA: ESTRUTURA_DOCUMENTACAO
#1 FINALIDADE: CONTRÓI UM CONJUNTO COM OS METADADOS E AS ROTINAS, PODENDO ACESSAR CADA UM DOS NÍVEIS
#1 ENTRADAS: CONJUNTO DAS DOCUMENTACOES FORMATADAS
#1 DEPENDENCIAS: COPY
#1 CHAMADO POR: AGREGA_DOCUMENTACOES
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: ESTRUTURA_DOCUMENTACAO
def estrutura_documentacao(documentacao_formatada:list):
    estruturada = copy.deepcopy(TEMPLATE_ESTRUTURADA_1)
    #2 CRIA UM CONJUNTO VAZIO A
    for doc_dict in documentacao_formatada:
        #2 VARRE OS ELEMENTOS DO CONJUNTO DE DOCUMENTACOES FORMATADAS
        chaves = list(doc_dict.keys())
        if chaves[0] in IDENTIFICADORES:
            if estruturada[ROTINAS].get(doc_dict[chaves[0]]) == None:
                estruturada[ROTINAS][doc_dict[chaves[0]]] = copy.deepcopy(TEMPLATE_ESTRUTURADA_2)
            estruturada[ROTINAS][doc_dict[chaves[0]]][PEGA_NIVEL[''.join(chaves)]] = doc_dict
        else:
            estruturada[METADADOS] = doc_dict
            #2 DEFINE O NÍVEL COM BASE NOS NOMES DOS CAMPOS
            #2 INSERE O PAR (RÓTULO, VALOR) DE UM DADO NÍVEL NO CONJUNTO A        
    return estruturada
    #2 RETORNA O CONJUNTO A
#2]

#3[
#3 DETALHES DE: ESTRUTURA_DOCUMENTACAO
#3 É NECESSÁRIO QUE COPY.DEEPCOPY() SEJA USADO, PORQUE A CÓPIA NATIVA DO PYTHON É APLICADA A AMBAS AS REFERêNCIAS SE HOUVEM LISTAS ENCADEADAS
#3 CASO ALGUM RÓTULO ESTEJA ESCRITO ERRADO, O EXTRATOR VAI DAR ERRO
#3 PARA PEGAR O NIVEL, EU TRANSFORMO A LISTA DE ROTULOS EM UMA ÚNICA STRING USANDO ''.JOIN(ROTULOS)
#3 APÓS CRIAR A STRING, FAÇO UMA BUSCA PELO PAR <CHAVE,VALOR> NO DICIONARIO PEGA_NIVEL DEFINIDO EM CONSTANTES.PY
#3]

#1[
#1 ROTINA: AGREGA_DOCUMENTACOES
#1 FINALIDADE: VERIFICA SE O PATH FORNECIDO É UMA PASTA OU UM ARQUIVO, MUDANDO O COMPORTAMENTO DE ACORDO
#1 ENTRADAS: PATH
#1 DEPENDENCIAS: OS
#1 CHAMADO POR: CONSTROI_DOCUMENTACOES
#1 CHAMA: ESTRUTURA_DOCUMENTACAO, FORMATA_DOCUMENTACAO, EXTRAI_DOCUMENTACAO, PEGA_ARQUIVOS
#1]

#2[
#2 PSEUDOCODIGO DE: AGREGA_DOCUMENTACOES
def agrega_documentacoes(path:str):
    agregadas = {}
    #2 CRIA UM CONJUNTO VAZIO A
    if os.path.isfile(path):
        print(f' [+] Extraindo documentação do arquivo com PATH: {arquivo}, sob o nome de {os.path.basename(arquivo)}') 
        agregadas[os.path.basename(path)] = estrutura_documentacao(formata_documentacao(extrai_documentacao(path)))
        #2 SE O PATH É UM ARQUIVO, ENTÃO INSERE EM A O PAR (NOME_DO_ARQUIVO, DOCUMENTACAO ESTRUTURADA)
    elif os.path.isdir(path):
        #2 SE O PATH É UMA PASTA, ENTÃO VARRE OS ELEMENTOS DO CONJUNTO DE ARQUIVOS NA PASTA
        for arquivo in pega_arquivos(path):
            print(f' [+] Extraindo documentação do PATH: {arquivo}, sob o nome de {os.path.basename(arquivo)}')
            agregadas[os.path.basename(arquivo)] = estrutura_documentacao(formata_documentacao(extrai_documentacao(arquivo)))
            #2 INSERE EM A O PAR (NOME_DO_ARQUIVO, DOCUMENTACAO ESTRUTURADA)
    else:
        print(f' [-] PATH não identificado como arquivo ou diretório: {path}')
    return agregadas
    #2 RETORNA O CONJUNTO A
#2]

#3[
#3 DETALHES DE: AGREGA_DOCUMENTACOES
#3 CASO NÃO SEJA UM ARQUIVO OU UMA PASTA, O PROGRAMA MOSTRA UMA MENSAGEM DE ERRO
#3]

#1[
#1 ROTINA: CONSTROI_DOCUMENTACOES
#1 FINALIDADE: ACOPLAR TODAS AS ROTINAS CHAMADAS
#1 ENTRADAS: PATH 
#1 DEPENDENCIAS: OS, JSON
#1 CHAMADO POR: MAIN
#1 CHAMA: AGREGA_DOCUMENTACOES
#1]

#2[
#2 PSEUDOCODIGO DE: CONSTROI_DOCUMENTACOES 
def constroi_documentacoes(path:str):
    documentacoes = agrega_documentacoes(path)
    #2 CRIA O CONJUNTO DE PARES (ARQUIVOS, DOCUMENTACOES)
    json.dump(documentacoes, open(PATH_DOCUMENTACAO,'w',encoding='utf8'))
    #2 SALVA O CONJUNTO EM UM ARQUIVO JSON
#2]

#3[
#3 DETALHES DE: CONSTROI_DOCUMENTACOES
#3 PATH DO SALVAMENTO ESTÁ EM CONSTANTS.PY
#3]

#1[
#1 ROTINA: MAIN
#1 FINALIDADE: RECEBER O PATH E CHAMAR A ROTINA PARA A CONSTRUÇÃO DA DOCUMENTAÇÃO
#1 ENTRADAS: PATH
#1 DEPENDENCIAS: SYS
#1 CHAMADO POR: 
#1 CHAMA: CONSTROI_DOCUMENTACOES
#1]
    
#2[
#2 PSEUDOCODIGO DE: MAIN
def main():
    if len(sys.argv) == 2:
        #2 SE FOR FORNECIDO O PATH, CHAMA A ROTINA PARA CONSTRUÇÃO DA DOCUMENTAÇÃO
        constroi_documentacoes(sys.argv[1])
    else:
        #2 SE NÃO FOR FORNECIDO O PATH, MOSTRA UMA MENSAGEM DE ERRO
        print(f' [-] MODO DE USO: py extrator_de_documentacao.py <PATH>')
#2]
        
#3[
#3 DETALHES DE: MAIN
#3 CASO SEJA NECESSÁRIO INFORMAR O FORMATO DO ARQUIVO, BASTA MUDAR A MAIN, CONSTROI_DOCUMENTACOES E AGREGA_DOCUMENTACOES
#3]
        
main()