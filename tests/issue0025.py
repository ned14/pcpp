
import unittest

class issue0025(unittest.TestCase):
    def runTest(self):
        from pcpp import Preprocessor
        import os, sys

        p = Preprocessor()
        path = 'tests/issue0025/main.c'
        with open(path, 'rt') as ih:
            p.parse(ih.read(), path)
        with open('tests/issue0025.i', 'w') as oh:
            p.write(oh)
        with open('tests/issue0025.i', 'r') as ih:
            was = ih.read()
        with open('tests/issue0025-ref.i', 'r') as ih:
            shouldbe = ih.read()
        if was != shouldbe:
            print("Should be:\n" + shouldbe, file = sys.stderr)
            print("\n\nWas:\n" + was, file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(was, shouldbe)
