from visitor import Visitor
from expr import *

class AstPrinter(Visitor):
    def print(self, expr):
        return self.visit(expr)

    def visit_binary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary(self, expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_literal(self, expr):
        if expr.value is None:
            return "null"
        return str(expr.value)

    def visit_grouping(self, expr):
        return self.parenthesize("group", expr.expression)

    def parenthesize(self, operator, *exprs):
        parts = [f"({operator}"]
        for e in exprs:
            parts.append(f" {self.visit(e)}")
        parts.append(")")
        return "".join(parts)