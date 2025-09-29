from typing import Any, List
from error_handler import ErrorHandler, ParseError
from token_type import TokenType
from noggin_token import Token
from expr import *

class Parser:
    def __init__(self, tokens:List[Token]):
        self.tokens = tokens
        self.current = 0
        self.line = 0
    
    def parse(self):
        # Start parsing the tokens
        try:
            return self.expression()
        except ParseError:
            return None
    
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
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
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
        if self.match(TokenType.NUMBER,TokenType.STRING):
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
        raise self.error(self.peek(), "Expect expression.")
    
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
            if self.match(TokenType.CLASS, TokenType.DEF, TokenType.VAR,TokenType.FOR,
                          TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN):
                return
            self.advance()
        return
    
    def match(self, *expected_types) -> bool:
        for type in expected_types:
            if self.is_at_end() or self.tokens[self.current] == type:
                self.current += 1
                return True
        return False

    def check(self, expected_type) -> bool:
        if self.is_at_end() or self.tokens[self.current] != expected_type:
            return False
        self.current += 1
        return True
    
    def advance(self) -> Token:
        self.current += 1
        return self.tokens[self.current - 1]
    
    def is_at_end(self) -> bool:
        return self.current >= len(self.tokens)
    
    def peek(self) -> Token | str:
        if self.is_at_end():
            return "\0"
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]