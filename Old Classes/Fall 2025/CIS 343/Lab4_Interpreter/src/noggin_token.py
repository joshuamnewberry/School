from token_type import TokenType

class Token:
    def __init__(self, type:TokenType, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def to_string(self):
        return f"{self.type} | {self.lexeme} | {self.literal}"

    def __str__(self):
        return self.to_string()