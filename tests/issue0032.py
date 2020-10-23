from __future__ import absolute_import, print_function
import unittest, sys

shouldbe = r'''#line 1 "tests/issue0030/source3.c"
2
'''

class runner(object):
    def runTest(self):
        from pcpp import CmdPreprocessor
        p = CmdPreprocessor(['pcpp', '--time',
                             'tests/issue0030/source1.c'])
        self.assertEqual(p.return_code, 0)

class no_output_file(unittest.TestCase, runner):
    pass
