#!/usr/bin/python
# Python C99 conforming preprocessor expression evaluator
# (C) 2019 Niall Douglas http://www.nedproductions.biz/
# Started: Apr 2019

from __future__ import generators, print_function, absolute_import

import os, sys, copy
if __name__ == '__main__' and __package__ is None:
    sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from pcpp.preprocessor import Preprocessor, yacc, STRING_TYPES

# The width of signed integer which this evaluator will use
INTMAXBITS = 64

# Some Python 3 compatibility shims
if sys.version_info.major < 3:
    INTBASETYPE = long
else:
    INTBASETYPE = int

class Value(INTBASETYPE):
    """A signed or unsigned integer within a preprocessor expression, bounded
    to within INT_MIN and INT_MAX, or 0 and UINT_MAX. Signed overflow is handled
    like a two's complement CPU, despite being UB, as that's what GCC and clang do.
    
    >>> Value(5)
    Value(5)
    >>> Value('5L')
    Value(5)
    >>> Value('5U')
    Value(5U)
    >>> Value('0')
    Value(0)
    >>> Value('0U')
    Value(0U)
    >>> Value('-1U')
    Value(18446744073709551615U)
    >>> Value(5) * Value(2)
    Value(10)
    >>> Value(5) + Value('2u')
    Value(7U)
    >>> Value(5) * 2
    Value(10)
    >>> Value(50) % 8
    Value(2)
    >>> -Value(5)
    Value(-5)
    >>> +Value(-5)
    Value(-5)
    >>> ~Value(5)
    Value(-6)
    >>> Value(6) & 2
    Value(2)
    >>> Value(4) | 2
    Value(6)
    >>> Value(6) ^ 2
    Value(4)
    >>> Value(2) << 2
    Value(8)
    >>> Value(8) >> 2
    Value(2)
    >>> Value(9223372036854775808)
    Value(-9223372036854775808)
    >>> Value(-9223372036854775809)
    Value(9223372036854775807)
    >>> Value(18446744073709551615)
    Value(-1)
    >>> Value(False)
    Value(0)
    >>> Value(True)
    Value(1)
    >>> Value(5) == Value(6)
    Value(0)
    >>> Value(5) == Value(5)
    Value(1)
    >>> not Value(2)
    Traceback (most recent call last):
    ...
    AssertionError
    >>> Value(4) and Value(2)
    Traceback (most recent call last):
    ...
    AssertionError
    >>> Value(5) and not Value(6)
    Traceback (most recent call last):
    ...
    AssertionError
    """
    INT_MIN = -(1 << (INTMAXBITS - 1))
    INT_MAX = (1 << (INTMAXBITS - 1)) - 1
    INT_MASK = (1 << INTMAXBITS) - 1
    UINT_MIN = 0
    UINT_MAX = (1 << INTMAXBITS) - 1
    @classmethod
    def __sclamp(cls, value):
        value = INTBASETYPE(value)
        return ((value - cls.INT_MIN) & cls.INT_MASK) + cls.INT_MIN
    @classmethod
    def __uclamp(cls, value):
        value = INTBASETYPE(value)
        return value & cls.UINT_MAX
    def __new__(cls, value, unsigned = False):
        if isinstance(value, Value):
            unsigned = value.unsigned
        elif isinstance(value, INTBASETYPE) or isinstance(value, int):
            value = cls.__sclamp(value)
        elif isinstance(value, STRING_TYPES):
            # Strip any terminators
            while not (value[-1] >= '0' and value[-1] <= '9'):
                if value[-1] == 'u' or value[-1] == 'U':
                    unsigned = True
                value = value[:-1]
            x = INTBASETYPE(value)
            value = cls.__uclamp(x) if unsigned else cls.__sclamp(x)
            #assert x == value
        else:
            assert False  # Input is an unrecognised type
        inst = super(Value, cls).__new__(cls, value)
        inst.unsigned = unsigned
        return inst
    def __add__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) + self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__add__(other))
    def __sub__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) - self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__sub__(other))
    def __mul__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) * self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__mul__(other))
    def __div__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) / self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__div__(other))
    def __mod__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) % self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__mod__(other))
    def __neg__(self):
        return Value(super(Value, self).__neg__(), self.unsigned)
    def __invert__(self):
        return Value(super(Value, self).__invert__(), self.unsigned)
    def __and__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) & self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__and__(other))
    def __or__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) | self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__or__(other))
    def __pos__(self):
        return Value(super(Value, self).__pos__())
    def __pow__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) ** self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__pow__(other))
    def __lshift__(self, other):
        # Ignore other signedness
        other = Value(other)
        return Value(self.__uclamp(self) << self.__uclamp(other), True) if (self.unsigned) else Value(super(Value, self).__lshift__(other))
    def __rshift__(self, other):
        # Ignore other signedness
        other = Value(other)
        return Value(self.__uclamp(self) >> self.__uclamp(other), True) if (self.unsigned) else Value(super(Value, self).__rshift__(other))
    def __xor__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) ^ self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(super(Value, self).__xor__(other))
    def __repr__(self):
        if self.unsigned:
            return "Value(%dU)" % INTBASETYPE(self)
        else:
            return "Value(%d)" % INTBASETYPE(self)
    def __bool__(self):
        assert False  # Do not use Python logical operations
    def __nonzero__(self):
        assert False  # Do not use Python logical operations
    def __cmp__(self, other):
        assert False
    def __lt__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) < self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(self.__sclamp(self) < self.__sclamp(other), False)
    def __le__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) <= self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(self.__sclamp(self) <= self.__sclamp(other), False)
    def __eq__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) == self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(self.__sclamp(self) == self.__sclamp(other), False)
    def __ne__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) != self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(self.__sclamp(self) != self.__sclamp(other), False)
    def __ge__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) >= self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(self.__sclamp(self) >= self.__sclamp(other), False)
    def __gt__(self, other):
        other = Value(other)
        return Value(self.__uclamp(self) > self.__uclamp(other), True) if (self.unsigned or other.unsigned) else Value(self.__sclamp(self) > self.__sclamp(other), False)

        
