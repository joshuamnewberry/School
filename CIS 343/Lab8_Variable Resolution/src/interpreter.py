from typing import Any, List
from environment import *
from expr import *
from error_handler import *
from stmt import *
from visitor import *
from callable import *
from time import time

class Interpreter(Visitor):
    def __init__(self, environment=None):
        if environment is None:
            environment = Environment()
        self.environment = environment
        class ClockCallable(NogginCallable):
            def call(self, interpreter, arguments):
                return time()
            def arity(self):
                return 
            def __str__(self):
                return "<native fn>"
        class MinCallable(NogginCallable):
            def call(self, interpreter, arguments):
                return min(arguments[0], arguments[1])
            def arity(self):
                return 2
            def __str__(self):
                return "<native fn>"
        class MaxCallable(NogginCallable):
            def call(self, interpreter, arguments):
                return max(arguments[0], arguments[1])
            def arity(self):
                return 2
            def __str__(self):
                return "<native fn>"
        self.environment.define(Token(TokenType.IDENTIFIER, "clock", "clock", None), ClockCallable())
        self.environment.define(Token(TokenType.IDENTIFIER, "min", "min", None), MinCallable())
        self.environment.define(Token(TokenType.IDENTIFIER, "max", "max", None), MaxCallable())

    def interpret(self, statements:Expression|List[Stmt]):
        try:
            if not isinstance(statements, List):
                expr = self.evaluate(statements.expression)
                print(expr)
                return
            for stmt in statements:
                self.evaluate(stmt)
        except NogginRuntimeError as error:
            ErrorHandler.error(error, "")

    def evaluate(self, unknown):
        return self.visit(unknown)
    
    def stringify(self, input:Any) -> str:
        output = ""
        if input == None:
            return "null"
        if isinstance(input, bool):
            if input == True:
                return "true"
            if input == False:
                return "false"
        return str(input)
    
    def visit_expression(self, expressionObj:Expression):
        self.evaluate(expressionObj.expression)
        return None
    
    def visit_function(self, function:Function):
        self.environment.define(function.name, NogginFunction(function))

    def visit_call(self, call:Call):
        callee = self.evaluate(call.callee)
        if not isinstance(callee, NogginCallable):
            raise NogginRuntimeError(call.right_paren, "Expected a defined function")
        expected = callee.arity()
        if expected is not None and expected != len(call.arguments):
            raise NogginRuntimeError(call.right_paren, f"Expected {expected} arguments but got {len(call.arguments)}.")
        arguments = [self.evaluate(arg) for arg in call.arguments]
        return callee.call(self, arguments)
    
    def visit_return(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise NogginReturn(value)
    
    def visit_print(self, printObj:Print):
        res = ""
        for expr in printObj.exprList:
            res += self.stringify(self.evaluate(expr)) + " "
        print(res)
        return None
    
    def visit_def(self, defObj:Def):
        name = defObj.name
        value = None
        if defObj.initializer is not None:
            value = self.evaluate(defObj.initializer)
        self.environment.define(name, value)
        return None

    def visit_variable(self, var:Variable):
        name = var.name
        return self.environment.get(name)

    def visit_assignment(self, assign:Assignment):
        name = assign.name.lexeme
        value = self.evaluate(assign.expression)
        self.environment.assign(assign.name, value)
        return None
    
    def visit_if(self, If:If):
        if self.is_truthy(self.evaluate(If.condition)):
            self.evaluate(If.block)
        elif If.Else is not None:
            if isinstance(If.Else, Else):
                self.evaluate(If.Else.block)
            else:
                self.visit_if(If.Else)
        return None
    
    def visit_while(self, While:While):
        while(self.is_truthy(self.evaluate(While.condition))):
            self.evaluate(While.block)
        return None

    def visit_block(self, block:Block):
        previous = self.environment
        self.environment = Environment(previous)
        try:
            for stmt in block.statements:
                self.evaluate(stmt)
        finally:
            self.environment = previous
        return None

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
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
            right = self.evaluate(expr.right)
            if self.is_truthy(right):
                return right
            return False
        elif expr.operator.type == TokenType.AND:
            if self.is_truthy(left):
                right = self.evaluate(expr.right)
                if self.is_truthy(right):
                    return True
            return False
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