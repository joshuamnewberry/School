from noggin_token import *
from error_handler import *
from typing import Any

class Environment:
    def __init__(self, parent=None):
        self.dict = {}
        self.parent = parent

    def define (self, name:Token, value:Any):
        self.dict[name.lexeme] = value

    def get (self, name:Token):
        if name.lexeme in self.dict.keys():
            return self.dict.get(name.lexeme)
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NogginRuntimeError(name, f"Variable {name.lexeme} has no value (no variable declaration)")

    def assign (self, name:Token, value):
        if name.lexeme in self.dict.keys():
            self.dict.update({name.lexeme:value})
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NogginRuntimeError(name, f"Variable {name.lexeme} has not been declared")