# PLY yacc specification
# Valid C preprocessor expression items:
#   - Integer constants
#   - Character constants
#   - Addition, subtraction, multiplication, division, bitwise and-or-xor, shifts,
#     comparisons, logical and-or-not
#   - defined()
#
# The C preprocessor does not support:
#   - assignment
#   - increment and decrement
#   - array indexing, indirection
#   - casting
#   - sizeof, alignof

# The subset of tokens from Preprocessor used in preprocessor expressions
tokens = (
   'CPP_ID','CPP_INTEGER', 'CPP_CHAR', 'CPP_WS', 
   'CPP_PLUS', 'CPP_MINUS', 'CPP_STAR', 'CPP_FSLASH', 'CPP_PERCENT', 'CPP_BAR',
   'CPP_AMPERSAND', 'CPP_TILDE', 'CPP_HAT', 'CPP_LESS', 'CPP_GREATER', 'CPP_EQUAL', 'CPP_EXCLAMATION',
   'CPP_QUESTION', 'CPP_LPAREN', 'CPP_RPAREN',
   'CPP_COMMA', 'CPP_COLON', 'CPP_BSLASH', 'CPP_SQUOTE', 

   'CPP_LSHIFT', 'CPP_LESSEQUAL', 'CPP_RSHIFT',
   'CPP_GREATEREQUAL', 'CPP_LOGICALOR', 'CPP_LOGICALAND', 'CPP_EQUALITY',
   'CPP_INEQUALITY'
)

