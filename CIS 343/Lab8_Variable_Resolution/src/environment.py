from __future__ import annotations
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
    
    def get_at(self, distance:int, name:Token):
        return self.ancestor(distance).dict.get(name.lexeme)
    
    def ancestor(self:Environment, distance:int) -> Environment:
        environment = self
        for _ in range(distance):
            if isinstance(environment.parent, Environment):
                environment = environment.parent
            else:
                raise RuntimeError("Resolver calculated invalid scope distance")
        return environment

    def assign (self, name:Token, value:Any):
        if name.lexeme in self.dict.keys():
            self.dict.update({name.lexeme:value})
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NogginRuntimeError(name, f"Variable {name.lexeme} has not been declared")
    
    def assign_at(self, distance, name:Token, value:Any):
        self.ancestor(distance).dict[name.lexeme] = value