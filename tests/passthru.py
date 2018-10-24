from __future__ import absolute_import, print_function
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor, OutputDirective
        import os, time, sys

        class PassThruPreprocessor(Preprocessor):
            def on_include_not_found(self,is_system_include,curdir,includepath):
                raise OutputDirective()

            def on_unknown_macro_in_defined_expr(self,tok):
                return None  # Pass through as expanded as possible
                
            def on_unknown_macro_in_expr(self,tok):
                return None  # Pass through as expanded as possible
                
            def on_directive_handle(self,directive,toks,ifpassthru):
                super(PassThruPreprocessor, self).on_directive_handle(directive,toks,ifpassthru)
                return None  # Pass through where possible

            def on_directive_unknown(self,directive,toks,ifpassthru):
                if directive.value == 'error' or directive.value == 'warning':
                    super(PassThruPreprocessor, self).on_directive_unknown(directive,toks)
                # Pass through
                raise OutputDirective()                

            def on_comment(self,tok):
                # Pass through
                return True

        start = time.clock()
        p = PassThruPreprocessor()
        p.parse(self.input)
        oh = StringIO()
        p.write(oh)
        end = time.clock()
        print("Preprocessed test in", end-start, "seconds")
        if oh.getvalue() != self.output:
            print("Should be:\n" + self.output + "EOF\n", file = sys.stderr)
            print("\nWas:\n" + oh.getvalue()+"EOF\n", file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(oh.getvalue(), self.output)

            
class test1(unittest.TestCase, runner):
    input = r"""#if 5
I am five
#else
I am not five
#endif"""
    output = r"""
I am five
"""

class test2(unittest.TestCase, runner):
    input = r"""#if UNKNOWN
I am five
#else
I am not five
#endif"""
    output = r"""#if UNKNOWN
I am five
#else
I am not five
#endif
"""

class test3(unittest.TestCase, runner):
    input = r"""#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif
"""

class test4(unittest.TestCase, runner):
    input = r"""#define ALSO_UNKNOWN 1
#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""#define ALSO_UNKNOWN 1
#if UNKNOWN
A
#elif 1
B
#else
C
#endif
"""

class test5(unittest.TestCase, runner):
    input = r"""#define ALSO_UNKNOWN 0
#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""#define ALSO_UNKNOWN 0
#if UNKNOWN
A


#else
C
#endif
"""

class test6(unittest.TestCase, runner):
    input = r"""#define UNKNOWN 1
#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""#define UNKNOWN 1

A
"""

class test7(unittest.TestCase, runner):
    input = r"""#define UNKNOWN 0
#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""#define UNKNOWN 0


#if ALSO_UNKNOWN
B
#else
C
#endif
"""

class test8(unittest.TestCase, runner):
    input = r"""#define UNKNOWN 0
#if UNKNOWN
#if 1
A
#else
AA
#endif
#elif ALSO_UNKNOWN
#if 1
B
#else
BB
#endif
#else
#if 1
C
#else
CC
#endif
#endif"""
    output = r"""#define UNKNOWN 0






#if ALSO_UNKNOWN

B



#else

C



#endif
"""

class test9(unittest.TestCase, runner):
    input = r"""#define KNOWN 0
#if defined(UNKNOWN) || KNOWN
A
#endif
"""
    output = r"""#define KNOWN 0
#if defined(UNKNOWN) || 0
A
#endif
"""

class test10(unittest.TestCase, runner):
    input = r"""#if !defined(__cpp_constexpr)
#if __cplusplus >= 201402L
#define __cpp_constexpr 201304  // relaxed constexpr
#else
#define __cpp_constexpr 190000
#endif
#endif
"""
    output = r"""#if !defined(__cpp_constexpr)
#if __cplusplus >= 201402
#define __cpp_constexpr 201304  // relaxed constexpr
#else
#define __cpp_constexpr 190000
#endif
#endif
"""

class test11(unittest.TestCase, runner):
    input = r"""#define __cpp_constexpr 201304
#if !defined(__cpp_constexpr)
#if __cplusplus >= 201402L
#define __cpp_constexpr 201304  // relaxed constexpr
#else
#define __cpp_constexpr 190000
#endif
#endif
#ifndef BOOSTLITE_CONSTEXPR
#if __cpp_constexpr >= 201304
#define BOOSTLITE_CONSTEXPR constexpr
#endif
#endif
#ifndef BOOSTLITE_CONSTEXPR
#define BOOSTLITE_CONSTEXPR
#endif
"""
    output = r"""#define __cpp_constexpr 201304
#line 9
#ifndef BOOSTLITE_CONSTEXPR

#define BOOSTLITE_CONSTEXPR constexpr

#endif
"""

class test12(unittest.TestCase, runner):
    input = r"""
#define BOOST_OUTCOME_DISABLE_PREPROCESSED_INTERFACE_FILE

#ifndef BOOST_OUTCOME_DISABLE_PREPROCESSED_INTERFACE_FILE

#else

#if defined(_MSC_VER) && !defined(__clang__)
#define BOOST_OUTCOME_HEADERS_PATH2 BOOST_OUTCOME_VERSION_GLUE(v, BOOST_OUTCOME_HEADERS_VERSION, /monad.hpp)
#elif 1
#define BOOST_OUTCOME_HEADERS_PATH2 BOOST_OUTCOME_VERSION_GLUE(v, BOOST_OUTCOME_HEADERS_VERSION,)/monad.hpp
#endif

#endif
"""
    output = r"""
#define BOOST_OUTCOME_DISABLE_PREPROCESSED_INTERFACE_FILE





#if defined(_MSC_VER) && !defined(__clang__)
#define BOOST_OUTCOME_HEADERS_PATH2 BOOST_OUTCOME_VERSION_GLUE(v, BOOST_OUTCOME_HEADERS_VERSION, /monad.hpp)
#elif 1
#define BOOST_OUTCOME_HEADERS_PATH2 BOOST_OUTCOME_VERSION_GLUE(v, BOOST_OUTCOME_HEADERS_VERSION,)/monad.hpp
#endif
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
/*
multiline
comment
*/

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
    output = r"""
/*
a
comment
that
spans
eight
lines
*/

void shouldBeOnLineEleven();
"""
