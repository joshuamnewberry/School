from __future__ import annotations
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

class If(Stmt):
    def __init__(self, condition, block:Block, Else:None|If|Else = None):
        self.condition = condition
        self.block = block
        self.Else = Else

class Else(Stmt):
    def __init__(self, block:Block):
        self.block = block

class While(Stmt):
    def __init__(self, condition, block:Block):
        self.condition = condition
        self.block = block