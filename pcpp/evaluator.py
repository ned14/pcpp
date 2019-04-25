#!/usr/bin/python
# Python C99 conforming preprocessor expression evaluator
# (C) 2019 Niall Douglas http://www.nedproductions.biz/
# Started: Apr 2019

from __future__ import generators, print_function, absolute_import

import os, sys
if __name__ == '__main__' and __package__ is None:
    sys.path.append( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
from pcpp.preprocessor import OutputDirective, Action, STRING_TYPES

INTMAXBITS = 64

class Int(int):
    """A signed integer within a preprocessor expression, bounded
    to within INT_MIN and INT_MAX. Overflow is handled like a CPU,
    despite being UB, as that's what GCC and clang do.
    
    >>> Int(5)
    Int(5)
    >>> Int(5) * Int(2)
    Int(10)
    >>> Int(5) * 2
    Int(10)
    >>> Int(9223372036854775808)
    Int(-9223372036854775808)
    >>> Int(-9223372036854775809)
    Int(9223372036854775807)
    >>> Int(18446744073709551615)
    Int(-1)
    """
    INT_MIN = -(1 << (INTMAXBITS - 1))
    INT_MAX = (1 << (INTMAXBITS - 1)) - 1
    INT_MASK = (1 << INTMAXBITS) - 1
    @classmethod
    def __clamp(cls, value):
        return ((value - cls.INT_MIN) & cls.INT_MASK) + cls.INT_MIN
    def __new__(cls, value, *args, **kwargs):
        return super(Int, cls).__new__(cls, cls.__clamp(value))
    def __add__(self, other):
        return self.__class__(self.__clamp(super(Int, self).__add__(other)))
    def __sub__(self, other):
        return self.__class__(self.__clamp(super(Int, self).__sub__(other)))
    def __mul__(self, other):
        return self.__class__(self.__clamp(super(Int, self).__mul__(other)))
    def __div__(self, other):
        return self.__class__(self.__clamp(super(Int, self).__div__(other)))
    def __repr__(self):
        return "Int(%d)" % int(self)

#def execute_expr(token):
#    """Execute a fully macro expanded set of tokens representing an expression,
#    returning the result of the evaluation.
#    
#    >>> execute_expr('5')
#    5
#    """
#    if isinstance(tokens,STRING_TYPES):
#        tokens = self.tokenize(tokens)
#    return 

# 18446744073709551615 == -1
# -9223372036854775809 == 9223372036854775807
# (                                                                                  ( 0L && _CRT_DECLARE_NONSTDC_NAMES) ||         (!0L && !__STDC__                 )        )
# 0L
# (((1)?2:3) == 2)
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

