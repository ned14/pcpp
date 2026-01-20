import unittest, sys, io, os

shouldbe1 = r'''#line 1 "tests/alternate_input_encodings1_ucs16le.c"
语言处理
'''

shouldbe2 = r'''#line 1 "tests/alternate_input_encodings1_ucs16le.c"
语言处理
#line 1 "tests/alternate_input_encodings2_ucs16le.c"
いろはにほへとちりぬるを
'''

class runner(object):
    def runTest(self):
        from pcpp import CmdPreprocessor
        if self.multiple:
            p = CmdPreprocessor(['pcpp', '-o', 'tests/alternate_input_encodings.c',
                                 '--assume-input-encoding', 'utf_16_le',
                                 '--output-encoding', 'utf_8',
                                 'tests/alternate_input_encodings1_ucs16le.c',
                                 'tests/alternate_input_encodings2_ucs16le.c'])
        else:
            p = CmdPreprocessor(['pcpp', '-o', 'tests/alternate_input_encodings.c',
                                 '--assume-input-encoding', 'utf_16_le',
                                 '--output-encoding', 'utf_8',
                                 'tests/alternate_input_encodings1_ucs16le.c'])
        with io.open('tests/alternate_input_encodings.c', 'rt', encoding='utf-8') as ih:
            output = ih.read()
        os.remove('tests/alternate_input_encodings.c')
        if output != self.shouldbe:
            print("Should be:\n" + repr(self.shouldbe) + "EOF\n", file = sys.stderr)
            print("\nWas:\n" + repr(output) + "EOF\n", file = sys.stderr)
        self.assertEqual(p.return_code, 0)
        self.assertEqual(output, self.shouldbe)

class single_input_file(unittest.TestCase, runner):
    multiple = False
    shouldbe = shouldbe1

class multiple_input_files(unittest.TestCase, runner):
    multiple = True
    shouldbe = shouldbe2
