import sys

class ErrorHandler:
    had_error = False
    
    @staticmethod
    def error(line, message):
        ErrorHandler.report(line,"", message)
    
    @staticmethod
    def report(line, where, message):
        print(f"[line {line}] Error{where}: {message}")
        ErrorHandler.had_error = True