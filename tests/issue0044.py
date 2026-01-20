
import unittest
import sys, os

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
                             '-o', 'tests/issue0044.i',
                             'tests/issue0044.h'])
        with open('tests/issue0044.i', 'rt') as ih:
            output = ih.read()
        os.remove('tests/issue0044.i')
        if output != shouldbe:
            print("Should be:\n" + shouldbe + "EOF\n", file=sys.stderr)
            print("\nWas:\n" + output + "EOF\n", file=sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output, shouldbe)


class empty_line_directive(unittest.TestCase, runner):
    pass
