from __future__ import absolute_import, print_function
import ply.lex as lex

class Tokeniser(object):
    """A C/C++ tokeniser using the same token list as GCC
    (https://github.com/gcc-mirror/gcc/blob/master/libcpp/include/cpplib.h)"""
    tokens = [ 'EQ', 'NOT', 'GREATER', 'LESS', 'PLUS', 'MINUS', 'MULT', 'DIV', 'MOD', 'AND', 'OR', 'XOR', 'RSHIFT', 'LSHIFT',
        'COMPL', 'AND_AND', 'OR_OR', 'QUERY', 'COLON', 'COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'EQ_EQ', 'NOT_EQ', 'GREATER_EQ', 'LESS_EQ',
        'PLUS_EQ', 'MINUS_EQ', 'MULT_EQ', 'DIV_EQ', 'MOD_EQ', 'AND_EQ', 'OR_EQ', 'XOR_EQ', 'RSHIFT_EQ', 'LSHIFT_EQ',
        'HASH', 'PASTE',
        'OPEN_SQUARE', 'CLOSE_SQUARE', 'OPEN_BRACE', 'CLOSE_BRACE', 'SEMICOLON', 'ELLIPSIS', 'PLUS_PLUS', 'MINUS_MINUS', 'DEREF', 'DOT', 'SCOPE', 'DEREF_STAR', 'DOT_STAR',
        'NAME', 'FNAME', 'INTEGER', 'FLOAT',
        'CHAR',
        'STRING'
    ]

    t_ignore = " \t\n\r\f\v"
    t_EQ = r'='
    t_NOT = r'!'
    t_GREATER = r'>'
    t_LESS = r'<'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_MULT = r'\*'
    t_DIV = r'/(?!/)'
    t_MOD = r'%'
    t_AND = r'&'
    t_OR = r'\|'
    t_XOR = r'\^'
    t_RSHIFT = r'>>'
    t_LSHIFT = r'<<'

    t_COMPL = r'~'
    t_AND_AND = r'&&'
    t_OR_OR = r'\|\|'
    t_QUERY = r'\?'
    t_COLON = r':'
    t_COMMA = r','
    t_OPEN_PAREN = r'\('
    t_CLOSE_PAREN = r'\)'
    t_EQ_EQ = r'=='
    t_NOT_EQ = r'!='
    t_GREATER_EQ = r'>='
    t_LESS_EQ = r'<='

    t_PLUS_EQ = r'\+='
    t_MINUS_EQ = r'-='
    t_MULT_EQ = r'\*='
    t_DIV_EQ = r'/='
    t_MOD_EQ = r'%='
    t_AND_EQ = r'&='
    t_OR_EQ = r'\|='
    t_XOR_EQ = r'\^='
    t_RSHIFT_EQ = r'>>='
    t_LSHIFT_EQ = r'<<='

    t_HASH = r'\#'
    t_PASTE = r'\#\#'

    t_OPEN_SQUARE = r'\['
    t_CLOSE_SQUARE = r'\]'
    t_OPEN_BRACE = r'{'
    t_CLOSE_BRACE = r'}'
    t_SEMICOLON = r';'
    t_ELLIPSIS = r'\.\.\.'
    t_PLUS_PLUS = r'\+\+'
    t_MINUS_MINUS = r'--'
    t_DEREF = r'->'
    t_DOT = r'\.'
    t_SCOPE = r'::'
    t_DEREF_STAR = r'->\*'
    t_DOT_STAR = r'\.\*'

    t_NAME = r'[A-Za-z_][A-Za-z0-9_]*'
    t_FNAME = r'[A-Za-z_][A-Za-z0-9_]*\('  # EXTENSION: function macros cannot have whitespace between the name and the bracket
    # Instead of NUMBER we have:
    t_INTEGER = r'[0-9][0-9XxA-Fa-f]*'
    t_FLOAT = r'[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?'

    t_CHAR = "'.'"
    # WCHAR
    # CHAR16
    # CHAR32
    # UTF8CHAR
    # OTHER

    t_STRING = r'"[^\\"]*(?:\\"[^\\"]*)*"'
    # WSTRING
    # STRING16
    # STRING32
    # UTF8STRING
    # HEADER_NAME  # e.g. <stdio.h>

    # CHAR_USERDEF
    # WCHAR_USERDEF
    # CHAR16_USERDEF
    # CHAR32_USERDEF
    # UTF8CHAR_USERDEF
    # STRING_USERDEF
    # WSTRING_USERDEF
    # STRING16_USERDEF
    # STRING32_USERDEF
    # UTF8STRING_USERDEF
    
    # COMMENT
    
    #t_MACRO_ARG
    #t_PRAGMA
    # PRAGMA_EOL
    # PADDING

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module = self, **kwargs)

    def test(self, data):
            self.lexer.input(data)
            while True:
                 tok = self.lexer.token()
                 if not tok: 
                     break
                 print(tok)

tokens = Tokeniser.tokens
def __make_lexer():
    global lexer
    t = Tokeniser()
    lexer = lambda : t
# Default Tokeniser instance, constructed on first retrieval
lexer = __make_lexer

if __name__ == "__main__":
    lexer = Tokeniser()
    lexer.test('f(y+1) + f(f(z)) % t(t(g)(0) + t)(1);')
    print()
    lexer.test('p() i[q()] = { q(1), r(2,3), r(4,), r(,5), r(,) };')
    print()
    lexer.test('"niall" is here')
    print()
    lexer.test('"n\\"iall" is here')
