import sys
import os
from src.workflow_controller import WorkflowController

def start(file_path:str, file_name:str):
    manager = WorkflowController(file_path, file_name)
    manager.execute()

def main():
    if len(sys.argv) > 1:
        file_path, file_name = sys.argv[1], sys.argv[2]
    else:
        file_path = input("Please enter the file path: ")
        file_name = input("Please enter the file name: ")

    if not file_path.endswith('.py'):
        print("Error: The file must have a .py extension.")
        return
    
    if not os.path.isfile(file_path):
        print("Error: The file does not exist.")
        return

    start(file_path, file_name)

if __name__ == "__main__":
    main()
