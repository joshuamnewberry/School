import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from error_handler import ErrorHandler
from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter

class Noggin:
    def run_file(self, path):
        with open(path) as f:
            self.run(f.read())
    
    def run_prompt(self):
        try:
            print(">>>>> PLox Interactive Shell <<<<<")
            while True:
                self.run(input("> "))
                ErrorHandler.had_error = False
                ErrorHandler.had_runtime_error = False
        except KeyboardInterrupt:
            print("\nExiting PLox Interactive Shell.")
    
    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        if (ErrorHandler.had_error):
            return
        interpreter = Interpreter()
        interpreter.interpret(expression)

if __name__ == "__main__":
    noggin = Noggin()
    if len(sys.argv) > 2:
        print("Usage: lox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        noggin.run_file(sys.argv[1])
    else:
        noggin.run_prompt()