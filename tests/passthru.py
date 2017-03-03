from __future__ import absolute_import, print_function
import unittest
from StringIO import StringIO

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor, OutputDirective
        import os, time, sys

        class PassThruPreprocessor(Preprocessor):
            def on_include_not_found(self,is_system_include,curdir,includepath):
                raise OutputDirective()

            def on_unknown_macro_in_expr(self,tok):
                pass  # Pass through as expanded as possible
                
            def on_directive_unknown(self,directive,toks):
                if directive.value == 'error' or directive.value == 'warning':
                    super(Preprocessor, self).on_directive_unknown(directive,toks)
                # Pass through
                raise OutputDirective()                

        start = time.clock()
        p = PassThruPreprocessor()
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
#endif"""

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
#endif"""

class test4(unittest.TestCase, runner):
    input = r"""#define ALSO_UNKNOWN 1
#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""
#if UNKNOWN
A
#elif 1
B
#else
C
#endif"""

class test5(unittest.TestCase, runner):
    input = r"""#define ALSO_UNKNOWN 0
#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""
#if UNKNOWN
A


#else
C
#endif"""

class test6(unittest.TestCase, runner):
    input = r"""#define UNKNOWN 1
#if UNKNOWN
A
#elif ALSO_UNKNOWN
B
#else
C
#endif"""
    output = r"""

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
    output = r"""


#if ALSO_UNKNOWN
B
#else
C
#endif"""


class test99(unittest.TestCase, runner):
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
    output = r"""# 67
_1_0_std_std_01320023
namespace boost { namespace outcome { inline namespace _1_0_std_std_01320023 {"""