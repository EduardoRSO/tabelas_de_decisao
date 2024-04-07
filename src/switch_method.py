from extrator_de_td_traduzida import constroi_tds_estruturadas
import sys
from functools import reduce
import json

def switch_method(tds_estruturadas:dict):

    json.dump(tds_estruturadas,open("a.json",'w'))

    #Adicionar exceções tendo em vista que sabemosse esse valor é uma string, inequação, equação ou conjunto
    def grava_atribuicao_de_I_if(index, C_i, R, N):
        print(f'if {R} == {C_i} then I_{index} = 0')

    def grava_atribuicao_de_I_elif(index, C_i, R, N):
        print(" "*N[index]+f'elif {R} == {C_i} then I_{index} = {N[index]-1}')

    #nesse caso é necessária fazer a ordenação proposta... não entendi como é feita do outro jeito
    def auxiliar_grava_calculo_da_regra(tabela,C,N):
        I = "I = "
        for index in range(len(N)):
            I += f"I_{index} * {reduce(lambda x,y: x*y,N[:index+1]) if index != 0 else 1} +"  
        I += "1"
        print(I)


    #nao entendi direito como é feita a atribuição de valores de I -> acoes
    def auxiliar_pega_acoes_por_indice(tabela,index):
        size = len(tds_estruturadas[tabela]["ACTIONS"].values()) -1
        return [acoes[index % size] for acoes in tds_estruturadas[tabela]["ACTIONS"].values() if acoes[index % size] != "0"]

    def auxiliar_grava_acao_por_regra(tabela, C,N):
        S = "match I:\n"
        for i in range(reduce(lambda x,y: x*y,N)):
            S += " "*1+f"case {i}:\n"+" "*2+f"{auxiliar_pega_acoes_por_indice(tabela,i)}\n"
        S+= " "*1+f"case _:\n"+" "*2+f"Default\n"
        print(S)

    for tabela in tds_estruturadas.keys():
        C = [ set() for _ in range(len(tds_estruturadas[tabela]["CONDITIONS"].keys()))]
        N = [ 0 for _ in range(len(tds_estruturadas[tabela]["CONDITIONS"].keys()))]
        for index, linha_de_condicao in enumerate(tds_estruturadas[tabela]["CONDITIONS"].keys()):
            for i in range(len(tds_estruturadas[tabela]["CONDITIONS"][linha_de_condicao])-1):
                C_i = tds_estruturadas[tabela]["CONDITIONS"][linha_de_condicao][i]
                R = tds_estruturadas[tabela]["CONDITIONS"][linha_de_condicao]["ROTULO"]
                if C_i not in C[index]:
                    N[index] +=1
                    if C[index] == set():
                        grava_atribuicao_de_I_if(index, C_i, R, N)
                    else:
                        grava_atribuicao_de_I_elif(index, C_i, R, N)
                    C[index].add(C_i)

        auxiliar_grava_calculo_da_regra(tabela,C,N)
        auxiliar_grava_acao_por_regra(tabela,C,N)

def main():
    if len(sys.argv) == 2:
        #2 SE FOR FORNECIDO O PATH, CHAMA A ROTINA PARA CONSTRUÇÃO DAS TDS ESTRUTURADAS
        switch_method(constroi_tds_estruturadas(sys.argv[1]))
    else:
        #2 SE NÃO FOR FORNECIDO O PATH, MOSTRA UMA MENSAGEM DE ERRO
        print(f' [-] MODO DE USO: py switch_method.py <PATH>')

main()