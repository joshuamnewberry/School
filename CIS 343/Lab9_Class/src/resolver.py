from ast import And
from enum import Enum
from expr import Block
from visitor import Visitor
from error_handler import ErrorHandler
from interpreter import Interpreter
from stmt import *

class FunctionType(Enum):
    NONE = 0
    FUNCTION = 1

class Resolver(Visitor):
    def __init__(self, interpreter:Interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE

    def resolve(self, stmt_expr):
        if stmt_expr is None:
            return
        if isinstance(stmt_expr, list):
            for statement in stmt_expr:
                self.resolve(statement)
        else:
            return self.visit(stmt_expr)

    def declare(self, name):
        # global scope omitted
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = False

    def define(self, name):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr, name_token):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name_token.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def visit_block(self, stmt:Block):
        self.scopes.append({})
        self.resolve(stmt.statements)
        self.scopes.pop()
        return None

    def visit_def(self, stmt:Def):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)
        return None

    def visit_function(self, stmt:Function):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt)
        return None

    def resolve_function(self, function:Function):
        enclosing = self.current_function
        self.current_function = FunctionType.FUNCTION
        self.scopes.append({})
        for param in function.parameters:
            self.declare(param)
            self.define(param)
        self.resolve(function.block.statements)
        self.scopes.pop()
        self.current_function = enclosing
        return None

    def visit_expression(self, stmt:Expression):
        self.resolve(stmt.expression)
        return None

    def visit_print(self, stmt:Print):
        self.resolve(stmt.exprList)
        return None

    def visit_if(self, stmt:If):
        self.resolve(stmt.condition)
        self.resolve(stmt.block)
        if stmt.Else is not None:
            self.resolve(stmt.Else)
        return None

    def visit_while(self, stmt:While):
        self.resolve(stmt.condition)
        self.resolve(stmt.block)
        return None

    def visit_return(self, stmt:Return):
        if self.current_function is FunctionType.NONE:
            ErrorHandler.error(stmt.keyword, "Cannot return from top-level code.")
        if stmt.value is not None:
            self.resolve(stmt.value)
        return None

    def visit_binary(self, expr:Binary):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None

    def visit_call(self, expr:Call):
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)
        return None

    def visit_grouping(self, expr:Grouping):
        self.resolve(expr.expression)
        return None

    def visit_literal(self, expr:Literal):
        return None

    def visit_unary(self, expr:Unary):
        self.resolve(expr.right)
        return None

    def visit_variable(self, expr:Variable):
        if (len(self.scopes) != 0 and
            expr.name.lexeme in self.scopes[-1] and
            self.scopes[-1][expr.name.lexeme] is False):
            ErrorHandler.error(expr.name, "Cannot read local variable in its own initializer.")
        self.resolve_local(expr, expr.name)
        return None

    def visit_assignment(self, expr:Assignment):
        self.resolve(expr.expression)
        self.resolve_local(expr, expr.name)
        return None