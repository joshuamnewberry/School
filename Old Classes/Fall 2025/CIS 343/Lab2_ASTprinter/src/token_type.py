from enum import Enum

TokenType = Enum(
    'TokenType',
    [
        'LEFT_PAREN', 'RIGHT_PAREN', 'LEFT_BRACE', 'RIGHT_BRACE',
        'COMMA', 'DOT', 'MINUS', 'PLUS', 'SEMICOLON', 'SLASH', 'STAR',
        'BANG', 'BANG_EQUAL',
        'EQUAL', 'EQUAL_EQUAL',
        'GREATER', 'GREATER_EQUAL',
        'LESS', 'LESS_EQUAL',
        'IDENTIFIER', 'STRING', 'NUMBER',
        'AND', 'CLASS', 'DEF', 'ELSE', 'FALSE', 'FOR', 'IF', 'NULL', 'OTHER', 'OR',
        'PRINT', 'RETURN', 'SUPER', 'THIS', 'TRUE', 'VAR', 'WHILE',
        'EOF'
    ]
)