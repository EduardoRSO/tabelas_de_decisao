# Tabelas de decisão

Um pré-processador de tabelas de decisão, segundo a dissertação apresentada ao instituto de matemática e estatítica da universidade de São Paulo por Satoshi Nagayama, com o Prof. Dr. Valdemar W. Setzer como orientador. <br> 
Tabelas de Decisão ajudam a especificar condições lógicas de uma maneira compacta e gráfica, com enormes vantagens sobre árvores de decisão (encaixamentos de comandos if...then...else). Nesse projeto estamos implementando um pré-processador de tabelas de decisão imersas em programas em Python. O pré-processador converte as tabelas de decisão em código de Python. <br>
Além disso, todos os códigos do gerador/interpretador serão auto-documentados, isto é, toda a documentação está dentro dos programas, e 3 níveis de abstração. Está sendo feito um programa para extrair os vários níveis, de modo que se pode examinar a documentação nível a nível. O resultado é um texto em pdf com a documentação desejada.<br>

Capa

# Universidade de São Paulo
## Instituto de Matemática e Estatística

---

# Tabelas de Decisão em Python

### Eduardo Ribeiro Silva de Oliveira

---

**Orientador:** Prof. Dr. Valdemar W. Setzer

---

**São Paulo**  
**2024**

Abstract

## Abstract

Decision tables are a compact and graphical method for specifying logical conditions, offering significant advantages over traditional decision trees (nested `if...then...else` statements). This work explores the application of decision tables in Python, providing a more intuitive and efficient approach to decision-making in programming. 

The goal of this study is to develop a preprocessor for decision tables in Python, using a model described in Satoshi Nagayama's dissertation. The preprocessor aims to generate Python code from embedded decision tables within the program, facilitating a clearer and more concise expression of logical conditions. Additionally, the project emphasizes the importance of self-documenting code, as it enhances collaboration, reduces development time, and improves the maintainability and reliability of software.

The implementation of the decision table preprocessor will be tested through various case studies, including real-world examples from the author's data analysis internship. The results demonstrate the potential of decision tables to simplify code comprehension, making it more accessible to both programmers and non-programmers alike.

**Keywords**: Decision tables, Python, code generation, self-documentation, programming.


Resumo

## Resumo

Tabelas de decisão são um método compacto e gráfico para especificar condições lógicas, oferecendo vantagens significativas sobre árvores de decisão tradicionais (estruturas aninhadas de `if...then...else`). Este trabalho explora a aplicação de tabelas de decisão em Python, proporcionando uma abordagem mais intuitiva e eficiente para a tomada de decisões na programação.

O objetivo deste estudo é desenvolver um pré-processador para tabelas de decisão em Python, utilizando o modelo descrito na dissertação de Satoshi Nagayama. O pré-processador visa gerar código Python a partir de tabelas de decisão embutidas no programa, facilitando uma expressão mais clara e concisa das condições lógicas. Além disso, o projeto enfatiza a importância da auto-documentação do código, pois isso melhora a colaboração, reduz o tempo de desenvolvimento e aumenta a manutenibilidade e confiabilidade do software.

A implementação do pré-processador de tabelas de decisão será testada por meio de diversos estudos de caso, incluindo exemplos do mundo real provenientes do estágio do autor em análise de dados. Os resultados demonstram o potencial das tabelas de decisão para simplificar a compreensão do código, tornando-o mais acessível tanto para programadores quanto para não programadores.

**Palavras-chave**: Tabelas de decisão, Python, geração de código, auto-documentação, programação.


Introdução

## Introdução

A programação, em sua essência, envolve a criação de algoritmos que tomam decisões com base em condições lógicas. Tradicionalmente, essas decisões são implementadas por meio de estruturas como `if...then...else`, que, quando aninhadas, podem se tornar complexas e difíceis de manter. Nesse contexto, as tabelas de decisão emergem como uma alternativa poderosa, oferecendo uma forma compacta, gráfica e organizada de especificar condições lógicas.

As tabelas de decisão são amplamente utilizadas em áreas como engenharia de software e processamento de dados administrativos, onde é crucial representar combinações lógicas de maneira clara e eficiente. Elas permitem que os desenvolvedores visualizem de forma direta todas as possíveis condições e ações correspondentes, facilitando tanto a codificação quanto a validação de sistemas complexos.

