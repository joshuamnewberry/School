from error_handler import ErrorHandler
from token_type import TokenType
from noggin_token import Token

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "def": TokenType.DEF,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "null": TokenType.NULL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "while": TokenType.WHILE
        }
        self.current = 0
        self.line = 0
    
    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def scan_token(self):
        char = self.advance()
        if char == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self.add_token(TokenType.COMMA)
        elif char == "-":
            self.add_token(TokenType.MINUS)
        elif char == "+":
            self.add_token(TokenType.PLUS)
        elif char == ";":
            self.add_token(TokenType.SEMICOLON)
        elif char == "*":
            self.add_token(TokenType.STAR)
        elif char == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif char == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif char == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif char == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)
        elif char == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            elif self.match("*"):
                while not (self.peek() == "*" and self.peek_next() == "/"):
                    if char == "\n":
                        self.line += 1
                    self.advance()
                self.advance()
                self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif char == " " or char == "\r" or char == "\t" or char == "\b" or char == "\f":
            pass
        elif char == "\n":
            self.line += 1
        elif char.isdigit():
            self.number()
        elif char == ".":
            if self.peek().isdigit():
                self.advance()
                while self.peek().isdigit():
                    self.advance()
                self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
            else:
                self.add_token(TokenType.DOT)
        elif char == '"':
            self.string()
        elif char == "'":
            self.string()
        elif char.isalpha() or char == "_":
            self.identifier()
        else:
            print(char)
            ErrorHandler.error(self.line, f"Unexpected character: {char}")
    
    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    
    def match(self, expected):
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]
    
    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]
    
    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)
    
    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
    
    def string(self):
        while (self.peek() != '"' and self.peek() != "'") and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        if self.is_at_end():
            ErrorHandler.error(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_at_end(self):
        return self.current >= len(self.source)