precedence = (
    ('left', 'CPP_COMMA'),                                                     # 15
                                                                               # 14 (assignments, unused)
    ('left', 'CPP_QUESTION', 'CPP_COLON'),                                     # 13
    ('left', 'CPP_LOGICALOR'),                                                 # 12
    ('left', 'CPP_LOGICALAND'),                                                # 11
    ('left', 'CPP_BAR'),                                                       # 10
    ('left', 'CPP_HAT'),                                                       # 9
    ('left', 'CPP_AMPERSAND'),                                                 # 8
    ('left', 'CPP_EQUALITY', 'CPP_INEQUALITY'),                                # 7
    ('left', 'CPP_LESS', 'CPP_LESSEQUAL', 'CPP_GREATER', 'CPP_GREATEREQUAL'),  # 6
    ('left', 'CPP_LSHIFT', 'CPP_RSHIFT'),                                      # 5
    ('left', 'CPP_PLUS', 'CPP_MINUS'),                                         # 4
    ('left', 'CPP_STAR', 'CPP_FSLASH', 'CPP_PERCENT'),                         # 3
    ('right', 'UPLUS', 'UMINUS', 'CPP_EXCLAMATION', 'CPP_TILDE'),              # 2
                                                                               # 1 (unused in the C preprocessor)
)

def p_error(p):
    if p:
        raise Exception("Syntax error at '%s'" % p)
    else:
        raise Exception("Syntax error at EOF")

def p_expression_number(p):
    'expression : CPP_INTEGER'
    p[0] = Value(p[1])

def p_expression_group(t):
    'expression : CPP_LPAREN expression CPP_RPAREN'
    t[0] = t[2]

def p_expression_uplus(p):
    'expression : CPP_PLUS expression %prec UPLUS'
    p[0] = +Value(p[2])

def p_expression_uminus(p):
    'expression : CPP_MINUS expression %prec UMINUS'
    p[0] = -Value(p[2])

def p_expression_unop(p):
    """
    expression : CPP_EXCLAMATION expression
              | CPP_TILDE expression
    """
    if p[1] == '!':
        p[0] = Value(0) if (INTBASETYPE(Value(p[2]))!=0) else Value(1)
    elif p[1] == '~':
        p[0] = ~Value(p[2])

def p_expression_binop(p):
    """
    expression : expression CPP_STAR expression
              | expression CPP_FSLASH expression
              | expression CPP_PERCENT expression
              | expression CPP_PLUS expression
              | expression CPP_MINUS expression
              | expression CPP_LSHIFT expression
              | expression CPP_RSHIFT expression
              | expression CPP_LESS expression
              | expression CPP_LESSEQUAL expression
              | expression CPP_GREATER expression
              | expression CPP_GREATEREQUAL expression
              | expression CPP_EQUALITY expression
              | expression CPP_INEQUALITY expression
              | expression CPP_AMPERSAND expression
              | expression CPP_HAT expression
              | expression CPP_BAR expression
              | expression CPP_LOGICALAND expression
              | expression CPP_LOGICALOR expression
              | expression CPP_COMMA expression
    """
    # print [repr(p[i]) for i in range(0,4)]
    if p[2] == '*':
        p[0] = Value(p[1]) * Value(p[3])
    elif p[2] == '/':
        p[0] = Value(p[1]) / Value(p[3])
    elif p[2] == '%':
        p[0] = Value(p[1]) % Value(p[3])
    elif p[2] == '+':
        p[0] = Value(p[1]) + Value(p[3])
    elif p[2] == '-':
        p[0] = Value(p[1]) - Value(p[3])
    elif p[2] == '<<':
        p[0] = Value(p[1]) << Value(p[3])
    elif p[2] == '>>':
        p[0] = Value(p[1]) >> Value(p[3])
    elif p[2] == '<':
        p[0] = Value(p[1]) < Value(p[3])
    elif p[2] == '<=':
        p[0] = Value(p[1]) <= Value(p[3])
    elif p[2] == '>':
        p[0] = Value(p[1]) > Value(p[3])
    elif p[2] == '>=':
        p[0] = Value(p[1]) >= Value(p[3])
    elif p[2] == '==':
        p[0] = Value(p[1]) == Value(p[3])
    elif p[2] == '!=':
        p[0] = Value(p[1]) != Value(p[3])
    elif p[2] == '&':
        p[0] = Value(p[1]) & Value(p[3])
    elif p[2] == '^':
        p[0] = Value(p[1]) ^ Value(p[3])
    elif p[2] == '|':
        p[0] = Value(p[1]) | Value(p[3])
    elif p[2] == '&&':
        p[0] = Value(1) if (INTBASETYPE(Value(p[1]))!=0 and INTBASETYPE(Value(p[3]))!=0) else Value(0)
    elif p[2] == '||':
        p[0] = Value(1) if (INTBASETYPE(Value(p[1]))!=0 or INTBASETYPE(Value(p[3]))!=0) else Value(0)
    elif p[2] == ',':
        p[0] = Value(p[3])

