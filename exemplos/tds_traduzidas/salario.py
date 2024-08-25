

if __name__ == '__main__':
#TD decision table comissao
#TD sets
#TD    Faixa1                 <1000
#TD    Faixa2                 >=10000
#TD    Nota1                  0..5
#TD    Nota2                  6..10
#TD    Nota3                  {a,A,!,#$,cc,derf,1,2,3,a1,'1'}
#TD    Nota4                  =-1
#TD conditions
#TD    Salario                Faixa1  Faixa1    Faixa1  Faixa1  Faixa2  Faixa2  Faixa2  Faixa2
#TD    Avaliação              Nota1   Nota1     Nota2   Nota2   Nota1   Nota1   Nota2   Nota2     
#TD    Faltas<=10             Y       N         Y       N       Y       N       Y       N
#TD actions
#TD    Salario=P1*Salario     0       1         0       0       1       1       0       0        
#TD    Salario=P2*Salario     1       0         0       0       0       0       0       1
#TD    Salario=P3*Salario     0       0         1       1       0       0       1       0
#TD    Congela(Func)          0       2         0       0       2       2       0       0          
#TD    Promove(Func)          2       0         2       2       0       0       2       2
#TD    Else_Rule(Func)        0       0         0       0       0       0       0       0       1
#TD end table
    pass

#exemplo com comandos e com funçoes
#o codigo gerado deve ser auto documentado
#o codigo gerado deve carregar a sintaxe da td, mudando a td para 2
#limitar a qtd de colunas para n atrapalhar a leitura da td
#A...Z conjunto -->  
#{0,2,4,a,B} --> X IN {0,2,4,'a','B'}    

# mais exemplos com tipos de problemas diferentes --> tabelas diferentes
# de preferencia exemplos de problemas do mundo real

# inserir o codigo direto no python, deforma que seja possivel executar o codigo

#exemplo de tabela que chama uma nova tabela

# uma td que chama outra td. A segunda é definida dentro deuma função.

#exemplos das trilhas do bcc

#exemplo na dissertação em que 2 valores resultam e 4 folhas

#as tds implicam em decidir oq fazer e dps fazer. Isso separa o codigoe o estrutura mais

#elevas o nivel da programação, separando o pensamento de maquona e o problema em si. O ideal é que se esteja o mais proximo possivel do problema

#capitulo de justificação: eleva o nivel de abstração, permitindo uma aproximação do problema. Independete da estrutura da maquina.

