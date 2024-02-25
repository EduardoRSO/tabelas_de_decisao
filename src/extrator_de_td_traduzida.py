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
import os
import sys
from constantes import *

#1[
#1 ROTINA: PEGA_ARQUIVO
#1 FINALIDADE: RETORNA O ARQUIVO LIDO
#1 ENTRADAS: PATH DA PASTA
#1 DEPENDENCIAS: OS
#1 CHAMADO POR: 
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: PEGA_ARQUIVO
def pega_arquivo(path:str):
    pass
#2]
    
#3[
#3 DETALHES DE: PEGA_ARQUIVO
#3]


#1[
#1 ROTINA: EXTRAI_TD_TRADUZIDA
#1 FINALIDADE: RETORNA UM CONJUNTO COM TODAS AS TDS TRADUZIDAS
#1 ENTRADAS: PATH DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: 
#1 CHAMA: 
#1]
    
#2[
#2 PSEUDOCODIGO DE: EXTRAI_TD_TRADUZIDA
def extrai_td_traduzida(path_do_arquivo:str):
    pass
#2]

#3[
#3 DETALHES DE: EXTRAI_TD_TRADUZIDA
#3]

#1[
#1 ROTINA: FORMATA_TD_TRADUZIDA
#1 FINALIDADE: ORGANIZA UM CONJUNTO DE DTDS TRADUZIDAS EM UM CONJUNTO DE PARES (RÓTULO,VALOR).
#1 ENTRADAS: PATH DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: 
#1 CHAMA: 
#1]
    
#2[
#2 PSEUDOCODIGO DE: FORMATA_TD_TRADUZIDA
def formata_td_traduzida(lista_de_tds_traduzudas:list):
    pass
#2]

#3[
#3 DETALHES DE: FORMATA_TD_TRADUZIDA
#3]

#1[
#1 ROTINA: ESTRUTURA_TD_TRADUZIDA
#1 FINALIDADE: 
#1 ENTRADAS: 
#1 DEPENDENCIAS: 
#1 CHAMADO POR: 
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: ESTRUTURA_TD_TRADUZIDA
def estrutura_td_traduzida(documentacao_formatada:list):
    pass
#2]

#3[
#3 DETALHES DE: ESTRUTURA_TD_TRADUZIDA
#3]

#1[
#1 ROTINA: CONSTROI_TDS_ESTRUTURADAS
#1 FINALIDADE: ACOPLAR TODAS AS ROTINAS CHAMADAS
#1 ENTRADAS: 
#1 DEPENDENCIAS: 
#1 CHAMADO POR: 
#1 CHAMA: 
#1]

#2[
#2 PSEUDOCODIGO DE: CONSTROI_TDS_ESTRUTURADAS
def constroi_tds_estruturadas(path:str):
    pass
#2]

#3[
#3 DETALHES DE: CONSTROI_TDS_ESTRUTURADAS
#3]

#1[
#1 ROTINA: MAIN
#1 FINALIDADE: RECEBER O PATH E CHAMAR A ROTINA PARA A CONSTRUÇÃO DA TD TRADUZIDA
#1 ENTRADAS: PATH
#1 DEPENDENCIAS: SYS
#1 CHAMADO POR: 
#1 CHAMA: 
#1]
    
#2[
#2 PSEUDOCODIGO DE: MAIN
def main():
    if len(sys.argv) == 2:
        #2 SE FOR FORNECIDO O PATH, CHAMA A ROTINA PARA CONSTRUÇÃO DA DOCUMENTAÇÃO
        constroi_tds_estruturadas(sys.argv[1])
    else:
        #2 SE NÃO FOR FORNECIDO O PATH, MOSTRA UMA MENSAGEM DE ERRO
        print(f' [-] MODO DE USO: py extrator_de_td_traduzida.py <PATH>')
#2]
        
#3[
#3 DETALHES DE: MAIN
#3]
        
main()