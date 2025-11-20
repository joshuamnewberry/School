from typing import List
from stmt import Function
from environment import Environment
from error_handler import *

class NogginCallable:
    # call the function with given arguments
    def call(self, interpreter, arguments):
        raise NotImplementedError
        
    # return the number of parameters the function takes
    def arity(self):
        raise NotImplementedError
    
    # return a string representation of the function
    def __str__(self):
        raise NotImplementedError

class NogginFunction(NogginCallable):
    def __init__(self, declaration:Function):
        self.declaration = declaration

    def call(self, interpreter, arguments:List):
        previous = interpreter.environment
        # Create a new environment for the function call
        interpreter.environment = Environment(previous)
        # Define all local variables
        for i in range(0, self.arity()):
            interpreter.environment.define(self.declaration.parameters[i], arguments[i])
        try:
            for stmt in self.declaration.block.statements:
                interpreter.evaluate(stmt)
        except NogginReturn as r:
            interpreter.environment = previous
            return r.value
        finally:
            interpreter.environment = previous
        return None

    def arity(self):
        return len(self.declaration.parameters)
    
    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"
    
class NogginClass(NogginCallable):
    def __init__(self):
        raise NotImplementedError
    
    # call the function with given arguments
    def call(self, interpreter, arguments):
        raise NotImplementedError
        
    # return the number of parameters the function takes
    def arity(self):
        raise NotImplementedError
    
    # return a string representation of the function
    def __str__(self):
        raise NotImplementedError