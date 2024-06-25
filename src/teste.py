from code_reader.code_reader import CodeReader
from decision_table.decision_table import DecisionTable
from code_generator.code_generator import CodeGenerator

CR = CodeReader('/home/erso/Documents/tcc/tabelas_de_decisao/exemplos/tds_traduzidas/salario.py')

dt = CR.get_extracted_decision_tables()[0]

DT = DecisionTable(dt)

CG = CodeGenerator()

print(CG.generate_code(DT))


'''
pensando sobre como chamar tds recursivamente
percebi que o code reader precisar retornar todas as tds lidas e as posições no arquivo
assim, o objeto DecisionTable terá como objetivo retornar de forma estuturada o nome da td, a td e a posição
O codeGenerator pode inserir um novo dado nessa estrutura: o generated_code
Assim, o code inserter consegue inserir o código, assim como a propria td paraa documentação do código
No code inserter, é preciso recalcular as posições, porque elas serão alteradas à medida que TDS são inseridas.
'''