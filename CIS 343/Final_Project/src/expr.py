from __future__ import annotations
from noggin_token import *
from typing import List

class Expr:
    pass

class Binary(Expr):
    def __init__(self, left, operator:Token, right):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expr):
    def __init__(self, expression:Expr):
        self.expression = expression

class Literal(Expr):
    def __init__(self, value):
        self.value = value

class Unary(Expr):
    def __init__(self, operator:Token, right):
        self.operator = operator
        self.right = right

class Call(Expr):
    def __init__(self, callee:Get|Variable|Call, arguments:List, right_paren:Token):
        self.callee = callee
        self.arguments = arguments
        self.right_paren = right_paren

class Get(Expr):
    def __init__(self, object, name:Token):
        self.object = object
        self.name = name

class Set(Expr):
    def __init__(self, object, name:Token, value):
        self.object = object
        self.name = name
        self.value = value

class This(Expr):
    def __init__(self, keyword:Token):
        self.keyword = keyword

class Variable(Expr):
    def __init__(self, name:Token):
        self.name = name

class Block(Expr):
    def __init__(self, statements:List):
        self.statements = statements