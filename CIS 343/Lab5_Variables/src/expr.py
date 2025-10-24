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

class Variable(Expr):
    def __init__(self, name):
        self.name = name

class Block(Expr):
    def __init__(self, statements):
        self.statements = statements