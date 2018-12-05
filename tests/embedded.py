from __future__ import absolute_import, print_function
import unittest, sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class embedded1(unittest.TestCase):
    def runTest(self):
        from pcpp import Preprocessor
        output = r'''

a
'''

        p = Preprocessor()
        p.define('BAR FOO')
        p.parse(r'''#define FOO 1
#if FOO == BAR
a
#endif
''')
        oh = StringIO()
        p.write(oh)
        if oh.getvalue() != output:
            print("Should be:\n" + output, file = sys.stderr)
            print("\n\nWas:\n" + oh.getvalue(), file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(oh.getvalue(), output)
        
