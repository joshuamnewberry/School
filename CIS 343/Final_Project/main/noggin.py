from re import X
import sys
import os
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from error_handler import ErrorHandler
from scanner import Scanner
from parser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter
from environment import Environment
from resolver import Resolver

class Noggin:
    def __init__(self):
        self.environment = Environment()
        self.history = []
        self.clear = lambda: os.system('cls')
        self.previous_environment = []
        self.previous_history = []

    def run_file(self, path):
        with open(path) as f:
            self.run(f.read())
    
    def run_prompt(self):
        try:
            print(">>>>> PNoggin Interactive Shell <<<<<")
            while True:
                self.run(input("> "))
                ErrorHandler.had_error = False
                ErrorHandler.had_runtime_error = False
        except KeyboardInterrupt:
            print("\nExiting PNoggin Interactive Shell.")
    
    def run(self, source):
        if source == "allclear":
            self.clear()
            self.previous_environment.append(self.environment)
            self.environment = Environment()
            self.previous_history.append(self.history)
            self.history = []
            return
        if source == "clear":
            self.clear()
            return
        if source == "undo":
            if len(self.previous_environment) >= 1:
                self.environment = self.previous_environment.pop()
            else:
                print("Cannot revert to a previous environment")
            if len(self.previous_history) >= 1:
                self.history = self.previous_history.pop()
            else:
                print("Cannot revert to a previous history")
            return
        scanner = Scanner(source, len(self.history))
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        if ErrorHandler.had_error:
            return
        interpreter = Interpreter(self.environment)
        resolver = None
        if isinstance(statements, List):
            resolver = Resolver(interpreter)
            resolver.resolve(self.history + statements)
        if ErrorHandler.had_error:
            return
        interpreter.interpret(statements)
        if ErrorHandler.had_error:
            return
        if resolver is not None:
            self.history.append(statements)

if __name__ == "__main__":
    noggin = Noggin()
    if len(sys.argv) > 2:
        print("Usage: Noggin [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        noggin.run_file(sys.argv[1])
    else:
        noggin.run_prompt()