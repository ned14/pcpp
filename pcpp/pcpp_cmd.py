from __future__ import absolute_import, print_function
import sys, argparse
from .pcpp import Preprocessor, OutputDirective

version='1.0'

class CmdPreprocessor(Preprocessor):
    def __init__(self, argv):
        argp = argparse.ArgumentParser(prog='pcpp',
            description=
    '''A pure Python v2 C (pre-)preprocessor implementation very useful for
    pre-preprocessing header only C++ libraries into single file includes and
    other such build or packaging stage malarky.''',
            epilog=
    '''Note that so pcpp can stand in for other preprocessor tooling, it
    ignores any arguments it does not understand and any files it cannot open.''')
        argp.add_argument('input', metavar = 'input', type = argparse.FileType('rt'), default=sys.stdin, nargs = '?', help = 'File to preprocess')
        #argp.add_argument('inputs', metavar = 'inputs', nargs = '*', action = 'append', help = 'More files to preprocess')
        argp.add_argument('-o', dest = 'output', metavar = 'path', type = argparse.FileType('wt'), default=sys.stdout, nargs = '?', help = 'Output to a file')
        argp.add_argument('-D', dest = 'defines', metavar = 'macro[=val]', nargs = 1, action = 'append', help = 'Predefine name as a macro [with value]')
        argp.add_argument('-U', dest = 'undefines', metavar = 'macro', nargs = 1, action = 'append', help = 'Undefine name as a macro')
        argp.add_argument('-I', dest = 'includes', metavar = 'path', nargs = 1, action = 'append', help = "Path to search for unfound #include's")
        #argp.add_argument('--neverdefine', dest = 'neverdefines', metavar = 'macro', nargs = 1, action = 'append', help = 'Never define name as a macro, even if defined in the preprocessing.')
        argp.add_argument('--passthru', dest = 'passthru', action = 'store_true', help = 'Undefined macros or unfound includes cause preprocessor logic to be passed through instead of treated as 0L')
        argp.add_argument('--version', action='version', version='pcpp ' + version)
        args = argp.parse_known_args(argv[1:])
        #print(args)
        for arg in args[1]:
            print("NOTE: Argument %s not known, ignoring!" % arg, file = sys.stderr)

        self.args = args[0]
        super(CmdPreprocessor, self).__init__()
        self.debugout = open("pcpp_debug.log", "wt")

        if self.args.defines:
            for d in self.args.defines:
                d = d[0].replace('=', ' ')
                self.define(d)
        if self.args.undefines:
            for d in self.args.undefines:
                self.undef(d[0])
        if self.args.includes:
            for d in self.args.includes:
                self.add_path(d[0])

        self.parse(self.args.input)
        self.write(self.args.output)
        
    def on_include_not_found(self,is_system_include,curdir,includepath):
        if self.args.passthru:
            raise OutputDirective()
        super(CmdPreprocessor, self).on_include_not_found(is_system_include,curdir,includepath)
        raise OutputDirective()

    def on_unknown_macro_in_expr(self,tok):
        if self.args.passthru:
            return None  # Pass through as expanded as possible
        return super(CmdPreprocessor, self).on_unknown_macro_in_expr(tok)
        
    def on_directive_handle(self,directive,toks,ifpassthru):
#        if ifpassthru:
#            if directive.value == 'error' or directive.value == 'warning':
#                raise OutputDirective()
        return super(CmdPreprocessor, self).on_directive_handle(directive,toks,ifpassthru)

    def on_directive_unknown(self,directive,toks,ifpassthru):
        if not ifpassthru:
            if directive.value == 'error' or directive.value == 'warning':
                return super(CmdPreprocessor, self).on_directive_unknown(directive,toks,ifpassthru)
        if self.args.passthru:
            raise OutputDirective()        


def main():
    p = CmdPreprocessor(sys.argv)
    sys.exit(p.return_code)
        
