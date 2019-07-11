from __future__ import absolute_import, print_function
import unittest, sys

shouldbe = r'''#line 1 "tests/issue0030/source3.c"
2
'''

class runner(object):
    def runTest(self):
        from pcpp import CmdPreprocessor
        p = CmdPreprocessor(['pcpp', '-o', 'tests/issue0030.c',
                             'tests/issue0030/source1.c',
                             'tests/issue0030/source2.c',
                             'tests/issue0030/source3.c'])
        with open('tests/issue0030.c', 'rt') as ih:
            output = ih.read()
        if output != shouldbe:
            print("Should be:\n" + shouldbe + "EOF\n", file = sys.stderr)
            print("\nWas:\n" + output + "EOF\n", file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output, shouldbe)

class multiple_input_files(unittest.TestCase, runner):
    pass
