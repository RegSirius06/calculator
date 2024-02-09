from parser.to_calc import lex, yacc
from parser.to_display import lex as lex_d, yacc as yacc_d
from new_classes.digit import digit

def parser(formula: str) -> digit:
    m = lex.Lex()
    m.build(optimize=1)
    n = yacc.Yacc()
    n.build(m, debug=0, write_tables=0)
    return digit(n.get_result(formula))

def parser_to_disp(formula: str) -> digit:
    m = lex_d.Lex()
    m.build(optimize=1)
    n = yacc_d.Yacc()
    n.build(m, debug=0, write_tables=0)
    return n.get_result(formula)