def p_expression_conditional(p):
    'expression : expression CPP_QUESTION expression CPP_COLON expression'
    p[0] = Value(p[3]) if (INTBASETYPE(Value(p[1]))!=0) else Value(p[5])


class Evaluator(object):
    """Evaluator of #if C preprocessor expressions.
    
    >>> p = Preprocessor()
    >>> e = Evaluator(p)
    >>> e('5')
    Value(5)
    >>> e('5+6')
    Value(11)
    >>> e('5+6*2')
    Value(17)
    >>> e('5/2+6*2')
    Value(14)
    >>> e('5 < 6 <= 7')
    Value(1)
    >>> e('5 < 6 && 8 > 7')
    Value(1)
    >>> e('18446744073709551615 == -1')
    Value(1)
    >>> e('-9223372036854775809 == 9223372036854775807')
    Value(1)
    >>> e('-1 < 0U')
    Value(0U)
    >>> e('(( 0L && 0) || (!0L && !0 ))')
    Value(1)
    >>> e('(1)?2:3')
    Value(2)
    >>> e('(1 ? -1 : 0U) <= 0')
    Value(0)
    >>> e('0 && 10 / 0')
    Value(0)
    >>> e('0 ? 10 / 0 : 0')
    Value(0)
    >>> e('(3 ^ 5) != 6 || (3 | 5) != 7 || (3 & 5) != 1')
    Value(0)
    >>> e('1 << 2 != 4 || 8 >> 1 != 4')
    Value(0)
    >>> e('(2 || 3) != 1 || (2 && 3) != 1 || (0 || 4) != 1 || (0 && 5) != 0')
    Value(0)
    >>> e('-1 << 3U > 0')
    Value(0)
    """

    def __init__(self, preprocessor):
        self.preprocessor = preprocessor
        self.lexer = copy.copy(self.preprocessor.lexer)
        self.parser = yacc.yacc()
        
    def __nexttoken(self):
        while True:
            tok = self.lexer.token()
            if not tok or tok.type != 'CPP_WS':
                return tok

    def __call__(self, string):
        """Execute a fully macro expanded set of tokens representing an expression,
        returning the result of the evaluation.
        """
        if isinstance(string,list):
            string = ''.join(string)
        return self.parser.parse(string, lexer = self.lexer, tokenfunc = self.__nexttoken)



# L'\0' == 0
# 12 == 12
# 12L == 12
# -1 >= 0U
# (1<<2) == 4
# (-!+!9) == -1
# (2 || 3) == 1
# 1L * 3 != 3
# (!1L != 0) || (-1L != -1)
# 0177777 != 65535
# 0Xffff != 65535 || 0XFfFf != 65535
# 0L != 0 || 0l != 0
# 1U != 1 || 1u != 1
# 0 <= -1
# 1 << 2 != 4 || 8 >> 1 != 4
# (3 ^ 5) != 6 || (3 | 5) != 7 || (3 & 5) != 1
# (0 ? 1 : 2) != 2
# -1 << 3U > 0
# 0 && 10 / 0
# not_defined && 10 / not_defined
# 0 && 10 / 0 > 1
# (0) ? 10 / 0 : 0
# 0 == 0 || 10 / 0 > 1
# (15 >> 2 >> 1 != 1) || (3 << 2 << 1 != 24)
# (1 | 2) == 3 && 4 != 5 || 0
#  1  >  0
# '\123' != 83
# '\x1b' != '\033'
# 0 + (1 - (2 + (3 - (4 + (5 - (6 + (7 - (8 + (9 - (10 + (11 - (12 +          (13 - (14 + (15 - (16 + (17 - (18 + (19 - (20 + (21 - (22 + (23 -           (24 + (25 - (26 + (27 - (28 + (29 - (30 + (31 - (32 + 0))))))))))           )))))))))))))))))))))) == 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()

