import os
import logging
import re

class CodeInserter:
    def __init__(self, file_path: str, file_name: str):
        self.set_default_spacing(" "*4)
        self.set_file_path(file_path)
        self.set_file_name(file_name)
        self.set_file_string()
        self.set_new_file_path()

    def set_default_spacing(self, default_spacing: str):
        self.default_spacing = default_spacing

    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def set_file_name(self, file_name: str):
        self.file_name = file_name

    def set_file_string(self):
        with open(self.file_path, 'r') as file:
            self.file_string = file.readlines()

    def set_new_file_path(self):
        self.new_file_path = os.path.join(os.path.dirname(self.file_path), self.file_name)

    def set_code_spacing(self, code, column):
        code = code.replace('<INITIAL_SPACING>',' '*column)
        code = code.replace('<DEFAULT_SPACING>', self.default_spacing)
        return code

    def insert(self, dt_position_to_code_map: dict):
        for (start, end), generated_code in dt_position_to_code_map.items():
            start_line, start_column = start
            end_line, end_column = end
            for row in range(start_line, end_line):
                self.file_string[row] = ''
            
            new_line = self.set_code_spacing(generated_code, start[1])


            # Replace the old line with the new line
            self.file_string[start_line] = new_line

        # Save the modified content to self.new_file_path
        with open(self.new_file_path, 'w') as file:
            file.writelines(self.file_string)
