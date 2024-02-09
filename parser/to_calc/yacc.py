from ply import yacc

from new_classes.digit import digit

class Yacc:
    precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    def p_expression_binop(self, t):
        '''expression : expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression'''
        if t[2] == '+'  : t[0] = t[1] + t[3]
        elif t[2] == '-': t[0] = t[1] - t[3]
        elif t[2] == '*': t[0] = t[1] * t[3]
        elif t[2] == '/': t[0] = t[1] / t[3]

    def p_expression_uminus(self, t):
        'expression : MINUS expression %prec UMINUS'
        t[0] = -t[2]

    def p_expression_group(self, t):
        'expression : LPAREN expression RPAREN'
        t[0] = t[2]

    def p_expressions(self, t):
        '''
        expressions : expressions COLON expression
                | expression
                |
        '''
        if len(t) == 0:
            t[0]=None
            return
        t[0] = [t[1]] if len(t) == 2 else t[1] + [t[3]]

    def p_expression_function(self, t):
        '''
        expression : NAME LPAREN expressions RPAREN
        '''
        if t[1] == 'sin':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).sin()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'cos':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).cos()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'tg':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).tg()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'ctg':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).ctg()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asin':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).asin()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acos':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).acos()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'atg':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).atg()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'actg':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).actg()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'sinh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).sinh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'cosh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).cosh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'tgh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).tgh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'ctgh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).ctgh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asinh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).asinh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acosh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).acosh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'atgh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).atgh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'actgh':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).actgh()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'sec':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).sec()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'csc':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).csc()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asec':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).asec()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acsc':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).acsc()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'sech':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).sech()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'csch':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).csch()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asech':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).asech()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acsch':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).acsch()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'pow':
            if len(t[3]) == 2:
                t[0] = pow(digit(t[3][0]), digit(t[3][1]))
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'pow2':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]) ** 2
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'sqrt':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).sqrt()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'exp':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).exp()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'ln':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).ln()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'lg':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).lg()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'log2':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).log2()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'log':
            if len(t[3]) == 2:
                t[0] = digit(t[3][1]).log(digit(t[3][0]))
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')




        elif t[1] == 'factorial':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).factorial()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'radians':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).radians()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'degrees':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).degrees()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'ceil':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).ceil()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'floor':
            if len(t[3]) == 1:
                t[0] = digit(t[3][0]).floor()
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'round':
            if len(t[3]) == 2:
                t[0] = round(digit(t[3][0]), digit(t[3][1]))
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')




        elif t[1] == 'abs':
            if len(t[3]) == 1:
                t[0] = abs(digit(t[3][0]))
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'swapsign':
            if len(t[3]) == 1:
                t[0] = -digit(t[3][0])
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == '~':
            if len(t[3]) == 1:
                t[0] = ~digit(t[3][0])
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == '&':
            if len(t[3]) == 2:
                t[0] = digit(t[3][0]) & digit(t[3][1])
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == '|':
            if len(t[3]) == 2:
                t[0] = digit(t[3][0]) | digit(t[3][1])
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == '^':
            if len(t[3]) == 2:
                t[0] = digit(t[3][0]) ^ digit(t[3][1])
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'imp':
            if len(t[3]) == 2:
                t[0] = digit(t[3][0]).implication(digit(t[3][1]))
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'left':
            if len(t[3]) == 2:
                t[0] = (digit(t[3][0]) << digit(t[3][1]))
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'right':
            if len(t[3]) == 2:
                t[0] = (digit(t[3][0]) >> digit(t[3][1]))
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')




        elif t[1] == 'div':
            if len(t[3]) == 2:
                t[0] = digit(t[3][0]) // digit(t[3][1])
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'mod':
            if len(t[3]) == 2:
                t[0] = digit(t[3][0]) % digit(t[3][1])
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        t[0] = None
        raise SyntaxWarning(f'Undefined function \'{t[1]}\'')

    def p_expression_number(self, t):
        'expression : NUMBER'
        t[0] = t[1]

    def p_expression_name(self, t):
        'expression : NAME'
        try:
            t[0] = self.reserved[t[1]]
        except LookupError:
            t[0] = 0
            raise SyntaxWarning(f"Undefined name '{t[1]}'")

    def p_error(self, t):
        raise SyntaxError(f"Syntax error at '{t.value}'")

    def build(self, lexer, **kwargs):
        self.tokens = lexer.tokens
        self.reserved = lexer.reserved
        self.parser = yacc.yacc(module=self, **kwargs)
        self.lexer = lexer

    def get_result(self, s: str):
        return self.parser.parse(s, lexer=self.lexer)
