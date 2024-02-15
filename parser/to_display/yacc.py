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
        if t[2] == '+'  : t[0] = f"{digit(t[1])} увеличить на {digit(t[3])}"
        elif t[2] == '-': t[0] = f"{digit(t[1])} уменьшить на {digit(t[3])}"
        elif t[2] == '*': t[0] = f"{digit(t[1])} умножить на {digit(t[3])}"
        elif t[2] == '/': t[0] = f"{digit(t[1])} разделить на {digit(t[3])}"

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
                t[0] = f"Синус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'cos':
            if len(t[3]) == 1:
                t[0] = f"Косинус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'tg':
            if len(t[3]) == 1:
                t[0] = f"Тангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'ctg':
            if len(t[3]) == 1:
                t[0] = f"Котангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asin':
            if len(t[3]) == 1:
                t[0] = f"Арксинус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acos':
            if len(t[3]) == 1:
                t[0] = f"Арккосинус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'atg':
            if len(t[3]) == 1:
                t[0] = f"Арктангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'actg':
            if len(t[3]) == 1:
                t[0] = f"Арккотангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'sinh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический синус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'cosh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический косинус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'tgh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический тангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'ctgh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический котангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asinh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический арксинус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acosh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический арккосинус числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'atgh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический арктангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'actgh':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический арккотангенс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'sec':
            if len(t[3]) == 1:
                t[0] = f"Секанс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'csc':
            if len(t[3]) == 1:
                t[0] = f"Косеканс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asec':
            if len(t[3]) == 1:
                t[0] = f"Арксеканс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acsc':
            if len(t[3]) == 1:
                t[0] = f"Арккосеканс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'sech':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический секанс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'csch':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический косеканс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'asech':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический арксеканс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'acsch':
            if len(t[3]) == 1:
                t[0] = f"Гиперболический арккосеканс числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'pow':
            if len(t[3]) == 2:
                t[0] = f"Число {digit(t[3][0])} возвести в степень {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'pow2':
            if len(t[3]) == 1:
                t[0] = f"Число {digit(t[3][0])} возвести в квадрат"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'sqrt':
            if len(t[3]) == 1:
                t[0] = f"Извлечь из числа {digit(t[3][0])} квадратный корень"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'exp':
            if len(t[3]) == 1:
                t[0] = f"Число \'e\' возвести в степень {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'ln':
            if len(t[3]) == 1:
                t[0] = f"Натуральный логарифм числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'lg':
            if len(t[3]) == 1:
                t[0] = f"Логарифм числа {digit(t[3][0])} по основанию 10"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'log2':
            if len(t[3]) == 1:
                t[0] = f"Логарифм числа {digit(t[3][0])} по основанию 2"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'log':
            if len(t[3]) == 2:
                t[0] = f"Логарифм числа {digit(t[3][1])} по основанию {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')




        elif t[1] == 'factorial':
            if len(t[3]) == 1:
                t[0] = f"Факториал числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'radians':
            if len(t[3]) == 1:
                t[0] = f"Перевести число {digit(t[3][0])} в радианы"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'degrees':
            if len(t[3]) == 1:
                t[0] = f"Перевести число {digit(t[3][0])} в градусы"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'ceil':
            if len(t[3]) == 1:
                t[0] = f"Округлить число {digit(t[3][0])} вверх"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'floor':
            if len(t[3]) == 1:
                t[0] = f"Округлить число {digit(t[3][0])} вниз"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'round':
            if len(t[3]) == 2:
                t[0] = f"Округлить число {digit(t[3][0])} до знака после запятой номер {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')




        elif t[1] == 'abs':
            if len(t[3]) == 1:
                t[0] = f"Модуль числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'swapsign':
            if len(t[3]) == 1:
                t[0] = f"Смена знака числа {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')




        elif t[1] == 'inv':
            if len(t[3]) == 1:
                t[0] = f"Инверсия {digit(t[3][0])}"
                return
            raise SyntaxError(f'{t[1]}() function need one arguments')
        elif t[1] == 'and':
            if len(t[3]) == 2:
                t[0] = f"Побитовое И: {digit(t[3][0])} & {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'or':
            if len(t[3]) == 2:
                t[0] = f"Побитовое ИЛИ: {digit(t[3][0])} | {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'xor':
            if len(t[3]) == 2:
                t[0] = f"Побитовое ИСКЛЮЧАЮЩЕ ИЛИ: {digit(t[3][0])} ^ {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'imp':
            if len(t[3]) == 2:
                t[0] = f"Побитовая ИМПЛИКАЦИЯ: {digit(t[3][0])} -> {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'left':
            if len(t[3]) == 2:
                t[0] = f"Побитовый сдвиг {digit(t[3][0])} влево на {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'right':
            if len(t[3]) == 2:
                t[0] = f"Побитовый сдвиг {digit(t[3][0])} вправо на {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')




        elif t[1] == 'div':
            if len(t[3]) == 2:
                t[0] = f"{digit(t[3][0])} делить нацело на {digit(t[3][1])}"
                return
            raise SyntaxError(f'{t[1]}() function need two arguments')
        elif t[1] == 'mod':
            if len(t[3]) == 2:
                t[0] = f"Остаток от деления {digit(t[3][0])} на {digit(t[3][1])}"
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
