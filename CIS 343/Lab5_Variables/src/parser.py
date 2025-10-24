from typing import Any, List
from error_handler import ErrorHandler, ParseError
from token_type import TokenType
from noggin_token import Token
from expr import *
from stmt import *

class Parser:
    def __init__(self, tokens:List[Token]):
        self.tokens = tokens
        self.current = 0
        self.line = 0
    
    def parse(self):
        statements = []
        while (not self.is_at_end()) or (self.peek().type != TokenType.EOF):
            try:
                statements.append(self.statement())
            except ParseError:
                self.synchronize()
        return statements
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        else:
            return self.expressionStatement()
    
    def printStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after print token")
        expressions = []
        expressions.append(self.expression())
        while (not self.match(TokenType.RIGHT_PAREN)):
            self.consume(TokenType.COMMA, "Expect ',' in between expressions")
            expressions.append(self.expression())
        self.consume(TokenType.SEMICOLON, "Expect ';' after print function.")
        return Print(expressions)
    
    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after statement.")
        return Expression(expr)
    
    def expression(self):
        return self.equality()
    
    def equality(self):
        left = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            left = Binary(left, operator, right)
        return left
    
    def comparison(self):
        left = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            left = Binary(left, operator, right)
        return left
    
    def term(self):
        left = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            left = Binary(left, operator, right)
        return left
    
    def factor(self):
        left = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            left = Binary(left, operator, right)
        return left
    
    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            right = Unary(operator, right)
            return right
        return self.primary()
    
    def primary(self):
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.NULL):
            return Literal(None)
        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expression)
        raise self.error(self.peek(), "Unexpected Token in expression")
    
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self, token, message):
        ErrorHandler().error(token, message)
        return ParseError()
    
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.match(TokenType.CLASS, TokenType.DEF, TokenType.VAR, TokenType.FOR,
                          TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
                return
            self.advance()
        return
    
    def match(self, *expected_types) -> bool:
        for type in expected_types:
            if (not self.is_at_end()) and self.tokens[self.current].type == type:
                self.advance()
                return True
        return False

    def check(self, expected_type) -> bool:
        if (not self.is_at_end()) and self.tokens[self.current].type == expected_type:
            return True
        return False
    
    def advance(self) -> Token:
        self.current += 1
        return self.tokens[self.current - 1]
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)-1
    
    def peek(self) -> Token:
        if self.is_at_end():
            return Token(TokenType.EOF, None, None, None)
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]