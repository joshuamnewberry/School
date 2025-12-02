from typing import Any, List
from error_handler import ErrorHandler, NogginParseError
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
            except NogginParseError:
                self.synchronize()
        if len(self.statements) == 1 and isinstance(self.statements[0], Expression):
            return self.statements[0]
        return self.statements
    
    def statement(self) -> Print|Def|Class|Function|Assignment|Block|If|While|Return|Set|Expression:
        if self.match(TokenType.PRINT): ## Print
            return self.printStatement()
        elif self.match(TokenType.DEF): ## Declare and Function
            return self.declaration()
        elif self.match(TokenType.CLASS):
            return self.klass()
        elif self.is_start_of_assignment(): ## Assign
            return self.assignmentStatement()
        elif self.match(TokenType.LEFT_BRACE): ## Block
            return self.block()
        elif self.match(TokenType.IF): ## If
            return self.ifStatement()
        elif self.match(TokenType.WHILE): ## While
            return self.whileStatement()
        elif self.match(TokenType.FOR): ## For
            return self.forStatement()
        elif self.match(TokenType.RETURN):
            return self.returnStatement()
        else: ## Expression of some other kind
            return self.expressionStatement()
    
    def is_start_of_assignment(self) -> bool:
        index = self.current
        if self.tokens[index].type not in (TokenType.IDENTIFIER, TokenType.THIS):
            return False
        index += 1
        while index < len(self.tokens) and self.tokens[index].type == TokenType.DOT:
            index += 1
            if index >= len(self.tokens) or self.tokens[index].type != TokenType.IDENTIFIER:
                return False
            index += 1
        if index < len(self.tokens) and self.tokens[index].type == TokenType.EQUAL:
            return True
        return False
    
    def klass(self):
        self.consume(TokenType.IDENTIFIER, "Expect name after class token")
        name = self.previous()
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before contents of class")
        methods = []
        while not self.match(TokenType.RIGHT_BRACE):
            self.consume(TokenType.IDENTIFIER, "Expect function name for class function definitions")
            if not self.check(TokenType.LEFT_PAREN):
                raise self.error(self.peek(), "Expect '(' before parameters of function")
            methods.append(self.function())
        return Class(name, methods)
    
    def declaration(self):
        self.consume(TokenType.IDENTIFIER, "Expect variable or function name after def token")
        if self.peek().type == TokenType.LEFT_PAREN:
            return self.function()
        return self.varDeclaration()
    
    def function(self): 
        name = self.previous()
        self.advance()
        parameters = self.parameters()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters of function")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before contents of function")
        block = self.block()
        return Function(name, parameters, block)

    def parameters(self):
        parameters = []
        if self.match(TokenType.IDENTIFIER):
            parameters.append(self.previous())
            while self.match(TokenType.COMMA):
                self.advance()
                parameters.append(self.previous())
        return parameters
    
    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if token")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before if statement contents")
        block = self.block()
        if self.match(TokenType.ELSE):
            if self.match(TokenType.IF):
                return If(condition, block, self.ifStatement())
            self.consume(TokenType.LEFT_BRACE, "Expect '{' before else statement contents")
            else_block = self.block()
            return If(condition, block, Else(else_block))
        return If(condition, block)
    
    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after while token")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while expression")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before while statement contents")
        block = self.block()
        return While(condition, block)
    
    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after for token")
        definition = None
        if self.match(TokenType.DEF):
            definition = self.varDeclaration()
        condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition")
        modifier = self.statement()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for expression")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before for statement contents")
        block = self.block()
        block.statements.append(modifier)
        if definition:
            return Block([definition, # Define
                          While(condition, block)])
        return Block([While(condition, block)])
    
    def block(self) -> Block:
        statements = []
        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.is_at_end()):
            try:
                statements.append(self.statement())
            except NogginParseError:
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
        target = self.primary()
        while self.match(TokenType.DOT):
            self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
            name = self.previous()
            target = Get(target, name)
        self.consume(TokenType.EQUAL, "Expect '=' in assignment.")
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after assignment.")
        if isinstance(target, Variable):
            return Assignment(target.name, value)
        if isinstance(target, Get):
            return Set(target.object, target.name, value)
        raise self.error(self.previous(), "Invalid assignment target.")
    
    def varDeclaration(self):
        name = self.previous()
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return Def(name, initializer)
    
    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return.")
        return Return(keyword, value)

    def expression(self):
        return self.logical_or()
    
    def logical_or(self):
        left = self.logical_and()
        while(self.match(TokenType.OR)):
            operator = self.previous()
            right = self.logical_or()
            left = Binary(left, operator, right)
        return left
    
    def logical_and(self):
        left = self.equality()
        while(self.match(TokenType.AND)):
            operator = self.previous()
            right = self.equality()
            left = Binary(left, operator, right)
        return left
    
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
        return self.call()
    
    def call(self):
        left = self.primary()
        while self.match(TokenType.LEFT_PAREN, TokenType.DOT):
            if self.previous().type == TokenType.DOT:
                self.consume(TokenType.IDENTIFIER, "Expect Identifier after dot.")
                left = Get(left, self.previous())
            else:
                arguments = self.arguments()
                self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
                left = Call(left, arguments, self.previous())
        return left

    def arguments(self):
        if self.check(TokenType.RIGHT_PAREN):
            return []
        expressions = []
        expressions.append(self.expression())
        while(self.match(TokenType.COMMA)):
            expressions.append(self.expression())
        return expressions
    
    def primary(self):
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.NULL):
            return Literal(None)
        if self.match(TokenType.THIS):
            return This(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expression)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        raise self.error(self.peek(), "Unexpected Token in expression.")
    
    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self, token, message):
        ErrorHandler().error(token, message)
        return NogginParseError()
    
    def synchronize(self):
        if not self.is_at_end():
            self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.match(TokenType.CLASS, TokenType.DEF, TokenType.FOR,
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