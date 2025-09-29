import sys
from noggin_token import Token
from token_type import TokenType

class ErrorHandler:
    had_error = False
    
    @staticmethod
    def error(err, message):
        if isinstance(err, Token):
            if (err.type == TokenType.EOF):
                ErrorHandler.report(err.line, " at end", message)
            else:
                ErrorHandler.report(err.line, f" at '{err.lexeme}'", message)
        else:
            ErrorHandler.report(err, "", message)   
    
    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        ErrorHandler.had_error = True

class ParseError(RuntimeError):
    pass