#1[
#1 TITULO: EXTRACTOR
#1 AUTOR: EDUARDO RIBEIRO SILVA DE OLIVEIRA
#1 DATA: 25/09/2024
#1 VERSAO: 1
#1 FINALIDADE: REALIZA A EXTRAÇÃO DE DOCUMENTAÇÃO E GERAÇÃO DE PDF A PARTIR DE ARQUIVOS DE CÓDIGO
#1 ENTRADAS: CAMINHO DO ARQUIVO/DIRETÓRIO DE ENTRADA, CAMINHO DO ARQUIVO DE SAÍDA, MODO DE EXECUÇÃO
#1 SAIDAS: ARQUIVO PDF COM A DOCUMENTAÇÃO EXTRAÍDA
#1 ROTINAS CHAMADAS: _GET_ALL_FILES, EXECUTE, _EXTRACT_BY_MODE, EXTRAI_NIVEL_1, EXTRAI_NIVEL_2, EXTRAI_NIVEL_3, _BUILD_HTML, CONVERT_HTML_TO_PDF
#1]

import os
import re
import pdfkit
from typing import List

NV_1 = r'^ *#1.*'
NV_2 = r'^ *#1.*|^ *#2.*'

class Extractor:
    EXCLUDED_PATHS = ['.git', '__pycache__', 'node_modules', '.DS_Store', 'Thumbs.db', 'venv']
    EXCLUDED_SUFFIXES = ['.pdf', '__init__.py']

    #1[
    #1 ROTINA: __INIT__
    #1 FINALIDADE: INICIALIZA AS VARIÁVEIS DA CLASSE EXTRACTOR
    #1 ENTRADAS: CAMINHO DO ARQUIVO/DIRETÓRIO DE ENTRADA, CAMINHO DO ARQUIVO DE SAÍDA, MODO DE EXECUÇÃO
    #1 DEPENDENCIAS: OS
    #1 CHAMADO POR: EXTRACTOR
    #1 CHAMA: _GET_ALL_FILES (SE O CAMINHO FOR UM DIRETÓRIO)
    #1]
    #2[
    #2 PSEUDOCODIGO DE: __init__
    def __init__(self, input_path: str, output_path: str, execution_mode: int = 3):
        #2 ARMAZENA O CAMINHO DE ENTRADA E O CAMINHO DE SAÍDA
        self.input_path = input_path
        self.output_path = output_path
        #2 DEFINE O MODO DE EXECUÇÃO PADRÃO COMO 3
        self.execution_mode = execution_mode
        #2 VERIFICA SE O CAMINHO DE ENTRADA É UM ARQUIVO ÚNICO
        self.one_file = os.path.isfile(input_path)
        #2 GERA UMA LISTA DE ARQUIVOS A SEREM PROCESSADOS (SE FOR UM DIRETÓRIO)
        self.file_path_list = [input_path] if self.one_file else self._get_all_files(input_path)
        #2 INICIALIZA UM DICIONÁRIO PARA ARMAZENAR A DOCUMENTAÇÃO
        self.documentation = {}
        #2 INICIALIZA UMA STRING VAZIA PARA O CONTEÚDO HTML
        self.html_content = ''  # Armazenará o HTML gerado
    #2]

    #1[
    #1 ROTINA: _GET_ALL_FILES
    #1 FINALIDADE: OBTÉM TODOS OS ARQUIVOS DENTRO DE UM DIRETÓRIO, EXCLUINDO OS CAMINHOS E SUFIXOS DEFINIDOS
    #1 ENTRADAS: CAMINHO DO DIRETÓRIO
    #1 DEPENDENCIAS: OS, EXCLUDED_PATHS, EXCLUDED_SUFFIXES
    #1 CHAMADO POR: __INIT__
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _get_all_files
    def _get_all_files(self, path: str) -> List[str]:
        #2 CRIA UM CONJUNTO PARA ARMAZENAR A LISTA DE ARQUIVOS
        file_list = set()
        #2 PERCORRE AS PASTAS RECUSIVAMENTE E LISTA ARQUIVOS
        for root, dirs, files in os.walk(path):
        #2 REMOVE OS DIRETÓRIOS EXCLUÍDOS DA LISTA DE DIRETÓRIOS
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_PATHS]
        #2 PARA CADA ARQUIVO, ADICIONA À LISTA SE NÃO ESTIVER NAS EXCLUSÕES
            for file in files:
                if file not in self.EXCLUDED_PATHS and not file.endswith(tuple(self.EXCLUDED_SUFFIXES)):
                    file_list.add(os.path.join(root, file))
        #2 RETORNA A LISTA DE ARQUIVOS COMO UMA LISTA SIMPLES
        return list(file_list)
    #2]

    #1[
    #1 ROTINA: EXECUTE
    #1 FINALIDADE: EXECUTA O PROCESSO DE EXTRAÇÃO E GERAÇÃO DE DOCUMENTAÇÃO
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: OS, _EXTRACT_BY_MODE, _BUILD_HTML, CONVERT_HTML_TO_PDF
    #1 CHAMADO POR: __MAIN__
    #1 CHAMA: _EXTRACT_BY_MODE, _BUILD_HTML, CONVERT_HTML_TO_PDF
    #1]
    #2[
    #2 PSEUDOCODIGO DE: execute
    def execute(self):
        #2 PARA CADA ARQUIVO NA LISTA, LÊ O CONTEÚDO E ARMAZENA A DOCUMENTAÇÃO
        for file_path in self.file_path_list:
            with open(file_path, 'r') as file:
        #2 LÊ O CONTEÚDO DO ARQUIVO
                content = file.read()
        #2 ARMAZENA A DOCUMENTAÇÃO EXTRAÍDA NO DICIONÁRIO
                self.documentation[file_path] = self._extract_by_mode(content)
        #2 CONSTRÓI O CONTEÚDO HTML
        self._build_html()
        #2 CONVERTE O HTML GERADO PARA PDF
        self.convert_html_to_pdf()
    #2]

    #1[
    #1 ROTINA: _EXTRACT_BY_MODE
    #1 FINALIDADE: EXTRAI A DOCUMENTAÇÃO DE ACORDO COM O MODO DE EXECUÇÃO SELECIONADO
    #1 ENTRADAS: CONTEÚDO DO ARQUIVO
    #1 DEPENDENCIAS: EXTRAI_NIVEL_1, EXTRAI_NIVEL_2, EXTRAI_NIVEL_3
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: EXTRAI_NIVEL_1, EXTRAI_NIVEL_2, EXTRAI_NIVEL_3
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _extract_by_mode
    def _extract_by_mode(self, content: str) -> List[str]:
        #2 SE O MODO DE EXECUÇÃO FOR 1, EXTRAI APENAS O NÍVEL 1
        if self.execution_mode == 1:
            return self.extrai_nivel_1(content)
        #2 SE O MODO DE EXECUÇÃO FOR 2, EXTRAI APENAS O NÍVEL 2
        elif self.execution_mode == 2:
            return self.extrai_nivel_2(content)
        #2 SE O MODO DE EXECUÇÃO FOR 3, EXTRAI TODO O CONTEÚDO
        elif self.execution_mode == 3:
            return self.extrai_nivel_3(content)
        #2 LEVANTA UM ERRO SE O MODO DE EXECUÇÃO NÃO FOR VÁLIDO
        else:
            raise ValueError("Modo de execução inválido. Use 1, 2 ou 3.")
    #2]

    #1[
    #1 ROTINA: EXTRAI_NIVEL_1
    #1 FINALIDADE: EXTRAI A DOCUMENTAÇÃO DO NÍVEL 1 (CABECEALHOS)
    #1 ENTRADAS: CONTEÚDO DO ARQUIVO
    #1 DEPENDENCIAS: RE, NV_1
    #1 CHAMADO POR: _EXTRACT_BY_MODE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: extrai_nivel_1
    def extrai_nivel_1(self, arquivo: str) -> List[str]:
        #2 ENCONTRA TODAS AS OCORRÊNCIAS QUE CORRESPONDEM AO PADRÃO DE NÍVEL 1
        return '\n'.join(re.findall(NV_1, arquivo, re.MULTILINE))
    #2]

    #1[
    #1 ROTINA: EXTRAI_NIVEL_2
    #1 FINALIDADE: EXTRAI A DOCUMENTAÇÃO DO NÍVEL 2 (LINHA A LINHA)
    #1 ENTRADAS: CONTEÚDO DO ARQUIVO
    #1 DEPENDENCIAS: RE, NV_2
    #1 CHAMADO POR: _EXTRACT_BY_MODE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: extrai_nivel_2
    def extrai_nivel_2(self, arquivo: str) -> List[str]:
        #2 ENCONTRA TODAS AS OCORRÊNCIAS QUE CORRESPONDEM AO PADRÃO DE NÍVEL 2
        return '\n'.join(re.findall(NV_2, arquivo, re.MULTILINE))
    #2]

    #1[
    #1 ROTINA: EXTRAI_NIVEL_3
    #1 FINALIDADE: EXTRAI TODO O CONTEÚDO SEM FILTRAGEM (NÍVEL 3)
    #1 ENTRADAS: CONTEÚDO DO ARQUIVO
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: _EXTRACT_BY_MODE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: extrai_nivel_3
    def extrai_nivel_3(self, arquivo: str) -> str:
        #2 RETORNA TODO O CONTEÚDO DO ARQUIVO SEM NENHUMA FILTRAGEM
        return arquivo
    #2]

    #1[
    #1 ROTINA: _BUILD_HTML
    #1 FINALIDADE: CONSTRÓI O CONTEÚDO HTML A PARTIR DA DOCUMENTAÇÃO EXTRAÍDA
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: N/A
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: _build_html
    def _build_html(self):
        #2 INICIALIZA O CABEÇALHO HTML E O ESTILO PARA A FORMATAÇÃO DA TABELA
        self.html_content = '''
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                table {
                    width: 595px;  /* Largura de uma folha A4 em pontos */
                    border-collapse: collapse;
                    table-layout: fixed;  /* Garante que a tabela respeite a largura */
                    word-wrap: break-word;  /* Força a quebra de palavra se necessário */
                }
                th, td {
                    border: 1px solid black;
                    padding: 10px;
                    overflow-wrap: break-word;  /* Quebra automaticamente palavras longas */
                    word-break: break-word;  /* Alternativa para garantir quebra de palavras */
                }
                pre {
                    white-space: pre-wrap;  /* Preserve espaços e quebre linhas automaticamente */
                    word-wrap: break-word;  /* Força a quebra de palavra se necessário */
                }
                body {
                    margin: 0 auto;
                    width: 595px;  /* Alinha o conteúdo no centro, com largura fixa de A4 */
                }
            </style>
        </head>
        <body>\n
        '''
        #2 PARA CADA ARQUIVO DOCUMENTADO, CRIA UMA TABELA COM O NOME DO ARQUIVO E A DOCUMENTAÇÃO EXTRAÍDA
        for file_name, doc in self.documentation.items():
            self.html_content += '<table>\n'
            self.html_content += f'<tr><th style="text-align: center;">Nome do Arquivo</th></tr>\n'
            self.html_content += f'<tr><td style="text-align: left;">{os.path.basename(file_name)}</td></tr>\n'
            self.html_content += '<tr><th style="text-align: center;">Documentação</th></tr>\n'
            doc_lines = doc.split('\\n')
            self.html_content += f'<tr><td style="text-align: left;"><pre>{"".join(doc_lines)}</pre></td></tr>\n'
            self.html_content += '</table><br><br>\n'
            #2 FINALIZA O CONTEÚDO HTML
        self.html_content += '</body></html>'
        #2]

    #1[
    #1 ROTINA: CONVERT_HTML_TO_PDF
    #1 FINALIDADE: CONVERTE O CONTEÚDO HTML GERADO EM UM ARQUIVO PDF
    #1 ENTRADAS: N/A
    #1 DEPENDENCIAS: PDFKIT
    #1 CHAMADO POR: EXECUTE
    #1 CHAMA: N/A
    #1]
    #2[
    #2 PSEUDOCODIGO DE: convert_html_to_pdf
    def convert_html_to_pdf(self):
        #2 DEFINE OPÇÕES PARA A CONVERSÃO, UTILIZANDO A CODIFICAÇÃO UTF-8
        options = {
             'encoding': 'UTF-8',  # Define a codificação UTF-8 ao gerar o PDF
        }
        #2 CONVERTE O CONTEÚDO HTML PARA PDF E SALVA NO CAMINHO DE SAÍDA
        pdfkit.from_string(self.html_content, self.output_path, options=options)
    #2]