Este trabalho tem como objetivo explorar e implementar o uso de tabelas de decisão na linguagem Python, por meio do desenvolvimento de um pré-processador que converta essas tabelas em código Python executável. A abordagem é inspirada na dissertação de mestrado de Satoshi Nagayama, que descreve um sistema similar para outras linguagens de programação. Ao implementar este pré-processador, espera-se não apenas simplificar a codificação de condições lógicas, mas também promover a auto-documentação do código, uma prática que melhora significativamente a manutenção e a compreensão do software ao longo do tempo.

Além de oferecer uma alternativa mais legível e estruturada às tradicionais árvores de decisão, este trabalho também busca demonstrar como as tabelas de decisão podem ser aplicadas em cenários reais. Para isso, serão utilizados exemplos práticos provenientes de experiências do autor em análise de dados, destacando como essa abordagem pode reduzir o tempo de desenvolvimento e facilitar a comunicação entre programadores e outros profissionais.

Assim, este TCC contribui para o avanço das práticas de desenvolvimento em Python, introduzindo uma ferramenta que alia clareza, eficiência e facilidade de manutenção. Espera-se que o trabalho sirva de base para futuras pesquisas e desenvolvimentos na área, estimulando a adoção de tabelas de decisão em projetos de software de diversas naturezas.


Definição de uma tabela de decisão

## Definição da Sintaxe da Tabela de Decisão em Python

### Introdução

A tabela de decisão (TD) é uma ferramenta poderosa que permite organizar e simplificar a lógica condicional em programas de computador. Em vez de utilizar estruturas de controle tradicionais como `if...else`, a tabela de decisão estrutura as condições e as ações de maneira tabular, facilitando a compreensão, manutenção e expansão do código. Neste trabalho, a sintaxe da tabela de decisão foi implementada em Python, e este texto aborda a estrutura, as regras e as limitações dessa abordagem.

### Estrutura da Tabela de Decisão

Uma tabela de decisão em Python, conforme implementada neste TCC, é composta por três seções principais:

1. **Conjuntos (Sets)**: Definem os grupos de valores possíveis para as variáveis que serão analisadas nas condições.
2. **Condições (Conditions)**: Listam as condições lógicas que, quando avaliadas, determinam quais ações devem ser executadas.
3. **Ações (Actions)**: Especificam as operações a serem realizadas com base nas condições avaliadas.

### Sintaxe da Tabela de Decisão

A sintaxe da tabela de decisão segue um formato específico para garantir clareza e funcionalidade. Abaixo está um exemplo de como essa sintaxe é utilizada em um programa Python:

