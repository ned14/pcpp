from __future__ import absolute_import, print_function
import unittest
import sys

shouldbe = r'''a1



b1
'''


class runner(object):
    def runTest(self):
        from pcpp import CmdPreprocessor
        # failure: p = CmdPreprocessor(['pcpp', '--line-directive', '#line',
        # p = CmdPreprocessor(['pcpp', '--line-directive', 'nothing',
        # p = CmdPreprocessor(['pcpp', '--line-directive', 'None',
        p = CmdPreprocessor(['pcpp', '--line-directive', '',
                             '-o', 'tests/line-directive-nothing.i',
                             'tests/line-directive-nothing.h'])
        with open('tests/line-directive-nothing.i', 'rt') as ih:
            output = ih.read()
        if output != shouldbe:
            print("Should be:\n" + shouldbe + "EOF\n", file=sys.stderr)
            print("\nWas:\n" + output + "EOF\n", file=sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output, shouldbe)


class multiple_input_files(unittest.TestCase, runner):
    pass
