import os
import re
import json
from constantes import *


#1[
#1 ROTINA: PEGA_ARQUIVOS
#1 FINALIDADE: RETORNA UMA LISTA COM O PATH DE TODOS OS ARQUIVOS DE UMA PASTA
#1 ENTRADAS: PATH DA PASTA
#1 DEPENDENCIAS: OS
#1 CHAMADO POR: 
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: PEGA_ARQUIVOS
def pega_arquivos(path:str):
    arquivos = []
    #2 INICIALIZA UMA LISTA
    for arquivo in os.listdir(path):
        #2 ITERA POR CADA ITEM DA PASTA
        arquivos.append(os.path.join(path,arquivo))
        #2 ADICIONA O SUFIXO DO PATH PARA CADA ITEM
        #2 ADICIONA ÚLTIMA POSIÇÃO DA LISTA
    return arquivos
    #2 RETORNA A LISTA
#2]
    
#3[
#3 DETALHES DE: PEGA_ARQUIVOS
#3 LISTAS EM PYTHON SÃO IMPLEMENTADAS COMO PILHAS, ENTÃO AS INSERÇÕES SÃO INSERIDAS NO FIM DA LISTA
#3 OS.LISTDIR RETORNA OS ARQUIVOS EM UMA ORDEM ARBITRÁRIA
#3]

#1[
#1 ROTINA: EXTRAI_DOCUMENTACAO
#1 FINALIDADE: RETORNA UMA LISTA COM TODAS AS DOCUMENTAÇÕES, DE TODOS OS NÍVEIS, DE UM ARQUIVO
#1 ENTRADAS: PATH DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: 
#1 CHAMA: 
#1]
    
#2[
#2 PSEUDOCODIGO DE: EXTRAI_DOCUMENTACAO
def extrai_documentacao(path_do_arquivo:str):
    documentacao = []
    #2 INICIALIZA A LISTA
    with open(path_do_arquivo,'r',encoding='utf-8') as arquivo:
        #2 ABRE O ARQUIVO
        arquivo_str = arquivo.read()
        #2 FAZ A LEITURA DO ARQUIVO
        documentacao = [tupla[0] for tupla in re.findall(REGEX_NIVEIS_DE_DOCUMENTACAO,arquivo_str)]
        #2 PROCURA PELO PADRÃO USANDO EXPRESSÕES REGULARES
        #2 INSERE OS MATCHS NA LISTA
    return documentacao
    #2 RETORNA A LISTA
#2]

#3[
#3 DETALHES DE: EXTRAI_DOCUMENTACAO
#3 RE.FINDALL NÃO RETORNA MATCHS QUE SE SOBREPOEM
#3 O MATCH EM REGEX É UM TUPLA COM VALOR E NÚMERO DO MATCH, EXTRAIMOS APENAS O VALOR 
#3]

#1[
#1 ROTINA: FORMATA_DOCUMENTACAO
#1 FINALIDADE: RETORNA UMA LISTA DE DICIONÁRIOS, ORGANIZANDO UMA LISTA DE DOCUMENTACOES EM UMA LISTA DE <CHAVE,VALOR> PARA CADA DOCUMENTACAO FEITA
#1 ENTRADAS: LISTA COM TODAS AS DOCUMENTACOES
#1 DEPENDENCIAS: NENHUMA
#1 CHAMADO POR: 
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: FORMATA_DOCUMENTACAO
def formata_documentacao(lista_de_documentacoes:list):
    documentacao_formatada = []
    #2 INICIALIZA A LISTA DE DICIONÁRIOS
    for documentacao in lista_de_documentacoes:
        #2 PARA CADA DOCUMENTACAO NA LISTA DE DOCUMENTACOES
        dicionario = {}
        #2 INICIALIZA UM DICIONARIO TEMPORARIO
        for linha in documentacao.split('\n'):
            #2 SEPARA UM BLOCO DE DOCUMENTACAO EM LINHAS DE DOCUMENTACAO
            #2 ITERA EM CADA LINHA
            pula_linha = True
            for nivel in SINTAXE:
                if nivel in linha:
                    linha = linha.replace(nivel,'')
                    pula_linha = False
                    break
            if pula_linha or linha == "":
                continue
            #2 SE NÃO FOR COMENTÁRIO DE AUTO-DOCUMENTACAO, AVANÇA PARA A PROXIMA LINHA
            #2 REMOVE A PARTE QUE INDICA O NÍVEL
            #2 SE A LINHA FOR VAZIA, IGNORA
            elif SEPARADOR in linha:
                #2 SE HOUVER UM SEPARADOR NA LINHA, ADICIONA NO DICIONARIO
                linha = linha.split(SEPARADOR)
                dicionario[linha[0].strip()] = linha[1].strip()
            elif dicionario.get(COMENTARIO) == None:
                dicionario[COMENTARIO] = [linha]
            else:
                dicionario[COMENTARIO].append(linha)
            #2 SE NAO HOUVER SEPARADOR, ADICIONA COMO COMENTARIO
        documentacao_formatada.append(dicionario)
        #2 ADICIONA O DICIONARIO NA LISTA
    return documentacao_formatada
    #2 RETORNA A LISTA DE DICIONÁRIOS
