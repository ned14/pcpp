import unittest
from io import StringIO
from unittest.mock import patch

from pcpp import CmdPreprocessor


class macro_option_order(unittest.TestCase):
    def preprocess(self, options, source='FOO\n'):
        output = StringIO()
        source_file = StringIO(source)
        source_file.name = '<stdin>'
        with patch('sys.stdin', source_file), patch('sys.stdout', output):
            preprocessor = CmdPreprocessor(
                ['pcpp', '--line-directive', 'none'] + options + ['-'])
        self.assertEqual(preprocessor.return_code, 0)
        return output.getvalue(), preprocessor.args

    def test_undefine_then_define(self):
        output, _ = self.preprocess(['-U', 'FOO', '-D', 'FOO=2'])
        self.assertEqual(output, '2\n')

    def test_redefine_after_undefine(self):
        output, args = self.preprocess(
            ['-D', 'FOO=1', '-U', 'FOO', '-D', 'FOO=2'])
        self.assertEqual(output, '2\n')
        self.assertEqual(args.defines, ['FOO=1', 'FOO=2'])
        self.assertEqual(args.undefines, ['FOO'])

    def test_attached_arguments(self):
        output, _ = self.preprocess(['-DFOO=1', '-UFOO', '-DFOO=2'])
        self.assertEqual(output, '2\n')

    def test_default_definition_after_undefine(self):
        output, _ = self.preprocess(['-UFOO', '-DFOO'])
        self.assertEqual(output, '1\n')

    def test_final_undefine(self):
        output, _ = self.preprocess(
            ['-DFOO=1', '-UFOO', '-DFOO=2', '-UFOO'])
        self.assertEqual(output, 'FOO\n')

    def test_multiple_macros(self):
        output, _ = self.preprocess(
            ['-DFOO=1', '-UBAR', '-DBAR=3', '-UFOO'], 'FOO BAR\n')
        self.assertEqual(output, 'FOO 3\n')

    def test_only_definitions(self):
        output, args = self.preprocess(['-DFOO=1', '-DFOO=2'])
        self.assertEqual(output, '2\n')
        self.assertIsNone(args.undefines)

    def test_only_undefinitions(self):
        output, args = self.preprocess(['-UFOO'])
        self.assertEqual(output, 'FOO\n')
        self.assertIsNone(args.defines)

    def test_no_macro_options(self):
        output, _ = self.preprocess(['--compress'])
        self.assertEqual(output, 'FOO\n')

    def test_equals_in_value(self):
        output, _ = self.preprocess(['-DFOO=1==1'])
        self.assertEqual(output, '1==1\n')


if __name__ == '__main__':
    unittest.main()
