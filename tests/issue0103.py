
import unittest, sys
from io import StringIO

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor
        p = Preprocessor()
        p.parse(self.input)        
        output = StringIO()
        p.write(output)
        if output.getvalue() != self.shouldbe:
            print("Should be:\n" + self.shouldbe + "EOF\n", file=sys.stderr)
            print("\nWas:\n" + output.getvalue() + "EOF\n", file=sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output.getvalue(), self.shouldbe)


class multiline_char_literals1(unittest.TestCase, runner):
    input = r'''#if 'N\
\
\
\
\
\
\
\
' == 78
FOO
#endif
'''
    shouldbe = r'''#line 10
FOO
'''

class multiline_char_literals2(unittest.TestCase, runner):
    input = r'''#if '\
\
\
\
\
\
\
\
N' == 78
FOO
#endif
'''
    shouldbe = r'''#line 10
FOO
'''

if __name__ == '__main__':
    unittest.main()