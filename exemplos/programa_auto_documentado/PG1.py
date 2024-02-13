#copiei do relatorio técnico, com a pequena mudança de usar [] para indicar o inicio e fim ao invés de 1========= ou (*1=====*)
#1[
#1 TITULO: COMENTÁRIO
#1 AUTOR: AFONSO CELSO ROCHA MASTRELLI
#1 DATA: 29/06/1988
#1 VERSAO: 1.2
#1 FINALIDADE: GERAR RELATÓRIO CONTENDO A DOCUMENTAÇÃO DE DETERMINADO PROGRAMA
#1 ENTRADAS: ARQUIVO QUE CONTEM O CÓDIGO FONTE (EM PASCAL, COBOL OU ZIM) COMENTADO POR NÍVEIS; CÓDIGO DO NÍVEL DE COMENTÁRIO DESEJADO;
#1 SAÍDAS: RELATÓRIO COM A DOCUMENTAÇÃO EXTRAÍDA DO ARQUIVO FONTE;
#1 ROTINAS CHAMADAS: LIB$DO_COMMAND (EXTERNA), MOSTRA_TELA, CABEÇALHO, RELA_RELATPAS E SYS$ASCTIM (EXTERNA);
#1]

#1)esse comentário deve ser ignorado

#2)!@#!@#!@#!@#

#3)todos os simbolos especiais devem ser lidos sem problema

#4)minha ideia é que apenas a estrutura de NOME: COMENTARIO deve ser seguida, porque vou dar split(':')

#1[
#1 ROTINA: MOSTRA_TELA
#1 FINALIDADE: MOSTRA MENU AO USUÁRIO, PERGUNTANDO E RECEBENDO O NÍVEL DE DOCUMENTAÇÃO QUE ELE QUER E O NOME DO ARQUIVO A SER LIDO, PASSANDO ESSAS INFORMAÇÕES AO PROGRAMA PRINCIPAL
#1 ENTRADAS: NÍVEL DE DOCUMENTAÇÃO E NOME DO ARQUIVO A SER LIDO
#1 EXPORTAÇÕES GLOBAIS: NÍVEL DE DOCUMENTAÇÃO E NOME DO ARQUIVO A SER LIDO
#1 CHAMADO POR: COMENTARIO
#1]

#2[
#2 INICIO DE MOSTRA_TELA
#2 LIMPA A TELA 
#2 MOSTRA MENU DE OPÇÕES AO USUARIO
#2 LE OPÇÃO DO USUÁRIO
#2 OPCAO LIDA E DE CONTINAUR EXECUCAO?
#2      LE NOME DO ARQUIVO DE ENTRADA
#2      LE NOME DA LINGUAGEM UTILIZADA NO PROGRAMA
#2      LINGUAGEM NÃO É COBOL NEM ZIM?
#2              ASSUME-SE PASCAL COMO LINGUAGEM UTILIZADA
#2 FIM DE MOSTRA_TELA    
#2]

#5)no relatório o nível 3 é dito como aquele que engloba os niveis 1 e 2, assim como está no programa, mas eu acho que seria melhor fazer esse nível para comentar alguns detalhes ou truques, assim como sugerido pelo setzer

#3[
#3 LIMPA TELA FOI PRODUZIDA USANDO WRITE(CLS), PORQUE, DADO QUE CLS ESTÁ VAZIO, O BUFFER É ALTERADO PARA UMA STRING VAZIA
#3 AS OPÇÕES DO MENU ESTÃO NO ARQUIVO constants.py, EM FORMATO DE LISTA
#3 CASO SEJA FORNECIDO A ENTRADA DEVMODE SERÃO CRIADOS ARQUIVOS .JSON COM O PRODUTO CARTESIANO DOS NÍVEIS DISPONÍVEIS  
#3]


#6)eu acho que o controle de versionamento não é interessante, porque como vou utilizar o git, ele já possui uma ferramenta para tal
#7)mas fazer os comentários no código usando um determinado padrão e criar um programa que extrai esses comentários à minha escolha definitivamente é interessante
#8)a minha ideia é que o produto final seja um arquivo json, porque é muito fácil fazer a leitura, escrita e converter em uma estrutura de dados.
#9)fora que usando o arcabouço pandas do python, posso transofrmar em um dataframe e converter para uma infinidade de formatos, o pandas permite até o uso de uma sintaxe semelhante ao SQL, usando WHERE, SELECT, JOIN, etc.
#10)o extrator vai ser capaz de resgatar comentarios de linha única(nivel 2) e blocos de comentário(nivel 1 e 3).... talvez eu use apenas comentarios de linha para facilitar minha vida