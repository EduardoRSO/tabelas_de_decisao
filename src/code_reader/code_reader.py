import os
import re

class CodeReader:
    def __init__(self, path_code: str) -> None:
        self.set_path_code(path_code)
        self.set_code()
        self.set_extracted_decision_tables()

    def __str__(self) -> str:
        return (f' [+] CodeReader:\n'
                f'     path_code: {self.get_path_code()}\n'
                f'     len(code): {len(self.get_code())}\n'
                f'     len(extracted_decision_tables): {len(self.get_extracted_decision_tables())}')

    def set_path_code(self, path_code: str) -> None:
        self.path_code = self._is_valid_path(path_code)

    def set_code(self) -> None:
        self.code = self._is_valid_code()

    def set_extracted_decision_tables(self) -> None:
        self.extracted_decision_tables, self.positions = self._find_decision_tables()

    def get_path_code(self) -> str:
        return self.path_code

    def get_code(self) -> str:
        return self.code

    def get_extracted_decision_tables_positions(self) -> list:
        return self.positions

    def get_extracted_decision_tables(self) -> list:
        return self.extracted_decision_tables

    def get_positions(self) -> list:
        return self.positions

    def _is_valid_path(self, path_code: str) -> str:
        if not os.path.isfile(path_code):
            raise FileNotFoundError(f" [-] O path passado {path_code} não é um arquivo.")
        if not path_code.endswith('.py'):
            raise ValueError(f" [-] O path do arquivo passado {path_code} não é um arquivo python")
        return path_code

    def _is_valid_code(self) -> str:
        with open(self.get_path_code(), 'r') as file:
            content = file.read().strip()
            if len(content) == 0:
                raise ValueError(f' [-] O arquivo passado {self.get_path_code()} está vazio')
            return content

    def _find_decision_tables(self) -> tuple:
        decisions_table_found = []
        positions = []
        pattern = re.compile(r'(#TD decision table.*?#TD end table)', re.DOTALL)

        for match in pattern.finditer(self.get_code()):
            start = match.start()
            end = match.end()
            end_line, end_column = self._get_line_col_from_pos_end(end)
            start_line, start_column = self._get_line_col_from_pos_start(start)
            decision_table = match.group(0)
            decisions_table_found.append(decision_table)
            positions.append(((start_line, start_column), (end_line, end_column)))

        if not decisions_table_found:
            raise ValueError(f' [-] O arquivo não possui nenhuma tabela de decisão')

        return decisions_table_found, positions

    def _get_line_col_from_pos_end(self, pos: int) -> tuple:
        with open(self.get_path_code(), 'r') as file:
            content = file.read()
        
        lines = content[:pos].splitlines()
        line_number = len(lines)
        column_number = len(lines[-1].replace('#TD end table','')) if lines else 0

        return line_number, column_number
    
    
    def _get_line_col_from_pos_start(self, pos: int) -> tuple:
        with open(self.get_path_code(), 'r') as file:
            content = file.read()
        
        lines = content[:pos].splitlines()
        line_number = len(lines)
        column_number = len(lines[-1].replace('#TD decision table','')) if lines else 0

        return line_number -1, column_number