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