# Projeto de Extração e Processamento de TDs

Este repositório contém um sistema para extração e processamento de Documentação Técnica (TDs) em arquivos Python. Ele inclui um extrator de documentação e um pré-processador de TDs, além de exemplos e documentação relacionada.

## Estrutura do Repositório

A estrutura de diretórios do projeto está organizada da seguinte forma:

/
├── docs/                       # Arquivos .pdf usados na monografia
├── exemplos/                   # Exemplos de documentação gerada pelo extrator
│   ├── programa_auto_documentado/   # Exemplo de programa auto documentado
│   ├── tds_html/               # Versão em .html de uma TD
│   ├── tds_traduzidas/         # Exemplos de arquivos Python com TDs e seus arquivos pré-processados
├── src/                        # Códigos necessários para o funcionamento do pré-processador de TDs
├── extrator_de_documentacao.py  # Extrator de documentação
├── input_extrator_de_documentacao # Exemplo de input para o extrator
├── main.py                      # Pré-processador de arquivos Python com TDs
├── input_preprocessador         # Exemplo de input para o pré-processador
├── tese.pdf                     # Tese relacionada ao projeto
├── poster.pdf                   # Poster de apresentação do projeto
├── index.html                   # Página do site na rede Linux do IME

## Como Usar

1. **Executar o extrator de documentação:**
   ```sh
   python extrator_de_documentacao.py input_extrator_de_documentacao
   ```

2. **Executar o pré-processador de TDs:**
   ```sh
   python main.py input_preprocessador
   ```

## Contato

Para mais informações, entre em contato ou consulte os arquivos da pasta `docs/` para detalhes da monografia e referências técnicas.
```

