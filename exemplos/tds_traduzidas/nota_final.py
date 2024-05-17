'''
Uma situação em que se a frequencia for menor que 70, ou o aluno não fazer todas as listas, provas e exercícios-programa, ele está reprovado. 
Para isso, basta assumir que a função calcula_nota_final é dada por min(MP,MEP,ML)'''
if __name__ == '__main__':    
#TD decision table   
#TD sets
#          N                        0..10
#          F                        0..100
#TD conditions
#TD        fez_todas_provas         Y N Y Y N N Y N
#TD        fez_todas_listas         Y Y N Y N Y N N
#TD        fez_todas_eps            Y Y Y N Y N N N
#TD        media_provas             N N N N N N N N  
#TD        media_listas             N N N N N N N N
#TD        media_eps                N N N N N N N N
#TD        frequencia               F F F F F F F F
#TD actions
#TD        calcula_media_provas     1 1 1 1 1 1 1 1
#TD        calcula_media_listas     1 1 1 1 1 1 1 1
#TD        calcula_media_eps        1 1 1 1 1 1 1 1
#TD end table

#TD decision table 
#TD conditions
#TD        media_provas>5           Y N Y N Y N N -
#TD        media_listas>5           Y Y Y N N Y N -
#TD        media_eps>5              Y Y N Y N N N -
#TD        frequencia>70            Y Y Y Y Y Y Y N
#TD actions
#TD        calcula_nota_final       1 1 1 1 1 1 1 0
#TD        nota_final=0             0 0 0 0 0 0 0 1
#TD end table

#TD decision table 
#TD conditions
#TD        nota_final<3             N N -
#TD        nota_final>=3            - Y -
#TD        nota_final>=5            - N Y
#TD actions
#TD        resultado=reprovado      1 0 0
#TD        resultado=recuperação    0 1 0
#TD        resultado=aprovado       0 0 1
#TD end table
    pass 
