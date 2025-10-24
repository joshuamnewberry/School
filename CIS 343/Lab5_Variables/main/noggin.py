import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from error_handler import ErrorHandler
from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter
from environment import Environment

class Noggin:
    def run_file(self, path):
        environment = Environment()
        with open(path) as f:
            self.run(f.read(), environment)
    
    def run_prompt(self):
        environment = Environment()
        try:
            print(">>>>> PNoggin Interactive Shell <<<<<")
            while True:
                self.run(input("> "), environment)
                ErrorHandler.had_error = False
                ErrorHandler.had_runtime_error = False
        except KeyboardInterrupt:
            print("\nExiting PNoggin Interactive Shell.")
    
    def run(self, source, environment):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        interpreter = Interpreter(environment)
        interpreter.interpret(statements)

if __name__ == "__main__":
    noggin = Noggin()
    if len(sys.argv) > 2:
        print("Usage: Noggin [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        noggin.run_file(sys.argv[1])
    else:
        noggin.run_prompt()
