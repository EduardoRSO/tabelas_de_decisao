#1[
#1 TITULO: EXTRATOR DE TD TRADUZIDA
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 24/02/2024
#1 VERSAO: 1
#1 FINALIDADE: GERAR UMA ESTRUTURA DE DADOS PARA O ACESSO EM TEMPO CONSTANTE PARA OS COMPONENTES DE UMA TD
#1 ENTRADAS: ARQUIVO QUE CONTEM UMA TD TRADUZIDA
#1 SAIDAS: ESTRUTURA DE DADOS
#1 ROTINAS CHAMADAS: 
#1]

import re
import sys
from constantes import *

#1[
#1 ROTINA: PEGA_ARQUIVO
#1 FINALIDADE: RETORNA O ARQUIVO LIDO
#1 ENTRADAS: PATH DO ARQUIVO
#1 DEPENDENCIAS: 
#1 CHAMADO POR: CONSTROI_TDS_ESTRUTURADAS
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: PEGA_ARQUIVO
def pega_arquivo(path:str):
    #2 ABRE O ARQUIVO NO MODO LEITURA
    return open(path,'r',encoding='utf-8').read()
    #2 RETORNA UMA STRING DE TODO O CONTEUDO DO ARQUIVO
#2]
    
#3[
#3 DETALHES DE: PEGA_ARQUIVO
#3 O ENCODING UTILIZADO FOI UTF-8
#3]


#1[
#1 ROTINA: EXTRAI_TD_TRADUZIDA
#1 FINALIDADE: CRIA UM CONJUNTO COM TODAS AS TDS TRADUZIDAS EM UM PROGRAMA
#1 ENTRADAS: UM ARQUIVO LIDO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: CONSTROI_TDS_ESTRUTURADAS
#1 CHAMA: 
#1]
    
#2[
#2 PSEUDOCODIGO DE: EXTRAI_TD_TRADUZIDA
def extrai_td_traduzida(arquivo_lido:str):
    #2 UTILIZA EXPRESSÕES REGULARES PARA VARRER O CONJUNTO
    #2 PARA CADA TUPLA QUE POSSUA O PADRÃO FORNECIDO
    return [tupla[0] for tupla in re.findall(REGEX_TD_TRADUZIDA,arquivo_lido)]
    #2 RETORNA UMA LISTA COM APENAS O TEXTO DE CADA TD
#2]

#3[
#3 DETALHES DE: EXTRAI_TD_TRADUZIDA
#3 OS ITENS NÃO SE SOBREPOEM
#3]

#1[
#1 ROTINA: FORMATA_TD_TRADUZIDA
#1 FINALIDADE: CONSTROÍ UM CONJUNTO DE PARES <RÓTULO,VALOR> PARA CADA TD, DE TAL MODO QUE SEJA POSSÍVEL ACESSAR CADA UM DOS COMPONENTES EM O(1)
#1 ENTRADAS: LISTA DE TDS TRADUZIDAS
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: CONSTROI_TDS_ESTRUTURADAS
#1 CHAMA: AUXILIAR_DE_FORMATAÇÃO
#1]
    
