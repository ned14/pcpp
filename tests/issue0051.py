from __future__ import absolute_import, print_function
import unittest
import sys

class runner(object):
    def runTest(self):
        from pcpp import CmdPreprocessor
        p = CmdPreprocessor(['pcpp'] + self.options + [
                             '-o', 'tests/issue0051.i',
                             'tests/issue0051.c'])
        with open('tests/issue0051.i', 'rt') as ih:
            output = ih.read()
        if output != self.shouldbe:
            print("Should be:\n" + self.shouldbe + "EOF\n", file=sys.stderr)
            print("\nWas:\n" + output + "EOF\n", file=sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output, self.shouldbe)


class normal_inclusion(unittest.TestCase, runner):
    options = []
    shouldbe = r'''#line 3 "tests/issue0051.h"
void my_func1();
void my_func2();
void my_func3();
#line 4 "tests/issue0051.c"
  TRUE
'''

class exclude_inclusion(unittest.TestCase, runner):
    options = ['--passthru-includes', '"issue0051.h"']
    shouldbe = r'''#line 1 "tests/issue0051.c"
#include "issue0051.h"


  TRUE
'''
