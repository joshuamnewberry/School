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
        self.globals = environment
        self.environment = self.globals
        self.locals = {}
        class ClockCallable(NogginCallable):
            def call(self, interpreter, arguments):
                return time()
            def arity(self):
                return 0
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

    def evaluate(self, unknown:Any):
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
    
    def resolve(self, expr, depth):
        self.locals[expr] = depth
    
    def lookup_variable(self, name, expr):
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name)
        return self.globals.get(name)
    
    def execute_block(self, statements: list[Stmt], environment):
        previous_env = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.evaluate(stmt)
        finally:
            self.environment = previous_env
    
    def visit_expression(self, expressionObj:Expression):
        self.evaluate(expressionObj.expression)
        return None
    
    def visit_function(self, function:Function):
        self.environment.define(function.name, NogginFunction(function, self.environment))
        return None
    
    def visit_class(self, stmt:Class):
        self.environment.define(stmt.name, None)

        methods = {}
        for method in stmt.methods:
            is_init = method.name.lexeme == "init"
            function = NogginFunction(method, self.environment, is_init)
            methods[method.name.lexeme] = function

        klass = NogginClass(stmt.name.lexeme, methods)
        self.environment.assign(stmt.name, klass)
        return None

    def visit_get(self, expr:Get):
        obj = self.evaluate(expr.object)
        if not isinstance(obj, NogginInstance):
            raise NogginRuntimeError(expr.name, "Only instances have properties")
        return obj.get(expr.name)

    def visit_set(self, expr:Set):
        obj = self.evaluate(expr.object)
        if not isinstance(obj, NogginInstance):
            raise NogginRuntimeError(expr.name, "Only instances have fields")
        value = self.evaluate(expr.value)
        return obj.set(expr.name, value)

    def visit_this(self, expr):
        return self.lookup_variable(expr.keyword, expr)

    def visit_call(self, expr:Call):
        callee = self.evaluate(expr.callee)
        if not hasattr(callee, "call"):
            raise NogginRuntimeError(expr.right_paren, "Can only call functions and classes")
        if len(expr.arguments) != callee.arity():
            raise NogginRuntimeError(expr.right_paren, f"Expected {callee.arity()} arguments but got {len(expr.arguments)}")
        args = [self.evaluate(arg) for arg in expr.arguments]
        return callee.call(self, args)
    
    def visit_return(self, stmt:Return):
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
        return self.lookup_variable(var.name, var)
    
    def visit_assignment(self, expr:Assignment):
        value = self.evaluate(expr.expression)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
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