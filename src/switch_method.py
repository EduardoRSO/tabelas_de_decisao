import sys
import re
from functools import reduce
import operator


def le_tds(path:str):
    tds = re.findall(r'(#TD decision table.*?#TD end table)',open(path,'r').read(), re.DOTALL)
    return tds

def processa_tds(tds_nao_formatadas:list):
    tds_estruturadas = []
    for td_nao_formatda in tds_nao_formatadas:
        td = {'sets': [], 'conditions': [], 'actions': []}
        estado_atual = ''
        for linha in td_nao_formatda.split('\n'):
            if 'decision table' in linha:
                continue
            elif 'sets' in linha:
                estado_atual = 'sets'
                continue
            elif 'conditions' in linha:
                estado_atual = 'conditions'
                continue
            elif 'actions' in linha:
                estado_atual = 'actions'
                continue
            elif 'end table' in linha:
                continue
            else:
                td[estado_atual].append(linha.split()[1:])
        tds_estruturadas.append(td)
    return tds_estruturadas

def trata_condicao(td:dict, condicao:str,entrada:str):
    # 3 <= number <= 7
    # number in iteravel
    # string in iteravel
    # variavel == valor
    if entrada in [nome_e_definicao_dos_conjuntos[0] for nome_e_definicao_dos_conjuntos in td['sets']]:
        return f'{condicao} in {entrada}'
    else:
        return f'{condicao} == {entrada}'

def trata_acao(td:dict, M:int):
    #Como determinar qual é a sequencia de ações?
    #Há uma ordenação, mas ainda não enxerguei como isso implica que sempre
    #é verdade que se I == i, então Ações -> Acões da regra R_i
    return f'A_{M}'

def gera_codigo(td:dict):
    print(td)
    codigo_gerado = "\n".join([f'I_{index} = 0 #Inicialização do auxiliar da condição {condicao}' for index, condicao in enumerate(td['conditions'])])+'\nI   = 0 #Inicialização do número da regra\n'
    for index, linha_de_condicao in enumerate(td['conditions']):
        C = set(['-'])
        n_i = 0
        condicao = linha_de_condicao[0]
        entradas = linha_de_condicao[1:]
        for C_ij in entradas:
            if C_ij not in C:
                n_i +=1
                c_ij = C_ij
                if len(C) == 1:
                    codigo_gerado += f'if {trata_condicao(td, condicao, c_ij)}:\n    I_{index} = 0\n'
                else:
                    codigo_gerado += f'elif {trata_condicao(td, condicao, c_ij)}:\n    I_{index} = {n_i-1}\n'
                C.add(c_ij)
    
    entradas_por_condicao = [len(set(condicao))-1 for condicao in td['conditions']] 
    codigo_gerado += f"I = {'+'.join(['*'.join(['1']+[f'{entradas_por_condicao[j]}' for j in range(i+1,len(td['conditions']))])+f'*I_{i}' for i in range(len(td['conditions']))])}\n"
    codigo_gerado += f'match I:\n'
    for M in range(reduce(operator.mul, entradas_por_condicao, 1)):
        codigo_gerado += f'    case {M}:\n        {trata_acao(td,M)}\n'
    codigo_gerado += f'    case _:\n        exit()\n'    
    return codigo_gerado

    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Uso: python switch_method.py <PATH ARQUIVO> <PATH OUTPUT>')
    else:
        tds = le_tds(sys.argv[1])
        if tds:
            for td in processa_tds(tds):
                codigo_gerado = gera_codigo(td)
                print(codigo_gerado)
        else:
            print('O arquivo não possui TDS dentro dele')    