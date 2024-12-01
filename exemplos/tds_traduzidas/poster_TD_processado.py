hierarquia = ''
setor = ''
meta_atingida = ''

def inscreve_em_cursos():
    print(f'Funcionário inscrito em cursos de desenvolvimento')

def define_bonificacao(valor:int):
    print(f'Funcionário recebe bonificacção de {valor}% do salário')

def atribui_3dias_de_folga():
    print(f'Funcionário recebe 3 dias de folga')

if __name__ == '__main__':
    hierarquia = input('').upper()
    setor = input('').upper()
    meta_atingida = (input('').upper() == 'Y')
    #2[
    #2 #TD decision table td_estrutura_de_incentivos
    #2 #TD sets
    #2 #TD        hierarquia_gestor                     {"GESTOR"}
    #2 #TD        hierarquia_analista                   {"ANALISTA"}
    #2 #TD        setor_comercial                       {"COMERCIAL"}
    #2 #TD        setor_administrativo                  {"ADMINISTRATIVO"}
    #2 #TD conditions
    #2 #TD        hierarquia               hierarquia_gestor   hierarquia_gestor   hierarquia_gestor       hierarquia_gestor       hierarquia_analista     hierarquia_analista     hierarquia_analista     hierarquia_analista
    #2 #TD        setor                    setor_comercial     setor_comercial     setor_administrativo    setor_administrativo    setor_comercial         setor_comercial         setor_administrativo    setor_administrativo
    #2 #TD        meta_atingida            Y                   N                   Y                       N                       Y                       N                       Y                       N
    #2 #TD actions
    #2 #TD        inscreve_em_cursos()     1                   1                   1                       1                       1                       1                       1                       1                    
    #2 #TD        define_bonificacao(5)    0                   0                   0                       0                       2                       2                       0                       0      
    #2 #TD        define_bonificacao(10)   2                   2                   0                       0                       0                       0                       2                       2           
    #2 #TD        define_bonificacao(15)   0                   0                   2                       2                       0                       0                       0                       0
    #2 #TD        atribui_3dias_de_folga() 3                   0                   3                       0                       3                       0                       3                       0
    #2 #TD end table
    #2]
    def decision_table_td_estrutura_de_incentivos() ->None:
        I_0 = 0 #Inicialização do auxiliar da condição hierarquia
        I_1 = 0 #Inicialização do auxiliar da condição setor
        I_2 = 0 #Inicialização do auxiliar da condição meta_atingida
        I   = 0 #Inicialização do número da regra
        if hierarquia in set(["GESTOR"]):
            I_0 = 0
        elif hierarquia in set(["ANALISTA"]):
            I_0 = 1
        if setor in set(["COMERCIAL"]):
            I_1 = 0
        elif setor in set(["ADMINISTRATIVO"]):
            I_1 = 1
        if meta_atingida == True:
            I_2 = 0
        elif meta_atingida == False:
            I_2 = 1
        I = (2*2*1)*I_0 + (2*1)*I_1 + (1)*I_2
        match I:
            case 0:
                inscreve_em_cursos()
                define_bonificacao(10)
                atribui_3dias_de_folga()
            case 1:
                inscreve_em_cursos()
                define_bonificacao(10)
            case 2:
                inscreve_em_cursos()
                define_bonificacao(15)
                atribui_3dias_de_folga()
            case 3:
                inscreve_em_cursos()
                define_bonificacao(15)
            case 4:
                inscreve_em_cursos()
                define_bonificacao(5)
                atribui_3dias_de_folga()
            case 5:
                inscreve_em_cursos()
                define_bonificacao(5)
            case 6:
                inscreve_em_cursos()
                define_bonificacao(10)
                atribui_3dias_de_folga()
            case 7:
                inscreve_em_cursos()
                define_bonificacao(10)
            case _:
                exit()
    decision_table_td_estrutura_de_incentivos()
