from __future__ import absolute_import, print_function
import unittest, time
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor, OutputDirective, Action
        import os, sys, re

        p = Preprocessor()
        p.parse(self.input)
        with StringIO() as oh:
            p.write(oh)
            print("ok")
            if oh.getvalue() != self.output:
                print("Should be:\n" + self.output + "EOF\n", file = sys.stderr)
                print("\nWas:\n" + oh.getvalue()+"EOF\n", file = sys.stderr)
            self.assertEqual(p.return_code, 0)
            self.assertEqual(oh.getvalue(), self.output)

class pp_number_pasting(unittest.TestCase, runner):
    input = """#define CAT_(A,B)A##B
#define CAT(A,B)CAT_(A,B)
#define Ox 0x
#if CAT(Ox,1)
PP_NUMBER pasted ok
#else
PP_NUMBER paste fail
#endif
"""
    output = """



PP_NUMBER pasted ok
"""