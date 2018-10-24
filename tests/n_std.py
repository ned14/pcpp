from __future__ import absolute_import, print_function
import unittest

class n_std(unittest.TestCase):
    def runTest(self):
        from pcpp import Preprocessor
        import os, time

        start = time.clock()
        p = Preprocessor()
        p.compress = 1
        p.define('__STDC__ 1')
        p.define('__STDC_VERSION__ 199901L')
        p.define('NO_SYSTEM_HEADERS')
        path = 'tests/test-c/n_std.c'
        with open(path, 'rt') as ih:
            p.parse(ih.read(), path)
        with open('tests/n_std.i', 'w') as oh:
            p.write(oh)
        end = time.clock()
        print("Preprocessed", path, "in", end-start, "seconds")
        self.assertEqual(p.return_code, 0)
        