#1[
#1 ROTINA: __MAIN__
#1 FINALIDADE: PONTO DE ENTRADA PRINCIPAL DO PROGRAMA, COLETA INFORMAÇÕES DO USUÁRIO E EXECUTA A EXTRAÇÃO
#1 ENTRADAS: NENHUMA (SOLICITAÇÃO DE INPUT DO USUÁRIO)
#1 DEPENDENCIAS: EXTRACTOR, INPUT
#1 CHAMADO POR: N/A
#1 CHAMA: EXTRACTOR.__INIT__, EXTRACTOR.EXECUTE
#1]
#2[
#2 PSEUDOCODIGO DE: __main__
if __name__ == '__main__':
    #2 SOLICITA O CAMINHO DO ARQUIVO OU DIRETÓRIO
    input_path = input('Digite o caminho do arquivo ou diretório de entrada: ')
    #2 SOLICITA O NÍVEL DE EXTRAÇÃO (1, 2 OU 3)
    execution_mode = int(input('Digite o nível de extração (1, 2 ou 3): '))
    #2 SOLICITA O CAMINHO PARA SALVAR O ARQUIVO PDF DE SAÍDA
    output_path = input('Digite o caminho para salvar o arquivo PDF de saída: ')
    #2 CRIA UMA INSTÂNCIA DA CLASSE EXTRACTOR
    extractor = Extractor(input_path=input_path, output_path=output_path, execution_mode=execution_mode)
    #2 EXECUTA O PROCESSO DE EXTRAÇÃO E GERAÇÃO DO PDF
    extractor.execute()
#2]

