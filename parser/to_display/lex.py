from ply import lex

from new_classes.digit import digit

class Lex:
    tokens = (
        'NUMBER',
        'NAME',
        'COLON',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN'
    )

    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_COLON   = r','
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_ignore = ' \t'

    reserved = {
        'PI': f"{digit('PI')}",
        'TAU': f"{digit('TAU')}",
        'E': f"{digit('E')}"
    }

    def t_NUMBER(self, t):
        r'\d+(\.\d+)?'
        t.value = digit(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, input) -> None:
        self.lexer.input(input)

    def token(self):
        return self.lexer.token()
