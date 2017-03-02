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
