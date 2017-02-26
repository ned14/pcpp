from __future__ import absolute_import, print_function
import unittest
from StringIO import StringIO

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor
        import os, time, sys

        start = time.clock()
        p = Preprocessor()
        p.parse(self.input)
        oh = StringIO()
        p.write(oh)
        end = time.clock()
        print("Preprocessed test in", end-start, "seconds")
        if oh.getvalue() != self.output:
            print("Should be:\n" + self.output, file = sys.stderr)
            print("\n\nWas:\n" + oh.getvalue(), file = sys.stderr)
        else:
            self.assertEqual(p.return_code, 0)
            self.assertEqual(oh.getvalue(), self.output)

            
# These preprocessor test fragments are borrowed from the C11 standard

class std1(unittest.TestCase, runner):
    input = r"""#define x 3
#define f(a) f(x * (a))
#undef x
#define x 2
#define g f
#define z z[0]
#define h g(~
#define m(a) a(w)
#define w 0,1
#define t(a) a
#define p() int
#define q(x) x
#define r(x,y) x ## y
#define str(x) # x
f(y+1) + f(f(z)) % t(t(g)(0) + t)(1);
g(x+(3,4)-w) | h 5) & m
(f)^m(m);
p() i[q()] = { q(1), r(2,3), r(4,), r(,5), r(,) };
char c[2][6] = { str(hello), str() };"""
    output = r"""# 14
f(2 * (y+1)) + f(2 * (f(2 * (z[0])))) % f(2 * (0)) + t(1);
f(2 * (2+(3,4)-0,1)) | f(2 * (~ 5)) & f(2 * (0,1))^m(0,1);
int i[] = { 1, 23, 4, 5, };
char c[2][6] = { "hello", "" };"""

class std2(unittest.TestCase, runner):
    input = r"""#define TWO_ARGS        a,b
#define sub( x, y)      (x - y)
    assert( sub( TWO_ARGS, 1) == 1);
"""
    output = r"""

    assert( (a,b - 1) == 1);"""

class std3(unittest.TestCase, runner):
    input = r"""#define t(x,y,z) x ## y ## z
int j[] = { t(1,2,3), t(,4,5), t(6,,7), t(8,9,),
t(10,,), t(,11,), t(,,12), t(,,) };
"""
    output = r"""
int j[] = { 123, 45, 67, 89,
10, 11, 12, };"""

class std4(unittest.TestCase, runner):
    input = r"""#define debug(...) fprintf(stderr, __VA_ARGS__)
#define showlist(...) puts(#__VA_ARGS__)
#define report(test, ...) ((test)?puts(#test):\
printf(__VA_ARGS__))
debug("Flag");
debug("X = %d\n", x);
showlist(The first, second, and third items.);
report(x>y, "x is %d but y is %d", x, y);
"""
    output = r"""



fprintf(stderr, "Flag");
fprintf(stderr, "X = %d\n", x);
puts("The first, second, and third items.");
((x>y)?puts("x>y"):printf( "x is %d but y is %d", x, y));"""

class std5(unittest.TestCase, runner):
    input = r"""#define Z   Z[0]
    assert( Z == 1);
#define AB  BA
#define BA  AB
    assert( AB == 1);
#define f(a)    a + f(a)
    assert( f( x) == 2);
#define g(a)    a + h( a)
#define h(a)    a + g( a)
    assert( g( x) == 4);
    assert( f( Z) == 2);
"""
    output = r"""
    assert( Z[0] == 1);


    assert( AB == 1);

    assert( x + f(x) == 2);


    assert( x + x + g( x) == 4);
    assert( Z[0] + f(Z[0]) == 2);"""


class std6(unittest.TestCase, runner):
    input = r"""#define MACRO_0         0
#define MACRO_1         1
#define glue( a, b)     a ## b
    assert( glue( MACRO_0, MACRO_1) == 2);
"""
    output = r"""


    assert( MACRO_0MACRO_1 == 2);"""


class std7(unittest.TestCase, runner):
    input = r"""#define MACRO_abcd  /*
    in comment
    */  abcd
MACRO_abcd
"""
    output = r"""
abcd"""


class std8(unittest.TestCase, runner):
    input = r"""#if 0
niall
#elif 0
douglas
#elif 1
foo
#endif
"""
    output = r"""




foo
"""


class std9(unittest.TestCase, runner):
    input = r'''#define str(x) # x
str(    niall  is      a   /* comment */
   pretty      boy           )
'''
    output = r'''
"niall is a pretty boy"'''


class std10(unittest.TestCase, runner):
    input = r"""#define MACRO_0         0
#define MACRO_1         1
#define glue( a, b)     a ## b
    assert( glue( MACRO_, 1) == 1);
"""
    output = r"""


    assert( 1 == 1);"""

class std11(unittest.TestCase, runner):
    input = r"""#define FUNC( a, b, c)      a + b + c
        FUNC
        (
            a,
            b,
            c
        )
        == 6
"""
    output = r"""
        a + b + c





        == 6"""

