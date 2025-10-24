from typing import Any, List
from environment import Environment
from expr import *
from error_handler import *
from stmt import *
from visitor import Visitor

class Interpreter(Visitor):
    def __init__(self):
        pass

    def interpret(self, statements:Expression|List[Stmt]):
        try:
            if not isinstance(statements, List):
                expr = self.evaluate(statements)
                print(self.stringify(expr))
                return
            for stmt in statements:
                self.evaluate(stmt)
        except RuntimeError as error:
            ErrorHandler.error(error, "")

    def evaluate(self, unknown):
        return self.visit(unknown)
    
    def stringify(self, input:Any) -> str:
        output = ""
        if input == None:
            return "null"
        if input == True:
            return "true"
        if input == False:
            return "false"
        return str(input)
    
    def visit_expression(self, expressionObj:Expression):
        self.evaluate(expressionObj.expression)
        return None
    
    def visit_print(self, printObj:Print):
        res = ""
        for expr in printObj.exprList:
            res += self.stringify(self.evaluate(expr)) + " "
        print(res.strip())
        return None
    
    def visit_def(self, defObj:Def):
        pass

    def visit_variable(self, var:Variable):
        pass

    def visit_assignment(self, assignment:Assignment):
        pass

    def visit_block(self, block:Block):
        pass

    def visit_literal(self, expr:Literal):
        return expr.value

    def visit_grouping(self, expr:Grouping):
        return self.evaluate(expr.expression)

    def visit_unary(self, expr:Unary):
        right = self.evaluate(expr.right)
        if expr.operator.lexeme == "-":
            if isinstance(right, float):
                return -right
            else:
                raise NogginRuntimeError(expr.operator, "Operand must be a number")
        elif expr.operator.lexeme == "!":
            return not self.is_truthy(right)
        raise NogginRuntimeError(expr.operator, f"Unsupported unary operator '{expr.operator.lexeme}'.")

    def visit_binary(self, expr:Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if isinstance(left, str) and isinstance(right, str):
            if expr.operator.lexeme == "+":
                return left + right
            else:
                raise NogginRuntimeError(expr.operator, "Strings can only use the \"+\" operator")
        elif isinstance(left, float) and isinstance(right, float):
            if expr.operator.lexeme == "+":
                return left + right
            if expr.operator.lexeme == "-":
                return left - right
            if expr.operator.lexeme == "*":
                return left * right
            if expr.operator.lexeme == "/":
                if right == 0:
                    raise NogginRuntimeError(expr.right, "Cannot divide by zero")
                return left / right
            if expr.operator.lexeme == "==":
                return left == right
            if expr.operator.lexeme == "!=":
                return left != right
            if expr.operator.lexeme == ">":
                return left > right
            if expr.operator.lexeme == ">=":
                return left >= right
            if expr.operator.lexeme == "<":
                return left < right
            if expr.operator.lexeme == "<=":
                return left <= right
            raise NogginRuntimeError(expr.operator, "Unsupported binary operator for two floats")
        elif expr.operator.lexeme == "==":
            return left == right
        elif expr.operator.lexeme == "!=":
            return left != right
        raise NogginRuntimeError(expr.operator, f"Unsupported binary operation '{expr.operator.lexeme}' for operands of type {type(left).__name__} and {type(right).__name__}.")

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