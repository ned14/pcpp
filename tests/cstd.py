from __future__ import absolute_import, print_function
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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
    output = r"""#line 15
f(2 * (y+1)) + f(2 * (f(2 * (z[0])))) % f(2 * (0)) + t(1);
f(2 * (2+(3,4)-0,1)) | f(2 * (~ 5)) & f(2 * (0,1))^m(0,1);

int i[] = { 1, 23, 4, 5, };
char c[2][6] = { "hello", "" };
"""

class std2(unittest.TestCase, runner):
    input = r"""#define TWO_ARGS        a,b
#define sub( x, y)      (x - y)
    assert( sub( TWO_ARGS, 1) == 1);
"""
    output = r"""

    assert( (a,b - 1) == 1);
"""

class std3(unittest.TestCase, runner):
    input = r"""#define t(x,y,z) x ## y ## z
int j[] = { t(1,2,3), t(,4,5), t(6,,7), t(8,9,),
t(10,,), t(,11,), t(,,12), t(,,) };
"""
    output = r"""
int j[] = { 123, 45, 67, 89,
10, 11, 12, };
"""

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
((x>y)?puts("x>y"):printf( "x is %d but y is %d", x, y));
"""

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
    assert( Z[0] + f(Z[0]) == 2);
"""


class std6(unittest.TestCase, runner):
    input = r"""#define MACRO_0         0
#define MACRO_1         1
#define glue( a, b)     a ## b
    assert( glue( MACRO_0, MACRO_1) == 2);
"""
    output = r"""


    assert( MACRO_0MACRO_1 == 2);
"""