```python
if __name__ == '__main__':
    # Código inicial...
    
    while True:
        option = int(input('> Please choose an option:\n'
                           '  1 - Update the database\n'
                           '  2 - Perform data analysis and plot graphs\n'
                           '  3 - Quit the program\n> '))
        #TD decision table td_main
        #TD sets
        #TD        opcao_valida                     {1,2,3,12,13,123}
        #TD        atualiza                         {1}
        #TD        analisa                          {2}
        #TD        sai                              {3}
        #TD        atualiza_analisa                 {12}
        #TD        atualiza_sai                     {13}
        #TD        atualiza_analisa_sai             {123}
        #TD conditions
        #TD        option                           opcao_valida  opcao_valida opcao_valida opcao_valida        opcao_valida opcao_valida 
        #TD        option                           atualiza      analisa      sai          atualiza_analisa    atualiza_sai atualiza_analisa_sai
        #TD actions
        #TD        analysis.visualization_core()    0             1            0            2                   0            2
        #TD        updater.update_core()            1             0            0            1                   1            1  
        #TD        quit_program()                   0             0            1            0                   2            3
        #TD end table

## Definições e Regras

### 1. Conjuntos (Sets)

**Definição**: Conjuntos, ou sets, definem as coleções de valores possíveis para as variáveis que serão analisadas nas condições. No exemplo acima, o conjunto `opcao_valida` define os valores `{1,2,3,12,13,123}`, que correspondem às opções válidas que o usuário pode selecionar.

**Regra**: Cada conjunto deve ser definido com um nome claro e os valores possíveis devem estar entre chaves `{}`. O nome do conjunto serve como uma referência nas condições subsequentes.

**Limitação**: Todos os valores dentro de um conjunto devem ser únicos e distintos. Além disso, as interações entre diferentes conjuntos devem ser consideradas cuidadosamente para evitar ambiguidades na avaliação das condições.

### 2. Condições (Conditions)

**Definição**: Condições são as expressões lógicas que determinam quais ações serão executadas. Cada linha de condição avalia uma variável em relação aos conjuntos definidos e mapeia essas avaliações a ações específicas.

**Regra**: As condições devem ser definidas usando as variáveis associadas aos conjuntos. Cada coluna na linha de condições representa uma combinação de valores que será avaliada.

**Limitação**: A complexidade das condições é limitada pela clareza necessária para a manutenção do código. Condições excessivamente complexas ou dependentes de múltiplos conjuntos podem dificultar a legibilidade e a depuração.

### 3. Ações (Actions)

**Definição**: Ações especificam o que deve ser feito quando uma condição correspondente é avaliada como verdadeira. Cada linha em `actions` define uma função ou procedimento a ser executado.

**Regra**: As ações são mapeadas diretamente para as condições. O número em cada célula (`0`, `1`, `2`, etc.) indica se a ação deve ser executada (`1`), ignorada (`0`), ou se deve fazer parte de um grupo de ações a serem executadas em sequência.

**Limitação**: A execução de ações deve ser cuidadosamente ordenada para evitar efeitos colaterais indesejados. Por exemplo, uma ação que encerra o programa (`quit_program()`) deve ser claramente distinguida e normalmente colocada no final da sequência de ações.

## Limitações e Regras da Sintaxe

**Ordem de Avaliação**: A tabela de decisão é avaliada de cima para baixo, o que significa que a ordem das condições e ações é crucial. Alterações na ordem podem mudar o comportamento do programa.

**Clareza e Manutenção**: Embora a tabela de decisão simplifique a lógica condicional, ela também impõe a necessidade de uma organização clara e concisa. Tabelas complexas podem se tornar difíceis de manter se não forem bem documentadas.

**Flexibilidade vs. Rigor**: A tabela de decisão oferece flexibilidade na definição de condições e ações, mas exige rigor na implementação para evitar inconsistências. Cada conjunto, condição e ação deve ser cuidadosamente definido para garantir que a tabela funcione conforme o esperado.

**Extensibilidade**: A adição de novas condições ou ações requer uma revisão completa da tabela para garantir que a nova lógica seja corretamente integrada. Isso pode aumentar a complexidade do código, exigindo mais atenção na manutenção.

## Conclusão

A sintaxe da tabela de decisão implementada em Python neste TCC proporciona uma maneira estruturada e eficiente de lidar com lógicas condicionais complexas. Ao seguir as definições e regras descritas, é possível criar sistemas mais legíveis e fáceis de manter, embora seja essencial estar ciente das limitações e desafios associados. A tabela de decisão utilizada neste trabalho exemplifica como uma abordagem disciplinada pode resultar em um código mais organizado e escalável, facilitando a evolução e manutenção do sistema ao longo do tempo.


Metodologia

## Metodologia

### 1. Desenvolvimento do Pré-Processador de Tabelas de Decisão

O desenvolvimento do pré-processador de tabelas de decisão em Python foi dividido em várias etapas, cada uma com um foco específico na estruturação e automatização do processo de conversão de tabelas de decisão em código executável. A seguir, detalha-se o fluxo metodológico utilizado:

### 1.1. Análise de Requisitos

O primeiro passo foi a análise detalhada das necessidades que o pré-processador deveria atender. Baseando-se na dissertação de Satoshi Nagayama, foram identificados os seguintes requisitos principais:
- **Leitura de tabelas de decisão embutidas em arquivos Python**: O sistema deveria ser capaz de identificar e extrair tabelas de decisão formatadas de maneira específica.
- **Processamento das tabelas de decisão**: As tabelas de decisão extraídas deveriam ser processadas para identificar condições, ações e conjuntos associados.
- **Geração de código Python**: A partir das tabelas de decisão processadas, o sistema deveria gerar código Python correspondente, utilizando diferentes métodos de tradução.
- **Inserção do código gerado**: O código gerado deveria ser inserido automaticamente nos locais apropriados dentro do arquivo original.

### 1.2. Estruturação do Código

Para atender aos requisitos, o desenvolvimento foi estruturado em módulos, cada um responsável por uma parte específica do processo:

- **Módulo `code_reader.py`**: Este módulo foi responsável pela leitura do arquivo Python original e pela extração das tabelas de decisão. Foi implementado com um foco robusto na validação do caminho do arquivo e na extração precisa das tabelas de decisão e suas posições dentro do código.

- **Módulo `decision_table.py`**: Focado na modelagem das tabelas de decisão, este módulo encapsula a lógica necessária para representar e manipular as tabelas extraídas, permitindo sua fácil integração nos processos subsequentes.

- **Módulo `condition.py`, `action.py`, `set.py`**: Estes módulos foram desenvolvidos para processar e extrair condições, ações e conjuntos das tabelas de decisão. Cada módulo é responsável por interpretar uma parte específica da tabela de decisão e preparar esses elementos para a geração de código.

- **Módulo `code_generator.py`**: O coração do pré-processador, este módulo é responsável por traduzir as tabelas de decisão processadas em código Python executável. Ele oferece suporte a diferentes métodos de tradução, como o `switch method`, `fatorações sucessivas`, `busca exaustiva`, e `programação dinâmica`. Cada método foi implementado para maximizar a eficiência e a clareza do código gerado.

- **Módulo `code_inserter.py`**: Após a geração do código, este módulo insere o código gerado nos locais apropriados no arquivo original. O processo de inserção foi cuidadosamente projetado para preservar a estrutura original do arquivo enquanto integra o novo código de maneira fluida.

- **Módulo `workflow_controller.py`**: Este módulo controla o fluxo completo do pré-processador, desde a leitura das tabelas de decisão até a inserção do código gerado no arquivo final. Ele orquestra a interação entre os módulos e garante que o processo seja executado de maneira eficiente e coerente.

### 1.3. Auto-Documentação

Um dos aspectos centrais deste trabalho foi a implementação de uma metodologia de auto-documentação. Cada função e classe desenvolvida foi acompanhada de comentários detalhados que seguem um padrão pré-estabelecido. Estes comentários incluem informações sobre a finalidade, entradas, saídas, dependências e rotinas chamadas. A auto-documentação foi projetada para:
- **Facilitar a manutenção do código**: Permitindo que outros desenvolvedores compreendam rapidamente o funcionamento do sistema.
- **Promover a clareza e a transparência**: Ajudando a evitar mal-entendidos e erros durante a evolução do código.
- **Servir como base para futuras melhorias**: A documentação clara permite que novos recursos sejam adicionados sem comprometer a integridade do código existente.

### 1.4. Desenvolvimento do Extrator de Documentação

Além do pré-processador, foi desenvolvido o script `extrator_de_documentacao.py`, que automatiza a extração e geração de relatórios em PDF da documentação presente no código-fonte. Abaixo, detalhes da implementação e funcionamento deste módulo:

- **Finalidade do Código**:
  - O script `extrator_de_documentacao.py` foi criado com o objetivo de automatizar a extração de comentários de auto-documentação em diferentes níveis (1, 2 e 3) de um arquivo de código Python. O resultado é um relatório em formato PDF que contém a documentação extraída, facilitando a leitura e o compartilhamento da documentação gerada automaticamente.

- **Estrutura do Código**:
  - O código está dividido em funções específicas para extrair os diferentes níveis de documentação e para gerar o PDF final com as informações extraídas.

- **Níveis de Documentação**:
  - **Nível 1**: Documentação mais básica, contendo cabeçalhos de procedimentos e descrições gerais.
  - **Nível 2**: Inclui a documentação de nível 1 e adiciona detalhes sobre algoritmos e estruturas de dados.
  - **Nível 3**: Engloba os níveis 1 e 2, além de incluir todos os detalhes do código, com uma documentação detalhada das implementações.

- **Funções de Extração**:
  - **`extrai_nivel_1`, `extrai_nivel_2`, `extrai_nivel_3`**: Essas funções utilizam expressões regulares para percorrer o arquivo de código e extrair os comentários correspondentes a cada nível de documentação. A função `re.findall()` é utilizada para localizar e coletar as partes relevantes do texto.

- **Geração do PDF**:
  - **`constroi_pdf`**: Esta função utiliza a biblioteca `reportlab` para gerar um arquivo PDF que contém a documentação extraída. O layout do PDF é básico, com opções de configuração para o título, tamanho da fonte, e margens. A função cuida de distribuir o conteúdo nas páginas, criando novas páginas quando necessário.

- **Modo de Execução**:
  - O script é executado a partir da linha de comando, onde o usuário fornece três argumentos: o caminho do arquivo de código, o nível de documentação desejado, e o caminho para salvar o PDF gerado. O script então seleciona a função de extração correspondente e cria o relatório em PDF.

### 1.5. Testes e Validação

Após o desenvolvimento de cada módulo, foram realizados testes unitários para garantir que cada parte do sistema funcionasse conforme o esperado. Além disso, o sistema como um todo foi testado utilizando tabelas de decisão reais extraídas de atividades realizadas durante o estágio do autor em análise de dados. Os testes focaram em:
- **Precisão da extração das tabelas de decisão**.
- **Correta geração do código Python a partir das tabelas de decisão**.
- **Integridade do código inserido no arquivo original**.

### 1.6. Implementação dos Exemplos

Finalmente, foram desenvolvidos exemplos práticos de tabelas de decisão para demonstrar o funcionamento do pré-processador. Esses exemplos foram escolhidos com base em cenários reais enfrentados durante o estágio do autor, e ilustram como o sistema pode ser aplicado para resolver problemas de tomada de decisão de maneira eficiente e automatizada.

### 1.7. Ferramentas Utilizadas

O desenvolvimento do pré-processador foi realizado utilizando as seguintes ferramentas:
- **Linguagem de programação Python**: Escolhida pela sua flexibilidade e pela ampla gama de bibliotecas disponíveis.
- **Bibliotecas padrão do Python (re, os, etc.)**: Utilizadas para manipulação de strings, arquivos e expressões regulares.
- **Editor de código**: Visual Studio Code, para edição e depuração do código.
- **Sistema de controle de versão**: Git, para rastreamento das mudanças no código e colaboração.

### Conclusão

A metodologia adotada permitiu o desenvolvimento de um pré-processador de tabelas de decisão robusto e eficiente, com um alto grau de auto-documentação. O resultado é uma ferramenta poderosa para desenvolvedores Python que necessitam integrar tabelas de decisão em seus projetos de forma automatizada, clara e documentada. Além disso, a criação de um extrator de documentação complementa o projeto, permitindo a geração de relatórios detalhados que facilitam a compreensão e o compartilhamento do código.


Discussão:

## Discussão

### 1. Implementação das Tabelas de Decisão em Python

A implementação das tabelas de decisão em Python, através do desenvolvimento de um pré-processador específico, mostrou-se uma solução eficaz para a automatização e simplificação da codificação de condições lógicas complexas. As tabelas de decisão fornecem uma representação clara e concisa das regras de negócio, que foi diretamente traduzida em código Python utilizando diferentes métodos de tradução, como o `switch method`, `fatorações sucessivas`, `busca exaustiva` e `programação dinâmica`.

A escolha do Python como linguagem de implementação foi motivada pela sua flexibilidade e pela vasta gama de bibliotecas disponíveis, o que facilitou a integração das tabelas de decisão com os sistemas existentes. Além disso, o uso de Python permitiu a criação de um sistema modular e extensível, onde cada parte do processo, desde a leitura das tabelas até a inserção do código gerado, foi encapsulada em módulos separados, favorecendo a manutenção e a evolução futura do projeto.

### 2. Auto-Documentação e Manutenção de Código

Um dos aspectos mais inovadores deste trabalho foi a integração da auto-documentação ao longo de todo o desenvolvimento do pré-processador. Cada função e classe foram acompanhadas de comentários detalhados, seguindo uma estrutura padronizada que inclui informações sobre a finalidade, entradas, saídas, dependências e rotinas chamadas. Essa abordagem não só melhorou a clareza do código, mas também facilitou a colaboração e a manutenção do projeto.

A auto-documentação demonstrou ser uma prática essencial para projetos de software de longo prazo, onde a manutenção e a evolução do código são inevitáveis. A capacidade de gerar relatórios de documentação em diferentes níveis (1, 2 e 3), utilizando o `extrator_de_documentacao.py`, permite que a documentação se mantenha sempre atualizada e alinhada com o código, reduzindo significativamente o tempo necessário para compreender e modificar o software.

### 3. Validação e Testes

Os testes realizados com o pré-processador validaram sua eficácia em traduzir tabelas de decisão em código Python executável de maneira correta e eficiente. A utilização de exemplos reais, provenientes das atividades realizadas durante o estágio do autor, proporcionou uma validação prática das funcionalidades implementadas. Esses testes mostraram que o sistema é capaz de lidar com diferentes complexidades de tabelas de decisão, garantindo que as regras de negócio sejam implementadas fielmente no código gerado.

Entretanto, alguns desafios foram identificados durante os testes, como a necessidade de otimização do código gerado para cenários de grande escala, onde o número de condições e ações nas tabelas de decisão é elevado. Embora o sistema atual seja robusto para casos de uso comuns, futuras melhorias poderão focar em técnicas de otimização para reduzir a complexidade computacional do código gerado.

### 4. Limitações e Possíveis Melhorias

Embora o pré-processador desenvolvido tenha atendido aos objetivos propostos, algumas limitações foram identificadas. A principal limitação está relacionada à complexidade dos métodos de tradução utilizados, especialmente em tabelas de decisão com um grande número de condições e ações. Nesses casos, o código gerado pode se tornar menos legível e mais difícil de manter, especialmente para desenvolvedores menos experientes.

Para mitigar essas limitações, futuras versões do pré-processador podem incluir:
- **Melhorias na interface de usuário**: Desenvolver uma interface gráfica ou um sistema web para facilitar a especificação e visualização das tabelas de decisão.
- **Otimização do código gerado**: Implementar técnicas de otimização que possam reduzir a redundância e melhorar a performance do código em cenários complexos.
- **Integração com outras ferramentas**: Expandir a compatibilidade do pré-processador para que ele possa ser integrado com outras linguagens de programação além do Python, aumentando sua aplicabilidade em diferentes contextos.

### 5. Contribuições do Trabalho

Este trabalho contribuiu significativamente para a área de engenharia de software ao demonstrar como tabelas de decisão podem ser efetivamente implementadas e automatizadas em Python. Além disso, a introdução de práticas de auto-documentação no desenvolvimento do pré-processador destaca a importância de uma documentação clara e acessível, não apenas para a manutenção do código, mas também para a sua evolução.

O desenvolvimento do `extrator_de_documentacao.py` é outra contribuição importante, pois permite que a documentação seja gerada automaticamente em diferentes níveis, facilitando a compreensão e o compartilhamento do código. Essa ferramenta é particularmente útil em ambientes colaborativos, onde diferentes níveis de documentação podem ser necessários para diferentes públicos, como desenvolvedores, gerentes de projeto e stakeholders.

### 6. Impacto Prático

O impacto prático deste trabalho é evidente na simplificação e automatização do processo de codificação de condições lógicas complexas. O pré-processador desenvolvido pode ser diretamente aplicado em projetos reais, onde a clareza e a eficiência do código são cruciais. Além disso, a abordagem de auto-documentação implementada neste projeto serve como um modelo para outros desenvolvedores e equipes de software, incentivando a adoção de práticas que promovem a manutenção e a longevidade do código.

### 7. Perspectivas Futuras

O trabalho realizado abre várias oportunidades para pesquisas e desenvolvimentos futuros. Algumas das possíveis direções incluem:
- **Exploração de novas técnicas de otimização**: Investigar métodos de otimização que possam melhorar ainda mais a performance do código gerado.
- **Expansão do suporte para outras linguagens**: Adaptar o pré-processador para funcionar com outras linguagens de programação, aumentando sua utilidade e alcance.
- **Desenvolvimento de uma interface gráfica**: Criar uma interface amigável que permita a criação e visualização de tabelas de decisão de maneira mais intuitiva.

Estas perspectivas futuras mostram que o trabalho realizado até agora é apenas o começo de um campo promissor dentro da engenharia de software, com potencial para influenciar positivamente a forma como desenvolvedores abordam a automatização de regras de negócio e a documentação de código.

### Conclusão

A discussão apresentada demonstra que os objetivos do trabalho foram amplamente alcançados, com o desenvolvimento de um pré-processador funcional e bem documentado. As limitações identificadas abrem caminho para melhorias e inovações futuras, garantindo que este trabalho continue a evoluir e a contribuir para a comunidade de desenvolvimento de software.

Exemplos práticos/ Estudo de caso

### Estudo de Caso: Automação de Análise de Inflação com `sidra.py`

O script `sidra.py` foi desenvolvido como parte deste trabalho para demonstrar uma aplicação prática de automação na coleta, processamento, e análise de dados econômicos, especificamente a inflação no Brasil, utilizando tabelas de decisão e integração com APIs externas.

#### Descrição Geral

O `sidra.py` integra dados da API Sidra do IBGE com uma base de dados no Notion, automatizando a atualização e manutenção dessas informações. Além disso, ele realiza cálculos baseados nos dados coletados e gera gráficos que refletem a variação do Índice Nacional de Preços ao Consumidor Amplo (IPCA) e do IPCA-15 ao longo do tempo.

#### Funcionalidades Principais

- **Coleta de Dados**: Utilizando a biblioteca `sidrapy`, o script coleta dados relacionados ao IPCA e IPCA-15 diretamente da API do IBGE. A classe `HandlerIBGE` é responsável por esse processo, gerando e formatando os dados para análises subsequentes.

- **Integração com o Notion**: A classe `HandlerDatabase` gerencia a conexão e as operações no banco de dados do Notion. Ela permite a atualização, inserção e sincronização de informações entre os dados obtidos do IBGE e as tabelas armazenadas no Notion, garantindo que a base de dados esteja sempre atualizada.

- **Análise e Visualização de Dados**: Através da classe `HandlerAnalysis`, o script oferece funcionalidades para gerar gráficos de contribuição e variação, permitindo que os usuários visualizem a evolução dos índices ao longo do tempo. Esses gráficos são gerados utilizando o `matplotlib`, proporcionando uma maneira clara e visual de interpretar os dados.

- **Automação e Manutenção**: A classe `HandlerUpdater` coordena a atualização da base de dados do Notion com os dados mais recentes obtidos da API do IBGE. Ela valida e corrige registros, garantindo a integridade e atualidade das informações.

#### Impacto Prático

O `sidra.py` exemplifica como a automação pode ser aplicada para facilitar a análise de dados complexos, como os relacionados à inflação. A integração com APIs externas e a capacidade de gerar visualizações automáticas tornam o script uma ferramenta poderosa para economistas, analistas de dados e outros profissionais que precisam monitorar indicadores econômicos de forma eficiente e precisa.

Além disso, a modularidade do código e o uso de práticas de auto-documentação asseguram que o sistema seja fácil de manter e expandir, permitindo adaptações futuras conforme as necessidades dos usuários.

#### Conclusão

O desenvolvimento do `sidra.py` dentro do contexto deste trabalho demonstra como as tabelas de decisão e as práticas de auto-documentação podem ser integradas em soluções reais, proporcionando não apenas uma melhoria na eficiência operacional, mas também um aumento na qualidade e acessibilidade dos dados analisados. Este estudo de caso reforça a aplicabilidade prática dos conceitos explorados ao longo deste TCC.

Conclusão

## Conclusão

O presente trabalho teve como objetivo desenvolver um pré-processador de tabelas de decisão em Python, com ênfase na automatização da codificação de condições lógicas complexas e na promoção de práticas de auto-documentação. Ao longo do desenvolvimento, foram alcançados resultados significativos que contribuem para a simplificação do processo de programação e para a melhoria da manutenção de código em projetos de software.

### 1. Resultados Alcançados

O pré-processador desenvolvido foi capaz de traduzir tabelas de decisão em código Python executável, utilizando diferentes métodos de tradução, como o `switch method`, `fatorações sucessivas`, `busca exaustiva`, e `programação dinâmica`. Essa ferramenta demonstrou ser eficiente na conversão de regras de negócio complexas em código de forma automatizada, clara e concisa. A modularidade do sistema permitiu uma fácil manutenção e evolução do projeto, garantindo que futuras melhorias possam ser implementadas com facilidade.

A integração de práticas de auto-documentação foi outro marco importante do trabalho. A criação de comentários detalhados em cada função e classe, juntamente com o desenvolvimento do `extrator_de_documentacao.py`, garantiu que a documentação do código fosse sempre clara e atualizada. Isso não apenas facilita a compreensão do sistema por outros desenvolvedores, mas também promove uma manutenção mais eficiente e menos propensa a erros.

### 2. Contribuições para a Engenharia de Software

Este trabalho contribuiu de maneira significativa para a engenharia de software ao demonstrar como tabelas de decisão podem ser efetivamente implementadas e automatizadas em Python. A introdução de uma metodologia de auto-documentação aplicada ao desenvolvimento de software reforça a importância de práticas que aumentam a clareza e a manutenção do código, assegurando que o software permaneça compreensível e eficiente ao longo do tempo.

A criação do `extrator_de_documentacao.py` é uma inovação que facilita a geração automática de documentação em diferentes níveis, atendendo às necessidades de diversos públicos, desde desenvolvedores até gestores de projeto. Essa ferramenta tem o potencial de ser aplicada em diversos contextos, auxiliando na organização e na comunicação de projetos de software.

### 3. Limitações e Oportunidades para Futuras Pesquisas

Embora o pré-processador desenvolvido tenha alcançado seus objetivos, foram identificadas algumas limitações, especialmente em relação à complexidade e legibilidade do código gerado em casos de tabelas de decisão com grande número de condições e ações. Essas limitações abrem caminho para futuras pesquisas focadas em otimização de código e expansão do suporte do pré-processador para outras linguagens de programação.

Outras oportunidades de pesquisa incluem o desenvolvimento de interfaces gráficas para facilitar a criação e visualização de tabelas de decisão, bem como a investigação de novas técnicas de otimização que possam melhorar ainda mais a performance do código gerado.

### 4. Impacto Prático e Perspectivas Futuras

O impacto prático deste trabalho é evidente na sua aplicação direta em projetos reais, onde a clareza e a eficiência do código são cruciais. O pré-processador pode ser utilizado em diversas áreas que necessitam de uma automação eficaz das regras de negócio, proporcionando uma solução robusta e acessível.

No futuro, o trabalho realizado pode ser expandido para incluir suporte a outras linguagens de programação, bem como para desenvolver novas funcionalidades que aprimorem a usabilidade e a eficiência do sistema. A adoção das práticas de auto-documentação discutidas neste trabalho pode também inspirar outros projetos de software, incentivando o desenvolvimento de códigos mais claros e bem documentados.

### Conclusão Final

Em síntese, este trabalho não apenas alcançou os objetivos propostos, mas também abriu novas perspectivas para o desenvolvimento de ferramentas de automatização e documentação em projetos de software. A integração de tabelas de decisão em Python, juntamente com a prática de auto-documentação, oferece uma abordagem inovadora e eficaz para enfrentar os desafios da programação moderna. As contribuições realizadas por este trabalho têm o potencial de impactar positivamente a forma como desenvolvedores abordam a codificação de regras de negócio e a documentação de software, promovendo melhores práticas e aumentando a qualidade dos projetos desenvolvidos.


Bilbiografia

## Bibliografia

- KING, P. J. H. *Decision Tables*. 1. ed. London: Pitman Publishing, 1967.

- KOHAVI, Ron. *The Power of Decision Tables*. In: *Proceedings of the 8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. ACM, 2005. p. 725-730.

- MORET, Bernard M. E. *Decision Trees and Diagrams*. 1. ed. London: Addison-Wesley, 1982.

- NAGAYAMA, Satoshi. *Tabelas de Decisão e Implementação do Gerador I-M-E*. Dissertação (Mestrado em Matemática Aplicada) — Instituto de Matemática e Estatística, Universidade de São Paulo, 1990.

- SETZER, Valdemar W. *Um Sistema Simples para Documentação Semi-Automática de Programas*. 1. ed. São Paulo: USP, 1988.

- VANTHIENEN, J. *A Note on English for Decision Tables Considered Harmful and the Nested IF-THEN-ELSE*. In: *Proceedings of the 2nd International Conference on Software Engineering*. IEEE, 1977. p. 612-618.

- POOCH, Udo W. *Translation of Decision Tables*. 1. ed. New York: John Wiley & Sons, 1974.


Agradecimentos


## Agradecimentos

Primeiramente, agradeço a Deus por me guiar e me dar forças durante toda a jornada de desenvolvimento deste trabalho. Sua presença foi fundamental em cada passo dado ao longo deste caminho.

Aos meus pais, por todo o amor, apoio e incentivo incondicional ao longo de minha vida acadêmica. Sem vocês, este trabalho não teria sido possível. Agradeço por acreditarem em mim, mesmo nos momentos de maior dificuldade.

Ao meu orientador, Prof. Dr. Valdemar W. Setzer, por sua orientação, paciência e pelo conhecimento compartilhado. Suas sugestões e conselhos foram essenciais para o desenvolvimento deste TCC. Sou grato pela oportunidade de ter trabalhado sob sua supervisão e pelo aprendizado que levarei para toda a vida.

Agradeço também aos meus colegas de curso e amigos, que estiveram ao meu lado, oferecendo apoio, palavras de incentivo e momentos de descontração. A convivência com vocês tornou esta caminhada mais leve e agradável.

A todos os professores e funcionários do Instituto de Matemática e Estatística da Universidade de São Paulo, que contribuíram de forma direta ou indireta para minha formação acadêmica, meus sinceros agradecimentos.

Por fim, agradeço a todos que, de alguma forma, fizeram parte desta trajetória, seja com uma palavra amiga, um gesto de apoio, ou uma crítica construtiva. Este trabalho é resultado de um esforço coletivo, e sou eternamente grato a todos que contribuíram para sua realização.


#adicionar imagens de exemplo do output do sidra.py
#adicionar imagens da página no notion sobre cada uma das bases criadas.