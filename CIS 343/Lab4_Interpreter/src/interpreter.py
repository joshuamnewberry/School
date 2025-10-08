from typing import Any
from expr import *
from error_handler import *
from visitor import Visitor

class Interpreter(Visitor):
    def __init__(self):
        pass

    def interpret(self, expr):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RuntimeError as error:
            ErrorHandler.error(error, "")

    def evaluate(self, expr:Expr):
        return self.visit(expr)
    
    def stringify(self, input:Any) -> str:
        output = ""
        if input == None:
            return "null"
        if input == True:
            return "true"
        if input == False:
            return "false"
        return str(input)

    def visit_literal(self, expr:Literal):
        return expr.value

    def visit_grouping(self, expr:Grouping):
        return self.evaluate(expr.expression)

    def visit_unary(self, expr:Unary):
        right = self.evaluate(expr.right)
        if expr.operator.lexeme == "-":
            if isinstance(expr.right, float):
                return -expr.right
            else:
                raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        elif expr.operator.lexeme == "!":
            return not self.is_truthy(expr.right)
        raise LoxRuntimeError(expr.operator, f"Unsupported unary operator '{expr.operator.lexeme}'.")

    def visit_binary(self, expr:Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if isinstance(expr.left, str) and isinstance(expr.right, str):
            if expr.operator.lexeme == "+":
                return expr.left + expr.right
            else:
                raise LoxRuntimeError(expr.operator, "Strings can only use the \"+\" operator")
        elif isinstance(expr.left, float) and isinstance(expr.right, float):
            if expr.operator.lexeme == "+":
                return expr.left + expr.right
            if expr.operator.lexeme == "-":
                return expr.left - expr.right
            if expr.operator.lexeme == "*":
                return expr.left * expr.right
            if expr.operator.lexeme == "/":
                return expr.left / expr.right
            raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")

    def is_truthy(self, input:Any) -> bool:
        ## None -- False -- Empty String, List or Tuple -- Zero: False
        ## All else: True
        if input is None:
            return False
        if input == False:
            return False
        if input == "":
            return False
        if input == []:
            return False
        if input == ():
            return False
        if input == 0:
            return False
        return True