from __future__ import absolute_import, print_function
import sys, argparse
from .pcpp import Preprocessor, OutputDirective

version='1.0'

__all__ = []

class CmdPreprocessor(Preprocessor):
    def __init__(self, argv):
        argp = argparse.ArgumentParser(prog='pcpp',
            description=
    '''A pure universal Python C (pre-)preprocessor implementation very useful for
    pre-preprocessing header only C++ libraries into single file includes and
    other such build or packaging stage malarky.''',
            epilog=
    '''Note that so pcpp can stand in for other preprocessor tooling, it
    ignores any arguments it does not understand and any files it cannot open.''')
        argp.add_argument('input', metavar = 'input', type = argparse.FileType('rt'), default=sys.stdin, nargs = '?', help = 'File to preprocess')
        #argp.add_argument('inputs', metavar = 'inputs', nargs = '*', action = 'append', help = 'More files to preprocess')
        argp.add_argument('-o', dest = 'output', metavar = 'path', type = argparse.FileType('wt'), default=sys.stdout, nargs = '?', help = 'Output to a file instead of stdout')
        argp.add_argument('-D', dest = 'defines', metavar = 'macro[=val]', nargs = 1, action = 'append', help = 'Predefine name as a macro [with value]')
        argp.add_argument('-U', dest = 'undefines', metavar = 'macro', nargs = 1, action = 'append', help = 'Pre-undefine name as a macro')
        argp.add_argument('-N', dest = 'nevers', metavar = 'macro', nargs = 1, action = 'append', help = 'Never define name as a macro, even if defined during the preprocessing.')
        argp.add_argument('-I', dest = 'includes', metavar = 'path', nargs = 1, action = 'append', help = "Path to search for unfound #include's")
        #argp.add_argument('--passthru', dest = 'passthru', action = 'store_true', help = 'Pass through everything unexecuted except for #include and include guards (which need to be the first thing in an include file')
        argp.add_argument('--passthru-defines', dest = 'passthru_defines', action = 'store_true', help = 'Pass through but still execute #defines and #undefs if not always removed by preprocessor logic')
        argp.add_argument('--passthru-unfound-includes', dest = 'passthru_unfound_includes', action = 'store_true', help = 'Pass through #includes not found without execution')
        argp.add_argument('--passthru-undefined-exprs', dest = 'passthru_undefined_exprs', action = 'store_true', help = 'Undefined macros in expressions cause preprocessor logic to be passed through instead of executed by treating undefined macros as 0L')
        argp.add_argument('--version', action='version', version='pcpp ' + version)
        args = argp.parse_known_args(argv[1:])
        #print(args)
        for arg in args[1]:
            print("NOTE: Argument %s not known, ignoring!" % arg, file = sys.stderr)

        self.args = args[0]
        super(CmdPreprocessor, self).__init__()
        self.define("__PCPP_VERSION__ " + version)
        self.define("__PCPP_ALWAYS_FALSE__ 0")
        self.define("__PCPP_ALWAYS_TRUE__ 1")
        self.debugout = open("pcpp_debug.log", "wt")
        self.bypass_ifpassthru = False

        if self.args.defines:
            self.args.defines = [x[0] for x in self.args.defines]
            for d in self.args.defines:
                d = d.replace('=', ' ')
                self.define(d)
        if self.args.undefines:
            self.args.undefines = [x[0] for x in self.args.undefines]
            for d in self.args.undefines:
                self.undef(d)
        if self.args.nevers:
            self.args.nevers = [x[0] for x in self.args.nevers]
        if self.args.includes:
            self.args.includes = [x[0] for x in self.args.includes]
            for d in self.args.includes:
                self.add_path(d)

        self.parse(self.args.input)
        self.write(self.args.output)
        
    def on_include_not_found(self,is_system_include,curdir,includepath):
        if self.args.passthru_unfound_includes:
            raise OutputDirective()
        return super(CmdPreprocessor, self).on_include_not_found(is_system_include,curdir,includepath)

    def on_unknown_macro_in_defined_expr(self,tok):
        if self.args.undefines:
            if tok.value in self.args.undefines:
                return False
        if self.args.passthru_undefined_exprs:
            return None  # Pass through as expanded as possible
        return super(CmdPreprocessor, self).on_unknown_macro_in_defined_expr(tok)
        
    def on_unknown_macro_in_expr(self,tok):
        if self.args.undefines:
            if tok.value in self.args.undefines:
                return super(CmdPreprocessor, self).on_unknown_macro_in_expr(tok)
        if self.args.passthru_undefined_exprs:
            return None  # Pass through as expanded as possible
        return super(CmdPreprocessor, self).on_unknown_macro_in_expr(tok)
        
    def on_directive_handle(self,directive,toks,ifpassthru):
        if ifpassthru:
            if directive.value == 'if' or directive.value == 'elif' or directive == 'else' or directive.value == 'endif':
                self.bypass_ifpassthru = len([tok for tok in toks if tok.value == '__PCPP_ALWAYS_FALSE__' or tok.value == '__PCPP_ALWAYS_TRUE__']) > 0
            if not self.bypass_ifpassthru and (directive.value == 'define' or directive.value == 'undef'):
                raise OutputDirective()  # Don't execute anything with effects when inside an #if expr with undefined macro
        if (directive.value == 'define' or directive.value == 'undef') and self.args.nevers:
            if toks[0].value in self.args.nevers:
                raise OutputDirective()
        if self.args.passthru_defines:
            super(CmdPreprocessor, self).on_directive_handle(directive,toks,ifpassthru)
            return None  # Pass through where possible
        return super(CmdPreprocessor, self).on_directive_handle(directive,toks,ifpassthru)

    def on_directive_unknown(self,directive,toks,ifpassthru):
        if ifpassthru:
            return None  # Pass through
        return super(CmdPreprocessor, self).on_directive_unknown(directive,toks,ifpassthru)


def main():
    p = CmdPreprocessor(sys.argv)
    sys.exit(p.return_code)
        
