from expr import Binary, Unary, Literal, Grouping
from ast_printer import AstPrinter
from noggin_token import Token
from token_type import TokenType

# Example AST: (* (- 123) (group 45.67))
expression = Binary(
    Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
    Token(TokenType.STAR, "*", None, 1),
    Grouping(Literal(45.67))
)

printer = AstPrinter()
print(printer.print(expression))