#2]

#3[
#3 DETALHES DE: FORMATA_DOCUMENTACAO
#3 A REMOÇÃO DA PARTE QUE INDICA O NÍVEL DA DOCUMENTACAO É FEITA IGNORANDO OS 2 PRIMEIROS CARACTERES
#3 SE HOUVER UM SEPARADOR, UTILIZO STRIP() PARA REMOVER ESPAÇOS LATERAIS DE UMA STRING
#3 SE NÃO HÁ SEPARADOR, NAO USO O STRIP() PARA NÃO REMOVER A IDENTAÇÃO
#3]

#1[
#1 ROTINA: ESTRUTURA_DOCUMENTACAO
#1 FINALIDADE: RETORNA UM DICIONARIO COM OS METADADOS E AS ROTINAS, PODENDO ACESSAR CADA UM DOS NÍVEIS
#1 ENTRADAS: LISTA COM TODAS AS DOCUMENTACOES FORMATADAS
#1 DEPENDENCIAS: NENHUMA
#1 CHAMADO POR: 
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: ESTRUTURA_DOCUMENTACAO
def estrutura_documentacao(documentacao_formatada:list):
    estruturada = TEMPLATE_ESTRUTURADA_1.copy()
    #2 INICIALIZA O DICIONARIO COM A ESTRUTURA DE METADADOS E ROTINAS
    for doc_dict in documentacao_formatada:
        #2 PARA CADA DICIONARIO NA LISTA DE DICIONARIOS FORMATADA
        chaves = list(doc_dict.keys())
        if chaves[0] in IDENTIFICADORES:
            #2 SE FOR IDENTIFICADOR
            if estruturada[ROTINAS].get(doc_dict[chaves[0]]) == None:
                estruturada[ROTINAS][doc_dict[chaves[0]]] = TEMPLATE_ESTRUTURADA_2.copy()
                #2 INICIALIZA A ESTRUTURA DOS NIVEIS, CASO NAO TENHA SIDO INICIALIZADA AINDA
            estruturada[ROTINAS][doc_dict[chaves[0]]][PEGA_NIVEL[''.join(chaves)]] = doc_dict
            #2 DEFINE O NÍVEL COM BASE NOS NOMES DOS CAMPOS
            #2 INSERE NO RESPECTIVO NÍVEL
        else:
            #2 SE NÃO FOR IDENTIFICADOR, INSERE COMO METADADO
            estruturada[METADADOS] = doc_dict        
    return estruturada
    #2 RETORNA O DICIONARIO
#2]

#3[
#3 DETALHES DE: ESTRUTURA_DOCUMENTACAO
#3 CASO ALGUM RÓTULO ESTEJA ESCRITO ERRADO, O EXTRATOR VAI DAR ERRO
#3 PARA PEGAR O NIVEL, EU TRANSFORMO A LISTA DE ROTULOS EM UMA ÚNICA STRING USANDO ''.JOIN(ROTULOS)
#3 APÓS CRIAR A STRING, FAÇO UMA BUSCA PELO PAR <CHAVE,VALOR> NO DICIONARIO PEGA_NIVEL DEFINIDO EM CONSTANTES.PY
#3]

def agrega_documentacoes(path:str):
    agregadas = {}
    if os.path.isfile(path): 
        agregadas[os.path.basename(path)] = estrutura_documentacao(formata_documentacao(extrai_documentacao(path)))
    else:
        for arquivo in pega_arquivos(path):
            agregadas[os.path.basename(arquivo)] = estrutura_documentacao(formata_documentacao(extrai_documentacao(arquivo)))
    return agregadas


'''
inicializa um dicionario de documentacoes estruturadas(LDE)
se for uma pasta, entao
    para cada arquivo
        insere o arquivo em LDE como chave
        insere a documentacao estruturado do arquivo como valor na LDE
senao
    insere o arquivo em LDE como chave
    insere a documentacao estruturado do arquivo como valor na LDE
retorna LDE -> salva no formato json
'''
if __name__ == '__main__':
    path = input(FRASE_INPUT_PATH)
    #f = formata_documentacao(extrai_documentacao(pega_arquivos(path)[0]))
    json.dump(agrega_documentacoes(path),open('a.json','w'))
