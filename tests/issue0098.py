
import unittest, sys
from io import StringIO

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor
        p = Preprocessor()
        p.include_next_enabled = True
        
        # Add the test directories to the search path
        p.add_path('tests/issue0098/dir1')
        p.add_path('tests/issue0098/dir2')
        p.add_path('tests/issue0098/dir3')
        p.add_path('tests/issue0098/dir4')

        p.parse(self.input)        
        output = StringIO()
        p.write(output)
        if output.getvalue() != self.shouldbe:
            print("Should be:\n" + self.shouldbe + "EOF\n", file=sys.stderr)
            print("\nWas:\n" + output.getvalue() + "EOF\n", file=sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output.getvalue(), self.shouldbe)


class include_next_works(unittest.TestCase, runner):
    input = r'''#include_next "header.h"
'''
    shouldbe = r'''#line 1 "tests/issue0098/dir1/header.h"
header1
#line 1 "tests/issue0098/dir2/header.h"
header2
#line 1 "tests/issue0098/dir3/header.h"
header3
#line 1 "tests/issue0098/dir4/header.h"
header4
'''

class has_include_works(unittest.TestCase, runner):
    input = r'''#ifdef __has_include
ifdef
#endif
#ifndef __has_include
ifndef
#endif
#if defined(__has_include)
defined
#endif
#if __has_include("header.h")
header
#endif
'''
    shouldbe = r'''
ifdef





defined


header
'''

if __name__ == '__main__':
    unittest.main()