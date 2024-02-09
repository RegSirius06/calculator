# lextab.py. This file automatically created by PLY (version 3.11). Don't edit!
_tabversion   = '3.10'
_lextokens    = set(('COLON', 'DIVIDE', 'LPAREN', 'MINUS', 'NAME', 'NUMBER', 'PLUS', 'RPAREN', 'TIMES'))
_lexreflags   = 64
_lexliterals  = ''
_lexstateinfo = {'INITIAL': 'inclusive'}
_lexstatere   = {'INITIAL': [('(?P<t_NUMBER>\\d+(\\.\\d+)?)|(?P<t_newline>\\n+)|(?P<t_NAME>[a-zA-Z_][a-zA-Z0-9_]*)|(?P<t_LPAREN>\\()|(?P<t_PLUS>\\+)|(?P<t_RPAREN>\\))|(?P<t_TIMES>\\*)|(?P<t_COLON>,)|(?P<t_DIVIDE>/)|(?P<t_MINUS>-)', [None, ('t_NUMBER', 'NUMBER'), None, ('t_newline', 'newline'), (None, 'NAME'), (None, 'LPAREN'), (None, 'PLUS'), (None, 'RPAREN'), (None, 'TIMES'), (None, 'COLON'), (None, 'DIVIDE'), (None, 'MINUS')])]}
_lexstateignore = {'INITIAL': ' \t'}
_lexstateerrorf = {'INITIAL': 't_error'}
_lexstateeoff = {}
