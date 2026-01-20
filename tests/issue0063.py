
import unittest
import sys, os

class runner(object):
    def runTest(self):
        from pcpp import CmdPreprocessor
        p = CmdPreprocessor(['pcpp'] + self.options + [
                             '-o', 'tests/issue0063.i',
                             'tests/issue0063.c'])
        with open('tests/issue0063.i', 'rt') as ih:
            output = ih.read()
        os.remove('tests/issue0063.i')
        if output != self.shouldbe:
            print("Should be:\n" + self.shouldbe + "EOF\n", file=sys.stderr)
            print("\nWas:\n" + output + "EOF\n", file=sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output, self.shouldbe)


class include_after_continued_macro1(unittest.TestCase, runner):
    options = []
    shouldbe = r'''#line 1 "tests/issue0063.h"
int f();
int f();
'''

class include_after_continued_macro2(unittest.TestCase, runner):
    options = [ '--passthru-defines' ]
    shouldbe = r'''#line 1 "tests/issue0063.c"
#define x
#line 1 "tests/issue0063.h"
int f();
#line 6 "tests/issue0063.c"
#undef x
#define x
#line 1 "tests/issue0063.h"
int f();
'''

class include_after_continued_macro3(unittest.TestCase, runner):
    options = [ '--line-directive=', '--passthru-defines' ]
    shouldbe = r'''#define x
int f();
#undef x
#define x
int f();
'''
