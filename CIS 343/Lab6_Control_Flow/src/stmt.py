from expr import *
from noggin_token import *
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
    def __init__(self, name:Token, initializer):
        self.name = name
        self.initializer = initializer

class Assignment(Stmt):
    def __init__(self, name:Token, expression):
        self.name = name
        self.expression = expression