#2[
#2 PSEUDOCODIGO DE: FORMATA_TD_TRADUZIDA
def formata_td_traduzida(lista_de_tds_traduzidas:list):
    #2 DEFINE UMA FUNÇÃO AUXILIAR QUE RECEBE O PADRÃO EM REGEX, A STRING DA TD E O ROTULO
    def auxiliar_de_formatacao(regex, td:str, descricao:str):
        #2 UTILIZA UM TRATAMENTO DE EXCEÇÃO
        try:
            #2 VARRE A TD UTILIZANDO O PADRAO
            tmp = re.findall(regex,td)
            #2 VERIFICA SE O QUE FOI RETORNADO PELO RE.FINDALL() É UMA LISTA
            if isinstance(tmp,list):
                #2 VERIFICA SE DENTRO DA LISTA EXISTE UMA TUPLA
                if isinstance(tmp[0],tuple):
                    #2 VERIFICA SE A TUPLA TEM TAMANHO MAIOR QUE UM
                    if len(tmp[0]) > 1:
                        return [re.sub(r'\s*','',elemento) for elemento in tmp[0][0].split('\n')]
                        #2 ACESSA APENAS A PRIMEIRA TUPLA
                        #2 CRIA UM CONJUNTO AO SEPARAR O CONTEUDO PELAS QUEBRAS DE LINHA
                        #2 PARA CADA ITEM DO CONJUNTO, REMOVE OS ESPAÇOS VAZIOS
                        #2 RETORNA O CONJUNTO
                    else:
                    #2 SE O TAMANHO FOR UM
                        return [re.sub(r'\s*','',elemento) for elemento in tmp[0].split('\n')]
                        #2 CRIA UM CONJUNTO AO SEPARAR O CONTEUDO PELAS QUEBRAS DE LINHA
                        #2 PARA CADA ITEM DO CONJUNTO, REMOVE OS ESPAÇOS VAZIOS
                        #2 RETORNA O CONJUNTO
                return tmp
        except Exception as e:
            #2 SE NÃO FOR UMA LISTA, RETORNA UMA STRING VAZIA
            print(f' [-] Erro na extração de {descricao}: {e}')
            return ""

    #2 CRIA UM CONJUNTO VAZIOS DE TDS FORMATADAS
    tds_formatadas = {}
    #2 VARRE O CONJUNTO DE TDS TARDUZIDAS
    for index, td in enumerate(lista_de_tds_traduzidas):
        #2 INSERE CADA TD NO CONJUNTO DE TDS FORMATDAS COM <ROTULO,VALOR> 
        tds_formatadas[index] = {
            "DECISION TABLE": auxiliar_de_formatacao(REGEX_EXTRAI_NOME,td,"NOME"),
            "PREPARATION": auxiliar_de_formatacao(REGEX_EXTRAI_PREPARACAO,td,"PREPARACAO"),
            "SETS": auxiliar_de_formatacao(REGEX_EXTRAI_CONJUNTOS,td,"CONJUNTO"),
            "CONDITIONS": auxiliar_de_formatacao(REGEX_EXTRAI_CONDICOES,td,"CONDICOES"),
            "ACTIONS": auxiliar_de_formatacao(REGEX_EXTRAI_ACOES,td,"ACOES")
        }
    #2 RETORNA O CONJUNTO DE TDS FORMATADAS
    return tds_formatadas
#2]

#3[
#3 DETALHES DE: FORMATA_TD_TRADUZIDA
#3 EXISTE UM REGEX PARA EXTRAIR CADA RÓTULO DE UMA TD E CASO ALGO SEJA ALTERADO ELE DEVE SER ESTUDADO NOVAMENTE EM CONSTANTES.PY
#3]

#1[
#1 ROTINA: ESTRUTURA_TD_TRADUZIDA
#1 FINALIDADE: ESTRUTURA UMA TD FORMATADA PARA QUE CADA VALOR SEJA ACESSÍVEL EM O(1)
#1 ENTRADAS: UM CONJUNTO DE PARES (ÍNDICE DA TD, TD), TAL QUE TD := {(RÓTULO, VALOR)} PARA CADA RÓTULO EM {DECISION TABLE, PREPARATION, SETS, CONDITIONS, ACTIONS}
#1 DEPENDENCIAS: NENHUMA
#1 CHAMADO POR: CONSTROI_TDS_ESTRUTURADAS
#1 CHAMA: AUXILIAR_DE_ESTRUTURAÇÃO
#1]

