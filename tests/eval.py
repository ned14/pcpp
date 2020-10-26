from __future__ import absolute_import, print_function
import unittest, time
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
try:
    clock = time.process_time
except:
    clock = time.clock

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor
        import os, sys

        start = clock()
        #p = Preprocessor()
        #lines = p.group_lines(self.input, '')
        #for x in lines:
        #    print(x)
        p = Preprocessor()
        p.parse(self.input)
        oh = StringIO()
        p.write(oh)
        end = clock()
        print("Preprocessed test in", end-start, "seconds")
        if oh.getvalue() != self.output:
            print("Should be:\n" + self.output, file = sys.stderr)
            print("\n\nWas:\n" + oh.getvalue(), file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(oh.getvalue(), self.output)


class eval1(unittest.TestCase, runner):
    input = r"""#if -1 >= 0U
correct
#endif"""
    output = r"""
correct
"""

class eval2(unittest.TestCase, runner):
    input = r"""#if 1<<2 == 4
correct
#endif"""
    output = r"""
correct
"""

class eval3(unittest.TestCase, runner):
    input = r"""#if (-!+!9) == -1
correct
#endif"""
    output = r"""
correct
"""

class eval4(unittest.TestCase, runner):
    input = r"""#if (2 || 3) == 1
correct
#endif"""
    output = r"""
correct
"""
