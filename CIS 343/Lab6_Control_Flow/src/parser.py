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
        self.statements = []
    
    def parse(self) -> Expression|List[Stmt]:
        self.statements = []
        while (not self.is_at_end()):
            try:
                self.statements.append(self.statement())
            except ParseError:
                self.synchronize()
        if len(self.statements) == 1 and isinstance(self.statements[0], Expression):
            return self.statements[0]
        return self.statements
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        elif self.match(TokenType.DEF):
            return self.varDeclaration()
        elif self.check(TokenType.IDENTIFIER) and self.peek_next().type == TokenType.EQUAL:
            self.advance()
            return self.assignmentStatement()
        elif self.match(TokenType.LEFT_BRACE):
            return self.block()
        else:
            return self.expressionStatement()
    
    def block(self):
        statements = []
        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.is_at_end()):
            try:
                statements.append(self.statement())
            except ParseError:
                self.synchronize()
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' at the end of block")
        return Block(statements)
    
    def printStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after print token")
        expressions = []
        expressions.append(self.expression())
        while (not self.match(TokenType.RIGHT_PAREN)):
            if self.check(TokenType.SEMICOLON):
                raise self.error(self.peek(), "Expect ')' before ';'")
            self.consume(TokenType.COMMA, "Expect ',' in between expressions")
            expressions.append(self.expression())
        self.consume(TokenType.SEMICOLON, "Expect ';' after print function.")
        return Print(expressions)
    
    def expressionStatement(self):
        expr = self.expression()
        if self.is_at_end() and len(self.statements) == 0:
            return Expression(expr)
        if self.check(TokenType.EQUAL):
            raise self.error(self.peek(), "Invalid assignment target")
        self.consume(TokenType.SEMICOLON, "Expect ';' after statement.")
        return Expression(expr)
    
    def assignmentStatement(self):
        name = self.previous()
        self.advance()
        initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable assignment")
        return Assignment(name, initializer)
    
    def varDeclaration(self):
        self.consume(TokenType.IDENTIFIER, "Expect variable name after def token")
        name = self.previous()
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return Def(name, initializer)

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
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        raise self.error(self.peek(), "Unexpected Token in expression")
    
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self, token, message):
        ErrorHandler().error(token, message)
        return ParseError()
    
    def synchronize(self):
        if not self.is_at_end():
            self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.match(TokenType.CLASS, TokenType.DEF, TokenType.VAR, TokenType.FOR,
                          TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN, TokenType.EOF):
                return
            self.advance()
        return
    
    def match(self, *expected_types) -> bool:
        for type in expected_types:
            if self.peek().type == type:
                self.advance()
                return True
        return False

    def check(self, expected_type) -> bool:
        if self.peek().type == expected_type:
            return True
        return False
    
    def advance(self) -> Token:
        self.current += 1
        return self.tokens[self.current-1]
    
    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self) -> Token:
        if self.current >= len(self.tokens):
            return Token(TokenType.EOF, "", None, self.line)
        return self.tokens[self.current]
    
    def peek_next(self) -> Token:
        if self.current >= len(self.tokens):
            return Token(TokenType.EOF, "", None, self.line)
        return self.tokens[self.current+1]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]