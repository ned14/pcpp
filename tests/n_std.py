from __future__ import absolute_import, print_function
import unittest

class n_std(unittest.TestCase):
    def runTest(self):
        from pcpp import Preprocessor
        import os, time

        start = time.clock()
        p = Preprocessor(quiet=False)
        p.cmd_define('__STDC__ 1')
        p.cmd_define('__STDC_VERSION__ 199901L')
        p.cmd_define('NO_SYSTEM_HEADERS')
        path = 'tests/test-c/n_std.c'
        with open(path, 'rt') as ih:
            p.add_raw_lines(ih.readlines(), path)
        p.preprocess()
        with open('tests/n_std.i', 'w') as oh:
            oh.writelines(p.get_lines())
        end = time.clock()
        print("Preprocessed", path, "in", end-start, "seconds")
        print("  Opening and reading files took", p.time_reading_files)
        print("  Decommenting and adding raw lines took", p.time_adding_raw_lines)
        print("  Executing preprocessor commands took", p.time_executing)
        print("  Expanding macros in lines took", p.time_expanding_macros)
        print("\n  Individual commands:")
        for cmd, time in p.time_cmds.items():
            print("    #"+cmd+":", time)
        self.assertEqual(p.return_code, 0)
        
