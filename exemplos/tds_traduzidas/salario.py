if __name__ == '__main__':
#TD decision table 
#TD sets
#TD    Faixa1                 <1000
#TD    Faixa2                 >=10000
#TD    Nota1                  0..5
#TD    Nota2                  6..10
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
