import os
import logging
import re

class CodeInserter:
    def __init__(self, file_path: str, file_name: str):
        self.set_initial_spacing("")
        self.set_file_path(file_path)
        self.set_file_name(file_name)
        self.set_file_string()
        self.set_new_file_path()

    def set_initial_spacing(self, initial_spacing: str):
        self.initial_spacing = initial_spacing

    def set_file_path(self, file_path: str):
        self.file_path = file_path

    def set_file_name(self, file_name: str):
        self.file_name = file_name

    def set_file_string(self):
        with open(self.file_path, 'r') as file:
            self.file_string = file.readlines()

    def set_new_file_path(self):
        self.new_file_path = os.path.join(os.path.dirname(self.file_path), self.file_name)

    def insert(self, dt_position_to_code_map: dict):
        for (line, column), code_snippet in dt_position_to_code_map.items():
            # Adjust the line index (list is zero-based, file is one-based)
            line_index = line - 1

            # Get the current line content
            current_line = self.file_string[line_index]

            # Insert the code_snippet at the specified column index
            new_line = current_line[:column] + code_snippet + current_line[column:]

            # Replace the old line with the new line
            self.file_string[line_index] = new_line

        # Save the modified content to self.new_file_path
        with open(self.new_file_path, 'w') as file:
            file.writelines(self.file_string)
