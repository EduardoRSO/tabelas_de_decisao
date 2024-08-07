from src.code_reader.code_reader import CodeReader
from src.decision_table.decision_table import DecisionTable
from src.code_generator.code_generator import CodeGenerator
from src.code_inserter.code_inserter import CodeInserter

class WorkflowController:
    def __init__(self, file_path):
        self.file_path = file_path
        self.code_reader = None
        self.decision_tables_found = []
        self.processed_tables = []
        self.code_generator = None
        self.generated_code = []

    def read_code(self):
        # Initialize and use CodeReader to read the code
        self.code_reader = CodeReader(self.file_path)
        self.decision_tables_found = self.code_reader.get_extracted_decision_tables()

    def process_decision_tables(self):
        # Initialize and use DecisionTable to process each decision table
        self.processed_tables = []
        for table in self.decision_tables_found:
            decision_table = DecisionTable(table)
            self.processed_tables.append(decision_table.process())

    def generate_code(self):
        # Initialize and use CodeGenerator to generate code for each processed table
        self.code_generator = CodeGenerator()
        self.generated_code = []
        for table in self.processed_tables:
            generated_code = self.code_generator.generate(table)
            self.generated_code.append(generated_code)

    def insert_code(self):
        # Initialize and use CodeInserter to insert the generated code into the file
        code_inserter = CodeInserter(self.file_path)
        code_inserter.insert(self.generated_code)

    def execute(self):
        # Execute the entire workflow
        self.read_code()
        self.process_decision_tables()
        self.generate_code()
        self.insert_code()

# Example usage
if __name__ == "__main__":
    file_path = "path/to/your/file.py"
    manager = WorkflowController(file_path)
    manager.execute()
