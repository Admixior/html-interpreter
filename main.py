import ply.lex as lex
import AST
import re

tokens = ( 'HTMLstart', 'HTMLend', 'BODYstart', 'BODYend', 'HEADstart', 'HEADend', 'TITLEstart', 'TITLEend', 'TITLEtext','H1', 'CENTER', 'BUTTON', 'TEXT', 'COMMENT' )

states = (
    ('htmlstate','inclusive'),
    ('titlestate','exclusive'),
    ('headstate','inclusive'),
    ('bodystate','inclusive'),
    ('commentstate','exclusive')
)



def t_HTMLstart(t):
    r'<html(\s[a-zA-Z]*="[a-zA-Z]*")*>'
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
    r'[^<\n\s]+[^<\n]*'
    AST.open_tag('text')
    AST.new_attr_tag('innertext',t.value)
    AST.new_attr_tag('align', AST.temp_style['align'])
    AST.new_attr_tag('size', AST.temp_style['size'])
    AST.move_up_to_close_tag("text")
    return t

def t_bodystate_BUTTON(t):
    r'<button>[^<]+<\/button>'
    AST.open_tag('button')
    AST.new_attr_tag('innertext',t.value[8:-9])
    AST.new_attr_tag('align', AST.temp_style['align'])
    AST.new_attr_tag('size', AST.temp_style['size'])
    AST.move_up_to_close_tag("button")
    return t

def t_bodystate_H1(t):
    r'<\/?h1>'
    if t.value[1]=='/':
        AST.temp_style['size']='normal'
    else:
        AST.temp_style['size']='h1'

def t_bodystate_CENTER(t):
    r'<\/?center>'
    if t.value[1]=='/':
        AST.temp_style['align']='left'
    else:
        AST.temp_style['align']='center'

def t_titlestate_TITLEtext(t):
    r'[^<\n]+'
    AST.AST_tree['attr']['windowtitle'] = t.value
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
    r'\n[\s\t]*'
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



AST.renderowanie()