class std7(unittest.TestCase, runner):
    input = r"""#if     0
    "nonsence"; /*
#else
    still in
    comment     */
#else
#define MACRO_abcd  /*
    in comment
    */  abcd
#endif
    assert( MACRO_abcd == 4);
"""
    output = r"""#line 11
    assert( abcd == 4);
"""

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
"niall is a pretty boy"
'''


class std10(unittest.TestCase, runner):
    input = r"""#define MACRO_0         0
#define MACRO_1         1
#define glue( a, b)     a ## b
    assert( glue( MACRO_, 1) == 1);
"""
    output = r"""


    assert( 1 == 1);
"""

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





        == 6
"""

class test12(unittest.TestCase, runner):
    input = r"""
#define BOOSTLITE_GLUE(x, y) x y

#define BOOSTLITE_RETURN_ARG_COUNT(_1_, _2_, _3_, _4_, _5_, _6_, _7_, _8_, count, ...) count
#define BOOSTLITE_EXPAND_ARGS(args) BOOSTLITE_RETURN_ARG_COUNT args
#define BOOSTLITE_COUNT_ARGS_MAX8(...) BOOSTLITE_EXPAND_ARGS((__VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0))

#define BOOSTLITE_OVERLOAD_MACRO2(name, count) name##count
#define BOOSTLITE_OVERLOAD_MACRO1(name, count) BOOSTLITE_OVERLOAD_MACRO2(name, count)
#define BOOSTLITE_OVERLOAD_MACRO(name, count) BOOSTLITE_OVERLOAD_MACRO1(name, count)

#define BOOSTLITE_CALL_OVERLOAD(name, ...) BOOSTLITE_GLUE(BOOSTLITE_OVERLOAD_MACRO(name, BOOSTLITE_COUNT_ARGS_MAX8(__VA_ARGS__)), (__VA_ARGS__))

#define BOOSTLITE_GLUE_(x, y) x y

#define BOOSTLITE_RETURN_ARG_COUNT_(_1_, _2_, _3_, _4_, _5_, _6_, _7_, _8_, count, ...) count
#define BOOSTLITE_EXPAND_ARGS_(args) BOOSTLITE_RETURN_ARG_COUNT_ args
#define BOOSTLITE_COUNT_ARGS_MAX8_(...) BOOSTLITE_EXPAND_ARGS_((__VA_ARGS__, 8, 7, 6, 5, 4, 3, 2, 1, 0))

#define BOOSTLITE_OVERLOAD_MACRO2_(name, count) name##count
#define BOOSTLITE_OVERLOAD_MACRO1_(name, count) BOOSTLITE_OVERLOAD_MACRO2_(name, count)
#define BOOSTLITE_OVERLOAD_MACRO_(name, count) BOOSTLITE_OVERLOAD_MACRO1_(name, count)

#define BOOSTLITE_CALL_OVERLOAD_(name, ...) BOOSTLITE_GLUE_(BOOSTLITE_OVERLOAD_MACRO_(name, BOOSTLITE_COUNT_ARGS_MAX8_(__VA_ARGS__)), (__VA_ARGS__))

#define BOOSTLITE_BIND_STRINGIZE(a) #a
#define BOOSTLITE_BIND_STRINGIZE2(a) BOOSTLITE_BIND_STRINGIZE(a)
#define BOOSTLITE_BIND_NAMESPACE_VERSION8(a, b, c, d, e, f, g, h) a##_##b##_##c##_##d##_##e##_##f##_##g##_##h
#define BOOSTLITE_BIND_NAMESPACE_VERSION7(a, b, c, d, e, f, g) a##_##b##_##c##_##d##_##e##_##f##_##g
#define BOOSTLITE_BIND_NAMESPACE_VERSION6(a, b, c, d, e, f) a##_##b##_##c##_##d##_##e##_##f
#define BOOSTLITE_BIND_NAMESPACE_VERSION5(a, b, c, d, e) a##_##b##_##c##_##d##_##e
#define BOOSTLITE_BIND_NAMESPACE_VERSION4(a, b, c, d) a##_##b##_##c##_##d
#define BOOSTLITE_BIND_NAMESPACE_VERSION3(a, b, c) a##_##b##_##c
#define BOOSTLITE_BIND_NAMESPACE_VERSION2(a, b) a##_##b
#define BOOSTLITE_BIND_NAMESPACE_VERSION1(a) a
#define BOOSTLITE_BIND_NAMESPACE_VERSION(...) BOOSTLITE_CALL_OVERLOAD(BOOSTLITE_BIND_NAMESPACE_VERSION, __VA_ARGS__)

#define BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT2(name, modifier) modifier namespace name {
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT1(name) namespace name {
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT(...) BOOSTLITE_CALL_OVERLOAD_(BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT, __VA_ARGS__)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND8(a, b, c, d, e, f, g, h) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND7(b, c, d, e, f, g, h)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND7(a, b, c, d, e, f, g) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND6(b, c, d, e, f, g)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND6(a, b, c, d, e, f) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND5(b, c, d, e, f)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND5(a, b, c, d, e) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND4(b, c, d, e)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND4(a, b, c, d) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND3(b, c, d)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND3(a, b, c) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND2(b, c)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND2(a, b) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND1(b)
#define BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND1(a) BOOSTLITE_BIND_NAMESPACE_BEGIN_NAMESPACE_SELECT a
#define BOOSTLITE_BIND_NAMESPACE_BEGIN(...) BOOSTLITE_CALL_OVERLOAD(BOOSTLITE_BIND_NAMESPACE_BEGIN_EXPAND, __VA_ARGS__)

#define BOOST_OUTCOME_VERSION_GLUE2(a, b, c) a##b##c
#define BOOST_OUTCOME_VERSION_GLUE(a, b, c) BOOST_OUTCOME_VERSION_GLUE2(a, b, c)

#define BOOST_OUTCOME_VERSION_MAJOR 1
#define BOOST_OUTCOME_VERSION_MINOR 0
#define BOOST_OUTCOME_VERSION_PATCH 0
#define BOOST_OUTCOME_VERSION_REVISION 0
#define BOOST_OUTCOME_NAMESPACE_VERSION BOOST_OUTCOME_VERSION_GLUE(BOOST_OUTCOME_VERSION_MAJOR, _, BOOST_OUTCOME_VERSION_MINOR)

#define BOOST_OUTCOME_PREVIOUS_COMMIT_UNIQUE 01320023

#define BOOST_OUTCOME_V1_STL11_IMPL std
#define BOOST_OUTCOME_V1_ERROR_CODE_IMPL std
#define BOOST_OUTCOME_V1 (boost), (outcome), (BOOSTLITE_BIND_NAMESPACE_VERSION(, BOOST_OUTCOME_NAMESPACE_VERSION, BOOST_OUTCOME_V1_STL11_IMPL, BOOST_OUTCOME_V1_ERROR_CODE_IMPL, BOOST_OUTCOME_PREVIOUS_COMMIT_UNIQUE), inline)
#define BOOST_OUTCOME_V1_NAMESPACE_BEGIN BOOSTLITE_BIND_NAMESPACE_BEGIN(BOOST_OUTCOME_V1)

BOOSTLITE_BIND_NAMESPACE_VERSION(, BOOST_OUTCOME_NAMESPACE_VERSION, BOOST_OUTCOME_V1_STL11_IMPL, BOOST_OUTCOME_V1_ERROR_CODE_IMPL, BOOST_OUTCOME_PREVIOUS_COMMIT_UNIQUE)
BOOST_OUTCOME_V1_NAMESPACE_BEGIN
"""
    output = r"""#line 67
_1_0_std_std_01320023
namespace boost { namespace outcome { inline namespace _1_0_std_std_01320023 {
"""

class test13(unittest.TestCase, runner):
    input = r"""
#define _CRT_INTERNAL_NONSTDC_NAMES                                            \
    (                                                                          \
        ( defined _CRT_DECLARE_NONSTDC_NAMES && _CRT_DECLARE_NONSTDC_NAMES) || \
        (!defined _CRT_DECLARE_NONSTDC_NAMES && !__STDC__                 )    \
    )
#if _CRT_INTERNAL_NONSTDC_NAMES
foo
#endif
"""
    output = r"""#line 8
foo
"""

class test14(unittest.TestCase, runner):
    input = r"""
# if defined __GNUC__ // NOTE: GNUC is also defined for Clang
#   if (__GNUC__ == 4) && (__GNUC_MINOR__ >= 8)
#     define TR2_OPTIONAL_GCC_4_8_AND_HIGHER___
#   elif (__GNUC__ > 4)
#     define TR2_OPTIONAL_GCC_4_8_AND_HIGHER___
#   endif
# 
#   if (__GNUC__ == 4) && (__GNUC_MINOR__ >= 7)
#     define TR2_OPTIONAL_GCC_4_7_AND_HIGHER___
#   elif (__GNUC__ > 4)
#     define TR2_OPTIONAL_GCC_4_7_AND_HIGHER___
#   endif
#
#   if (__GNUC__ == 4) && (__GNUC_MINOR__ == 8) && (__GNUC_PATCHLEVEL__ >= 1)
#     define TR2_OPTIONAL_GCC_4_8_1_AND_HIGHER___
#   elif (__GNUC__ == 4) && (__GNUC_MINOR__ >= 9)
#     define TR2_OPTIONAL_GCC_4_8_1_AND_HIGHER___
#   elif (__GNUC__ > 4)
#     define TR2_OPTIONAL_GCC_4_8_1_AND_HIGHER___
#   endif
# endif
foo
"""
    output = r"""#line 23
foo
"""

class test15(unittest.TestCase, runner):
    input = r"""#define f(type) type type##_base
f(g)
"""
    output = r"""
g g_base
"""

class test16(unittest.TestCase, runner):
    # #if ((1?2:3) == 2) is known to fail
    input = r"""#if (((1)?2:3) == 2)
hi
#endif
"""
    output = r"""
hi
"""

class test17(unittest.TestCase, runner):
    input = r"""#if L'\0' == 0
hi
#endif
"""
    output = r"""
hi
"""

class test18(unittest.TestCase, runner):
    input = r"""
/*
multiline
comment
*/

void shouldBeOnLineSeven();
"""
    output = r"""





void shouldBeOnLineSeven();
"""


class test19(unittest.TestCase, runner):
    input = r"""
/*
a
comment
that
spans
eight
lines
*/

void shouldBeOnLineEleven();"""
    output = r"""#line 11
void shouldBeOnLineEleven();
"""
