import os
import logging
import re

class CodeInserter:
    def __init__(self, file_path:str):
        self.initial_spacing = ""  

    def set_initial_spacing(self, lines):
        """Detect the initial_spacing used in the file."""
        for line in lines:
            match = re.match(r"(\s+)", line)
            if match:
                self.initial_spacing = match.group(1)
                break

    def insert(self, file_path, decision_tables, generated_code):
        if not os.path.isfile(file_path):
            logging.error(f"The file {file_path} does not exist.")
            return

        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Detect indentation
        self.detect_indentation(lines)

        # Pattern to identify decision tables
        decision_table_pattern = re.compile(r"(decision_table_\d+)")
        
        new_lines = []
        generated_code_idx = 0

        for line in lines:
            match = decision_table_pattern.search(line)
            if match and generated_code_idx < len(generated_code):
                # Determine the initial spacing of the decision table
                initial_spacing = re.match(r"(\s*)", line).group(1)
                # Add the generated code with matching spacing
                generated_code_lines = generated_code[generated_code_idx].split('\n')
                formatted_code = '\n'.join([initial_spacing + code_line if code_line.strip() else code_line for code_line in generated_code_lines])
                new_lines.append(f"{formatted_code}\n")
                generated_code_idx += 1
            new_lines.append(line)

        with open(file_path, 'w') as file:
            file.writelines(new_lines)

        logging.info(f"Code insertion complete for {file_path}")

# Example usage
if __name__ == "__main__":
    file_path = "path/to/your/file.py"
    decision_tables = ["decision_table_1", "decision_table_2"]
    generated_code = [
        "def generated_function_1():\n    pass",
        "def generated_function_2():\n    pass"
    ]

    code_inserter = CodeInserter()
    code_inserter.insert(file_path, decision_tables, generated_code)
