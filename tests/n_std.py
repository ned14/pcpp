
import unittest, time, difflib
clock = time.process_time

class n_std(unittest.TestCase):
    def runTest(self):
        from pcpp import Preprocessor
        import os

        start = clock()
        p = Preprocessor()
        p.compress = 1
        p.line_directive = '#'
        p.define('__STDC__ 1')
        p.define('__STDC_VERSION__ 199901L')
        p.define('__DATE__ "Jan 13 2020"')
        p.define('__TIME__ "10:47:38"')
        p.define('NO_SYSTEM_HEADERS')
        path = 'tests/test-c/n_std.c'
        with open(path, 'rt') as ih:
            p.parse(ih.read(), path)
        with open('tests/n_std.i', 'w') as oh:
            p.write(oh)
        end = clock()
        print("Preprocessed", path, "in", end-start, "seconds")
        self.assertEqual(p.return_code, 0)

        with open('tests/n_std.i', 'rt') as ih:
            written = ih.readlines()
        with open('tests/n_std-pcpp.i', 'rt') as ih:
            reference = ih.readlines()
        if written != reference:
            print("pcpp is not emitting its reference output! Differences:")
            for line in difflib.unified_diff(reference, written, fromfile='n_std-pcpp.i', tofile='n_std.i'):
                print(line, end='')
            self.assertTrue(False)
        
