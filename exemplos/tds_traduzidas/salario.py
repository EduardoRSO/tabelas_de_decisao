if __name__ == '__main__':
#TD decision table 
#TD sets
#TD    Faixa1                 <1000
#TD    Faixa2                 >=10000
#TD    Nota1                  0..5
#TD    Nota2                  6..10
#TD conditions
#TD    Salário                Faixa1  Faixa1  Faixa2  Faixa2
#TD    Avaliação              Nota1   Nota2   Nota1   Nota2
#TD    Faltas<=10             Y       -       Y       Y
#TD actions
#TD    Salário=P1*Salário     0       0       1       0        
#TD    Salário=P2*Salário     1       0       0       1
#TD    Salário=P3*Salário     0       1       0       0
#TD    Congela(Func)          0       0       2       0          
#TD    Promove(Func)          2       2       0       2
#TD    Else_Rule(Func)        0       0       0       0       1
#TD end table
    pass
