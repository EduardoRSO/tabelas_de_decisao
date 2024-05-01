#1[
#1 TITULO: EXTRATOR DE DOCUMENTACAO
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 01/05/2024
#1 VERSAO: 2
#1 FINALIDADE: GERAR RELATÓRIO CONTENDO A DOCUMENTAÇÃO DE DETERMINADO PROGRAMA
#1 ENTRADAS: ARQUIVO AUTO-DOCUMENTADO COM A SINTAXE ESPECIFICADA
#1 SAIDAS: ARQUIVO PDF COM A DOCUMENTAÇÃO
#1 ROTINAS CHAMADAS: EXTRAI_NIVEL_(1-3), CONSTROI_PDF
#1]

import re
import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

NV_1 = r'#1.*'
NV_2 = r'#2.*'
NV_3 = r'#3.*'

#1[
#1 ROTINA: EXTRAI_NIVEL_3
#1 FINALIDADE: EXTRAI AS DOCUMENTACOES DE NIVEL 1,2 E 3
#1 ENTRADAS: TEXTO DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: MAIN
#1 CHAMA: RE.FINDALL
#1]

#2[
#2 PSEUDOCODIGO DE: EXTRAI_NIVEL_3
def extrai_nivel_3(arquivo:str):
#2  CONSTROI UM CONJUNTO
#2  VARRE O ARQUIVO
#2  SE PERTENCE AO NIVEL 1,2 OU 3, INSERE NO CONJUNTO
#2  CASO CONTRÁRIO, IGNORA
#2  RETORNA O CONJUNTO
    return re.findall(NV_1+r'|'+NV_2+r'|'+NV_3,arquivo)
#2]


#1[
#1 ROTINA: EXTRAI_NIVEL_2
#1 FINALIDADE: EXTRAI AS DOCUMENTACOES DE NIVEL 1 E 2
#1 ENTRADAS: TEXTO DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: MAIN
#1 CHAMA: RE.FINDALL
#1]

#2[
#2 PSEUDOCODIGO DE: EXTRAI_NIVEL_2
def extrai_nivel_2(arquivo:str):
#2  CONSTROI UM CONJUNTO
#2  VARRE O ARQUIVO
#2  SE PERTENCE AO NIVEL 1 OU 2, INSERE NO CONJUNTO
#2  CASO CONTRÁRIO, IGNORA
#2  RETORNA O CONJUNTO
    return re.findall(NV_1+r'|'+NV_2,arquivo)
#2]


#1[
#1 ROTINA: EXTRAI_NIVEL_1
#1 FINALIDADE: EXTRAI AS DOCUMENTACOES DE NIVEL 1
#1 ENTRADAS: TEXTO DO ARQUIVO
#1 DEPENDENCIAS: RE
#1 CHAMADO POR: MAIN
#1 CHAMA: RE.FINDALL
#1]

#2[
#2 PSEUDOCODIGO DE: EXTRAI_NIVEL_1
def extrai_nivel_1(arquivo:str):
#2  CONSTROI UM CONJUNTO
#2  VARRE O ARQUIVO
#2  SE PERTENCE AO NIVEL 1, INSERE NO CONJUNTO
#2  CASO CONTRÁRIO, IGNORA
#2  RETORNA O CONJUNTO
    return re.findall(NV_1,arquivo)
#1]


#1[
#1 ROTINA: CONSTROI_PDF
#1 FINALIDADE: CONSTROI UM ARQUIVO EM PDF COM AS DOCUMENTACOES DE UM ARQUIVO
#1 ENTRADAS: LISTA DE DOCUMENTACOES E PATH DE SAIDA
#1 DEPENDENCIAS: REPORTLAB
#1 CHAMADO POR: MAIN
#1 CHAMA: REPORTLAB.LIB.PAGE.SIZES E REPORTLAB.PDFGEN 
#1]

#2[
#2 PSEUDOCODIGO DE: CONSTROI_PDF
def constroi_pdf(documentacao:list, path_saida:str, margem:int = 10, fonte:int = 5, titulo:str = 'DOCUMENTAÇÃO'):
#2  DEFINE UM CANVAS COM PATH DE SAIDA E TAMANHO DA PÁGINA
    c = canvas.Canvas(os.path.join(path_saida,'documentacao.pdf'), pagesize=letter)
#2  DEFINE O TAMANHO E ESTILO DA FONTE
    c.setFont("Helvetica", fonte)
#2  EXTRAI A LARGURA E ALTURA DA PÁGINA
    largura, altura = letter
#2  INSERE UM TITULO
    c.drawString((largura - c.stringWidth(titulo)) / 2, altura - 10, titulo)    
#2  GUARDA O ESPAÇO VERTICAL RESTANTE
    espaco_vertical_restante = altura - margem -10
#2  VARRE CADA LINHA DE DOCUMENTACAO
    for linha in documentacao:
#2      SE O ESPAÇO VERTICAL RESTANTE FOR MENOR QUE 50
        if espaco_vertical_restante < 50:
#2          CRIA UMA NOVA PÁGINA
            c.showPage()
#2          REDEFINE O ESPAÇO VERTICAL RESTANTE
            espaco_vertical_restante = altura-margem
#2      INSERE NA PÁGINA A LINHA NA POSIÇÃO ATUAL
        c.drawString(margem,espaco_vertical_restante,linha)
#2      SE NÃO FOR FIM DE NIVEL DE DOCUMENTACAO
#2          PULA PARA A PROXIMA LINHA
#2      CASO CONTRÁRIO, PULA 2 LINHAS
        espaco_vertical_restante -= fonte+1 if ']' not in linha else 3*fonte+1
#2  SALVA O CANVAS
    c.save()
#2]

modo_de_execucao = {
    '1': extrai_nivel_1,
    '2': extrai_nivel_2,
    '3': extrai_nivel_3
}

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Uso: python extrator_de_documentacao.py <PATH ARQUIVO> <NIVEL> <PATH OUTPUT>\n NIVEL é um valor entre 1 e 3')
    else:
        documentacao = modo_de_execucao[sys.argv[2]](open(sys.argv[1],'r').read())
        constroi_pdf(documentacao,sys.argv[3])