from ast import Expr
from typing import List

class Stmt:
    pass

class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

class Print(Stmt):
    def __init__(self, exprList:List):
        self.exprList = exprList

class Def(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

class Assignment(Stmt):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression