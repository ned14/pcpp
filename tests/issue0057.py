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
        from pcpp import Preprocessor, OutputDirective, Action
        import os, sys, re

        class PassThruPreprocessor(Preprocessor):
            def __init__(self):
                super(PassThruPreprocessor, self).__init__()
                self.passthru_includes = re.compile('.*/issue0057.*')
            def on_include_not_found(self,is_malformed,is_system_include,curdir,includepath):
                raise OutputDirective(Action.IgnoreAndPassThrough)

        start = clock()
        p = PassThruPreprocessor()
        p.parse(self.input)
        oh = StringIO()
        p.write(oh)
        end = clock()
        print("Preprocessed test in", end-start, "seconds")
        if oh.getvalue() != self.output:
            print("Should be:\n" + self.output + "EOF\n", file = sys.stderr)
            print("\nWas:\n" + oh.getvalue()+"EOF\n", file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(oh.getvalue(), self.output)

            
class newline_after_passthru_include1(unittest.TestCase, runner):
    input = r"""#include "tests/issue0057.h"
filetoken1
#include "tests/issue0057.h"
filetoken2
"""
    output = r"""#include "tests/issue0057.h"
filetoken1
#include "tests/issue0057.h"
filetoken2
"""

class newline_after_passthru_include2(unittest.TestCase, runner):
    input = r"""#include "tests/issue0057x.h"
filetoken1
#include "tests/issue0057x.h"
filetoken2
"""
    output = r"""#include "tests/issue0057x.h"
filetoken1
#include "tests/issue0057x.h"
filetoken2
"""

class newline_after_passthru_include3(unittest.TestCase, runner):
    input = r"""#include "unfoundfile"
filetoken1
#include "unfoundfile"
filetoken2
"""
    output = r"""#include "unfoundfile"
filetoken1
#include "unfoundfile"
filetoken2
"""
