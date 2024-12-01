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
    #TD decision table td_estrutura_de_incentivos
    #TD sets
    #TD        hierarquia_gestor                     {"GESTOR"}
    #TD        hierarquia_analista                   {"ANALISTA"}
    #TD        setor_comercial                       {"COMERCIAL"}
    #TD        setor_administrativo                  {"ADMINISTRATIVO"}
    #TD conditions
    #TD        hierarquia               hierarquia_gestor   hierarquia_gestor   hierarquia_gestor       hierarquia_gestor       hierarquia_analista     hierarquia_analista     hierarquia_analista     hierarquia_analista
    #TD        setor                    setor_comercial     setor_comercial     setor_administrativo    setor_administrativo    setor_comercial         setor_comercial         setor_administrativo    setor_administrativo
    #TD        meta_atingida            Y                   N                   Y                       N                       Y                       N                       Y                       N
    #TD actions
    #TD        inscreve_em_cursos()     1                   1                   1                       1                       1                       1                       1                       1                    
    #TD        define_bonificacao(5)    0                   0                   0                       0                       2                       2                       0                       0      
    #TD        define_bonificacao(10)   2                   2                   0                       0                       0                       0                       2                       2           
    #TD        define_bonificacao(15)   0                   0                   2                       2                       0                       0                       0                       0
    #TD        atribui_3dias_de_folga() 3                   0                   3                       0                       3                       0                       3                       0
    #TD end table