
import unittest, time
from io import StringIO
clock = time.process_time

class runner(object):
    def runTest(self):
        from pcpp import Preprocessor, OutputDirective, Action
        import os, sys

        class PassThruPreprocessor(Preprocessor):
            def on_directive_handle(self,directive,toks,ifpassthru,precedingtoks):
                if len(precedingtoks) == 1:
                    # Execute
                    return super(PassThruPreprocessor, self).on_directive_handle(directive,toks,ifpassthru,precedingtoks)
                raise OutputDirective(Action.IgnoreAndPassThrough)

        start = clock()
        p = PassThruPreprocessor()
        p.parse(self.input)
        oh = StringIO()
        p.write(oh)
        end = clock()
        print("Preprocessed test in", end-start, "seconds")
        if oh.getvalue() != self.output:
            print("Should be:\n" + self.output + "EOF\n", file = sys.stderr)
            print("\nWas:\n" + oh.getvalue()+"EOF\n", file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(oh.getvalue(), self.output)

            
class space_after_hash(unittest.TestCase, runner):
    input = r"""#if 5
1
#endif
# if 5
2
# endif
#warning Hi
# warning Hi2"""
    output = r"""
1

# if 5
2
# endif

# warning Hi2
"""