#2[
#2 PSEUDOCODIGO DE: ESTRUTURA_TD_TRADUZIDA
def estrutura_td_traduzida(tds_formatadas:dict):

    #2 DEFINE UMA FUNÇÃO AUXILIAR QUE RECEBE UMA TD E O RÓTULO A SER ESTRUTURADO
    def auxiliar_de_estruturacao(td:dict, rotulo:str):
        #2 ACESSA O VALOR DO RÓTULO
        lista_formatada = td[rotulo]
        #2 VERIFICA SE É UMA LISTA
        if isinstance(lista_formatada,list):
            #2 VERIFICA SE O RÓTULO É DECISION TABLE
            if rotulo == 'DECISION TABLE':
                #2 RETORNA A PRIMEIRA POSIÇÃO DA LISTA
                return lista_formatada[0]
            #2 SE NÃO FOR DECISION TABLE
            else:
                #2 CRIA UM CONJUNTO VAZIO
                tmp = {}
                #2 VARRE OS ITENS NO RÓTULO ATUAL
                for index, item in enumerate(lista_formatada):
                    #2 SEPARA CADA ITEM EM NOME E SUB VALORES, OBTENDO O INDEX DE CADA ITEM
                    item = item.split(DESCRICAO_TD)
                    #2 INSERE O NOME DO RÓTULO NO INDEX DO ITEM ATUAL
                    tmp[index] = {
                        "ROTULO": item[0]
                    }
                    #2 VERIFICA SE APÓS SEPARAR POR DESCRICAO_TD O TAMANHO É MAIOR QUE UM
                    if len(item) > 1:
                        #2 VARRE OS SUB VALORES, OBTENDO O SUB INDEX DE CADA UM
                        for subindex, subitem in enumerate(item[1].split(SEPARADOR)[:-1]):
                            #2 INSERE O VALOR DE CADA SUBITEM, PRESERVANDO O SUBINDEX E O VALOR DO SUBITEM 
                            tmp[index][subindex] = subitem
                    #2 CASO NÃO SEJA, INSERE NA PRIMEIRA POSIÇÃO O MESMO VALOR DO RÓTULO
                    else:
                        tmp[index][0] = item[0]
                return tmp    
        #2 SE NÃO FOR UMA LISTA
        else:
            #2 RETORNA O VALOR SEM ALTERAÇÕES
            return lista_formatada

    #2 PARA CADA TD FORMATADA
    for index_td in tds_formatadas.keys():
        #2 PARA CADA ROTULO EM CADA TD FORMATDA
        for rotulo in tds_formatadas[index_td].keys():
            #2 ESTRUTURA CADA ROTULO UTILIZANDO A FUNÇÃO AUXILIAR
            tds_formatadas[index_td][rotulo] = auxiliar_de_estruturacao(tds_formatadas[index_td],rotulo)
    #2 RETORNA A TD ESTRUTURADA
    return tds_formatadas
#2]

#3[
#3 DETALHES DE: ESTRUTURA_TD_TRADUZIDA
#3 É POSSÍVEL MODIFICAR O SEPARADOR DOS VALORES DA TD EM CONSTANTES.PY
#3]

#1[
#1 ROTINA: CONSTROI_TDS_ESTRUTURADAS
#1 FINALIDADE: ACOPLAR TODAS AS ROTINAS CHAMADAS
#1 ENTRADAS: O CAMINHO DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: MAIN
#1 CHAMA: PEGA_ARQUIVO, EXTRAI_TD_TRADUZIDA, FORMATADA_TD_TRADUZIDA, ESTRUTURA_TD_TRADUZIDA
#1]

#2[
#2 PSEUDOCODIGO DE: CONSTROI_TDS_ESTRUTURADAS
def constroi_tds_estruturadas(path:str):
    #2 FAZ A CHAMADA EM CADEIA DAS ROTINAS
    return estrutura_td_traduzida(formata_td_traduzida(extrai_td_traduzida(pega_arquivo(path))))
    #2 RETORNA A TD ESTRUTURADA 
#2]

#3[
#3 DETALHES DE: CONSTROI_TDS_ESTRUTURADAS
#3 O DICIONÁRIO RETORNADA É DO TIPO ((indice_da_td,(td)), tal que a td é dada por (rotulo,((indice_do_valor,valor)))
#3]

#1[
#1 ROTINA: MAIN
#1 FINALIDADE: RECEBER O PATH E CHAMAR A ROTINA PARA A CONSTRUÇÃO DA TD TRADUZIDA
#1 ENTRADAS: PATH
#1 DEPENDENCIAS: SYS
#1 CHAMADO POR: 
#1 CHAMA: CONSTROI_TDS_ESTRUTURADAS
#1]
    
#2[
#2 PSEUDOCODIGO DE: MAIN
def main():
    if len(sys.argv) == 2:
        #2 SE FOR FORNECIDO O PATH, CHAMA A ROTINA PARA CONSTRUÇÃO DAS TDS ESTRUTURADAS
        print(constroi_tds_estruturadas(sys.argv[1]))
    else:
        #2 SE NÃO FOR FORNECIDO O PATH, MOSTRA UMA MENSAGEM DE ERRO
        print(f' [-] MODO DE USO: py extrator_de_td_traduzida.py <PATH>')
#2]
        
#3[
#3 DETALHES DE: MAIN
#3]
        
#main()