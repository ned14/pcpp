from __future__ import absolute_import, print_function
import sys, argparse, traceback
from pcpp.preprocessor import Preprocessor, OutputDirective

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
        argp.add_argument('--passthru-unknown-exprs', dest = 'passthru_undefined_exprs', action = 'store_true', help = 'Unknown macros in expressions cause preprocessor logic to be passed through instead of executed by treating unknown macros as 0L')
        argp.add_argument('--passthru-comments', dest = 'passthru_comments', action = 'store_true', help = 'Pass through comments unmodified')
        argp.add_argument('--disable-auto-pragma-once', dest = 'auto_pragma_once_disabled', action = 'store_true', default = False, help = 'Disable the heuristics which auto apply #pragma once to #include files wholly wrapped in an obvious include guard macro')
        argp.add_argument('--line-directive', dest = 'line_directive', metavar = 'form', default = '#line', nargs = '?', help = "Form of line directive to use, defaults to #line, specify nothing to disable output of line directives")
        argp.add_argument('--debug', dest = 'debug', action = 'store_true', help = 'Generate a pcpp_debug.log file logging execution')
        argp.add_argument('--version', action='version', version='pcpp ' + version)
        args = argp.parse_known_args(argv[1:])
        #print(args)
        for arg in args[1]:
            print("NOTE: Argument %s not known, ignoring!" % arg, file = sys.stderr)

        self.args = args[0]
        super(CmdPreprocessor, self).__init__()
        
        # Override Preprocessor instance variables
        self.define("__PCPP_VERSION__ " + version)
        self.define("__PCPP_ALWAYS_FALSE__ 0")
        self.define("__PCPP_ALWAYS_TRUE__ 1")
        if self.args.debug:
            self.debugout = open("pcpp_debug.log", "wt")
        self.auto_pragma_once_enabled = not self.args.auto_pragma_once_disabled
        self.line_directive = self.args.line_directive
        
        # My own instance variables
        self.bypass_ifpassthru = False
        self.potential_include_guard = None

        if self.args.defines:
            self.args.defines = [x[0] for x in self.args.defines]
            for d in self.args.defines:
                if '=' not in d:
                    d += '=1'
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

        try:
            self.parse(self.args.input)
            self.write(self.args.output)
        except:
            print(traceback.print_exc(10), file = sys.stderr)
            print("\nINTERNAL PREPROCESSOR ERROR AT AROUND %s:%d, FATALLY EXITING NOW\n"
                % (self.lastdirective.source, self.lastdirective.lineno), file = sys.stderr)
            sys.exit(-99)
        
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
                if toks[0].value != self.potential_include_guard:
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

    def on_potential_include_guard(self,macro):
        self.potential_include_guard = macro
        return super(CmdPreprocessor, self).on_potential_include_guard(macro)

    def on_comment(self,tok):
        if self.args.passthru_comments:
            return
        return super(CmdPreprocessor, self).on_comment(tok)

def main():
    p = CmdPreprocessor(sys.argv)
    sys.exit(p.return_code)
        
if __name__ == "__main__":
    p = CmdPreprocessor(sys.argv)
    sys.exit(p.return_code)
