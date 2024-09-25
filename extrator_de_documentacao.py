import os
import re
import pdfkit
from typing import List

NV_1 = r'^ *#1.*'
NV_2 = r'^ *#2.*'

class Extractor:
    EXCLUDED_PATHS = ['.git', '__pycache__', 'node_modules', '.DS_Store', 'Thumbs.db']
    EXCLUDED_SUFFIXES = ['.pdf', '__init__.py']

    def __init__(self, input_path: str, output_path: str, execution_mode: int = 3):
        self.input_path = input_path
        self.output_path = output_path
        self.execution_mode = execution_mode
        self.one_file = os.path.isfile(input_path)
        self.file_path_list = [input_path] if self.one_file else self._get_all_files(input_path)
        self.documentation = {}
        self.html_content = ''  # Armazenará o HTML gerado

    def _get_all_files(self, path: str) -> List[str]:
        """Acessa recursivamente as pastas e retorna a lista de arquivos, ignorando os que estão em EXCLUDED_PATHS."""
        file_list = set()
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in self.EXCLUDED_PATHS]
            for file in files:
                if file not in self.EXCLUDED_PATHS and not file.endswith(tuple(self.EXCLUDED_SUFFIXES)):
                    file_list.add(os.path.join(root, file))
        return list(file_list)

    def execute(self):
        """Executa a extração e constrói a tabela HTML."""
        for file_path in self.file_path_list:
            with open(file_path, 'r') as file:
                content = file.read()
                self.documentation[file_path] = self._extract_by_mode(content)
        self._build_html()
        self.convert_html_to_pdf()

    def _extract_by_mode(self, content: str) -> List[str]:
        """Extrai a documentação conforme o modo de execução."""
        if self.execution_mode == 1:
            return self.extrai_nivel_1(content)
        elif self.execution_mode == 2:
            return self.extrai_nivel_2(content)
        elif self.execution_mode == 3:
            return self.extrai_nivel_3(content)
        else:
            raise ValueError("Modo de execução inválido. Use 1, 2 ou 3.")

    def extrai_nivel_1(self, arquivo: str) -> List[str]:
        return '\n'.join(re.findall(NV_1, arquivo, re.MULTILINE))

    def extrai_nivel_2(self, arquivo: str) -> List[str]:
        return '\n'.join(re.findall(NV_2, arquivo, re.MULTILINE))

    def extrai_nivel_3(self, arquivo: str) -> str:
        return arquivo

    def _build_html(self):
        """Constrói um arquivo HTML com tabelas para cada arquivo e sua documentação."""
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
        for file_name, doc in self.documentation.items():
            # Inicia a tabela com estilo de borda e largura A4
            self.html_content += '<table>\n'
            
            # Centraliza o header do nome do arquivo
            self.html_content += f'<tr><th style="text-align: center;">Nome do Arquivo</th></tr>\n'
            
            # Nome do arquivo (alinhado à esquerda)
            self.html_content += f'<tr><td style="text-align: left;">{os.path.basename(file_name)}</td></tr>\n'
            
            # Centraliza o header da documentação
            self.html_content += '<tr><th style="text-align: center;">Documentação</th></tr>\n'
            
            # Divide o texto da documentação por quebras de linha e preserva a formatação
            doc_lines = doc.split('\\n')
            self.html_content += f'<tr><td style="text-align: left;"><pre>{"".join(doc_lines)}</pre></td></tr>\n'
            
            # Fecha a tabela e adiciona espaçamento entre as tabelas
            self.html_content += '</table><br><br>\n'
        self.html_content += '</body></html>'

    def convert_html_to_pdf(self):
        """Converte o conteúdo HTML armazenado para um arquivo PDF usando pdfkit com UTF-8."""
        options = {
             'encoding': 'UTF-8',  # Define a codificação UTF-8 ao gerar o PDF
        }
        pdfkit.from_string(self.html_content, self.output_path, options=options)


if __name__ == '__main__':
    input_path = input('Digite o caminho do arquivo ou diretório de entrada: ')
    execution_mode = int(input('Digite o nível de extração (1, 2 ou 3): '))
    output_path = input('Digite o caminho para salvar o arquivo PDF de saída: ')

    extractor = Extractor(input_path=input_path, output_path=output_path, execution_mode=execution_mode)
    extractor.execute()
