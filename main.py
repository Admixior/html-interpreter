import ply.lex as lex
import re

tokens = ( 'HTMLstart', 'HTMLend', 'BODYstart', 'BODYend', 'HEADstart', 'HEADend', 'TITLEstart', 'TITLEend', 'TITLEtext','H1', 'TEXT', 'COMMENT' )

states = (
    ('htmlstate','inclusive'),
    ('titlestate','exclusive'),
    ('headstate','inclusive'),
    ('bodystate','inclusive'),
    ('commentstate','exclusive')
)

t_ANY_H1 = r'<\/?h1>'
t_ANY_ignore = r'\s*'

def t_HTMLstart(t):
    r'<html\s[a-zA-Z]*="[a-zA-Z]*">'
    t.lexer.begin('htmlstate')
    return t

def t_htmlstate_HTMLend(t):
    r'<\/html>'
    t.lexer.begin('INITIAL')
    return t
    
def t_htmlstate_HEADstart(t):
    r'<head>'
    t.lexer.begin('headstate')
    return t

def t_headstate_HTMLend(t):
    r'<\/head>'
    t.lexer.begin('htmlstate')
    return t

def t_htmlstate_BODYstart(t):
    r'<body>'
    t.lexer.begin('bodystate')
    return t

    
def t_htmlstate_BODYendt(t):
    r'<body>'
    t.lexer.begin('bodystate')
    return t

def t_bodystate_HTMLend(t):
    r'<\/body>'
    t.lexer.begin('htmlstate')
    return t

def t_bodystate_TEXT(t):
    r'[^<\n]+'
    return t

def t_titlestate_TITLEtext(t):
    r'[^<\n]+'
    return t

def t_headstate_TITLEstart(t):
    r'<title>'
    t.lexer.begin('titlestate')
    return t

def t_titlestate_TITLEend(t):
    r'<\/title>'
    t.lexer.begin('headstate')
    return t

def t_ANY_COMMENT(t):
    r'<!--.*-->'
    return t

def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ANY_error(t) :
    print("Illegal character '%s'" %t.value[0])
    t.lexer.skip(1)
    return t

lexer = lex.lex()
fh = open("example.html", "r");
lexer.input( fh.read() )
for token in lexer:
    print("line %d: %s(%s)" %(token.lineno, token.type, token.value))