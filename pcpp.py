#!/usr/bin/python
# Python C99 conforming preprocessor useful for generating single include files for C and C++ libraries
# (C) 2017 Niall Douglas http://www.nedproductions.biz/
# Started: Feb 2017
#
# What's working:
# - line continuation operator \
# - C99 correct elimination of comments
# - __DATE__, __TIME__, __FILE__, __LINE__
# - #define macro replacement
#   - correctly expands recursively, but each macro only ever expanded once
#     as per C99 rules
# - #undef macro
# - #include "path", <path> and PATH
#   - include_not_found(system_include, curdir, includepath) handler
#     is called to find non-curdir headers, this includes any system headers
# - #error
# - #warning
# - #pragma (ignored)
# - #line no, no "file" and NUMBER FILE
#
#
# What remains to implement:
# - defined operator
# - Stringizing operator #
# - Token pasting operator ##
# - C operators:
#   - +, -, !, ~
#   - *, /, %
#   - +, -
#   - <<, >>
#   - <, <=, >, >=
#   - ==, !=
#   - &
#   - ^
#   - |
#   - &&
#   - ||
# - #if, #ifdef, #ifndef, #elif, #else, #endif
#   - will have a special mode to pass through preprocessor logic if any
#     inputs are undefined (instead of treating undefined macros as if 0)
# - #define macro(...) expr

from __future__ import print_function
import sys, os, re, datetime, traceback, time

preprocessor_command       = re.compile(r"\s*#\s*([a-z]+)\s*(.*)")
preprocessor_continuation  = re.compile(r"\s*#\s*([a-z]+)\s*(.*)\s*\\")
preprocessor_stringliteral = re.compile(r"(.*)\"(\\.|[^\"])*\"(.*)")
preprocessor_multicomment  = re.compile(r"(.*)/\*.*?\*/(.*)")
preprocessor_singlecomment = re.compile(r"(.*)//")
preprocessor_punctuator    = re.compile(r"[ \t\n\r\f\v{}\[\]#()]")
preprocessor_macro_name    = re.compile(r"([a-zA-Z_][a-zA-Z_0-9]*)")
preprocessor_macro_object  = re.compile(r"([a-zA-Z_][a-zA-Z_0-9]*)\s+(.+)")
preprocessor_macro_function= re.compile(r"([a-zA-Z_][a-zA-Z_0-9]*)\((.*)\)\s*(.*)")
preprocessor_include       = re.compile(r"[<\"](.+)[>\"]")
preprocessor_line          = re.compile(r"([0-9]+)")
preprocessor_line2         = re.compile(r"([0-9]+)\s+(.*)\s*(.*)")
def is_preprocessor_punctuator(c):
    """Returns true if a preprocessor delimiter"""
    result = preprocessor_punctuator.match(c)
    return result is not None

def tokenise_stringliterals(line):
    """Split string literals in line, literals always end up at odd indices in returned list"""
    out = []
    while 1:
        dq = line.find('"')
        sq = line.find("'")
        if dq == -1 and sq == -1:
            out.append(line)
            return out
        if dq != -1 and sq != -1:
            if dq < sq:
                sq = -1
            else:
                dq = -1
        if dq != -1:
            end = dq
            while 1:
                end = line.find('"', end+1)
                if end == -1:
                    end = len(line)
                    break
                if line[end-1]!='\\':
                    break
            out.append(line[:dq])
            out.append(line[dq:end+1])
            line = line[end+1:]
        if sq != -1:
            end = sq
            while 1:
                end = line.find("'", end+1)
                if end == -1:
                    end = len(line)
                    break
                if line[end-1]!='\\':
                    break
            out.append(line[:sq])
            out.append(line[sq:end+1])
            line = line[end+1:]

def expand_macros(contents, macros):
    """Recursively expands any macro objects and functions in contents, returning the expanded line"""
    parts = tokenise_stringliterals(contents)
    partidx = 0
    changed = False
    while partidx < len(parts):
        thispart = parts[partidx]
        # Do a quick search of the macro objects to expand first, if nothing early exit
        need_to_expand = False
        for macro in macros:
            if macro.name() in thispart:
                need_to_expand = True
                break
        if need_to_expand:
            changed = True
            macro_objects = macros[:]  # Sorted shortest to longest
            while 1:
                expanded = False
                # Search this part for macros to expand, expanding from end to start
                for midx in xrange(len(macro_objects)-1, -1, -1):
                    macro = macro_objects[midx]
                    macroname = macro.name()
                    macronamelen = len(macroname)
                    #print("Searching for macro", macro.name())
                    pls_remove = False
                    idx = len(thispart)
                    while idx != -1:
                        idx = thispart.rfind(macroname, 0, idx)
                        if idx != -1:
                            #print(idx, macronamelen, len(thispart), "'"+thispart+"'")
                            if idx == 0 or is_preprocessor_punctuator(thispart[idx-1]):
                                if idx+macronamelen == len(thispart) or is_preprocessor_punctuator(thispart[idx+macronamelen]):
                                    thispart = thispart[:idx] + macro.contents() + thispart[idx+macronamelen:]
                                    #print(thispart)
                            idx -= 1
                            pls_remove = True
                    if pls_remove:
                        parts[partidx] = thispart
                        del macro_objects[midx]  # Prevent being reexpanded again
                        expanded = True
                if not expanded:
                    break
        partidx += 2
    return ''.join(parts) if changed else contents

class MacroObject:
    """Token replacing macro"""
    def __init__(self, name, contents=''):
        self.name = lambda: name
        self.contents = lambda: contents
    def __repr__(self):
        return '#define '+self.name()+' '+self.contents()
    def __cmp__(self, other):
        return -1 if self.name()<other.name() else 0 if self.name()==other.name() else 1

class Line:
    def __init__(self, line, filepath, lineno):
        self.line = line.rstrip()
        self.filepath = filepath
        self.lineno = lineno

class Preprocessor(object):
    def include_not_found(self, system_include, curdir, includepath):
        """Handler called when a #include is not found from the current directory.
           Return None to have the include passed through into the output"""
        if self.__passthru_undefined:
            return None
        raise RuntimeError('#include "'+includepath+'" not found')
    
    def __file(self):
        if self.__fileoverride is not None:
            return self.__fileoverride
        return '"null"' if self.__currentline is None else '"'+self.__currentline.filepath+'"'
    def __line(self):
        return '0' if self.__currentline is None else str(self.__currentline.lineno + self.__lineoverride)
    def __date(self):
        return self.__datetime.strftime('"%b %d %Y"')
    def __time(self):
        return self.__datetime.strftime('"%H:%M:%S"')

    def __init__(self, passthru_undefined = False, quiet = False):
        self.__passthru_undefined = passthru_undefined
        self.__quiet = quiet
        self.__macro_objects = []  # List of MacroObject instances, sorted by length of name descending
        self.__lines = []          # List of Line instances each representing a line in a given file
        self.__currentline = None
        self.__fileoverride = None
        self.__lineoverride = 0
        self.__datetime = datetime.datetime.now()
        self.__cmds = {k[4:]:getattr(self, k) for k in dir(self) if k.startswith('cmd_')}

        self.return_code = 0

        # Set up the magic macro objects
        self.__macro_objects.append(MacroObject('__FILE__'))
        self.__macro_objects[-1].contents = self.__file
        self.__macro_objects.append(MacroObject('__LINE__'))
        self.__macro_objects[-1].contents = self.__line
        self.__macro_objects.append(MacroObject('__DATE__'))
        self.__macro_objects[-1].contents = self.__date
        self.__macro_objects.append(MacroObject('__TIME__'))
        self.__macro_objects[-1].contents = self.__time

    def cmd_define(self, contents):
        """As if #define contents"""
        need_sort = False
        # Is it a #define name(pars) object?
        result = preprocessor_macro_function.match(contents)
        if result is not None:
            return  # temporary
        # Is it a #define name object?
        result = preprocessor_macro_object.match(contents)
        if result is not None:
            try:
                self.__macro_objects[self.__macro_objects.index(MacroObject(result.group(1)))].contents = lambda: result.group(2)
            except ValueError:
                self.__macro_objects.append(MacroObject(result.group(1), result.group(2)))
                need_sort = True
        else:
            # Is it a #define name?
            result = preprocessor_macro_name.match(contents)
            if result is None:
                raise RuntimeError('cmd_define("'+contents+'") does not match a #define')
            try:
                self.__macro_objects[self.__macro_objects.index(MacroObject(result.group(1)))].contents = lambda: ''
            except ValueError:
                self.__macro_objects.append(MacroObject(result.group(1)))
                need_sort = True
        if need_sort:
            self.__macro_objects.sort(key=lambda x: len(x.name()))
        #print(self.__macro_objects)
        return not self.__passthru_undefined

    def cmd_error(self, contents):
        """As if #error contents"""
        if not self.__quiet:
            print(self.__currentline.filepath+":"+str(self.__currentline.lineno)+":: error: "+contents, file=sys.stderr)
        self.return_code += 1
        return not self.__passthru_undefined

    def cmd_include(self, contents):
        """As if #include contents, returns True if successfully included"""
        contents = expand_macros(contents, self.__macro_objects).lstrip().rstrip()
        self.__fileoverride = None
        self.__lineoverride = 0
        result = preprocessor_include.match(contents)
        if result is None:
            raise RuntimeError('cmd_include("'+contents+'") does not match a #include')
        else:
            newpath = result.group(1)
        curdir = os.path.dirname(self.__currentline.filepath)
        system_include = contents[0]=='<'
        if not system_include and newpath[0] != '/':
            newpath = os.path.join(curdir, newpath)
        if not os.path.exists(path):
            newpath = self.include_not_found(system_include, curdir, result.group(1))
        if newpath is not None:
            newpath = os.path.normpath(newpath).replace('\\', '/')
        if os.path.exists(newpath):
            with open(newpath, 'rt') as ih:
                self.add_raw_lines(ih.readlines(), newpath, self.__lines.index(self.__currentline)+1)
            return True
        return False

    def cmd_line(self, contents):
        """As if #line contents"""
        contents = expand_macros(contents, self.__macro_objects)
        result = preprocessor_line2.match(contents)
        if result is not None:
            self.__fileoverride = result.group(2)
        else:
            result = preprocessor_line.match(contents)
            if result is None:
                raise RuntimeError('cmd_line("'+contents+'") does not match a #line')
        self.__lineoverride = int(result.group(1)) - self.__currentline.lineno - 1
        return False  # always pass through

    def cmd_pragma(self, contents):
        """As if #pragma contents"""
        pass  # always pass through

    def cmd_undef(self, contents):
        """As if #undef contents"""
        result = preprocessor_macro_name.match(contents)
        if result is None:
            raise RuntimeError('cmd_undef("'+contents+'") does not match a #undef')
        try:
            self.__macro_objects.remove(MacroObject(result.group(1)))
        except ValueError:
            pass
        return not self.__passthru_undefined

    def cmd_warning(self, contents):
        """As if #warning contents"""
        if not self.__quiet:
            print(self.__currentline.filepath+":"+str(self.__currentline.lineno)+":: warning: "+contents, file=sys.stderr)
        return not self.__passthru_undefined



    def add_raw_lines(self, rawlines, path, index = -1):
        """Adds additional raw lines to the internal store identified using path.
           Line continuations are fused and comments eliminated at this stage
           leaving the internal store of lines ready for preprocessing."""
        lines = []
        for idx in xrange(0, len(rawlines)):
            lines.append(Line(rawlines[idx], path, idx + 1))
            
        # Merge any continued lines onto a single line
        for idx in xrange(0, len(lines)):
            while idx<len(lines)-1 and len(lines[idx].line) and lines[idx].line[-1]=='\\':
                lines[idx].line = lines[idx].line[:-1] + lines[idx + 1].line
                del lines[idx + 1]
                
        # Replace all comments with a space
        in_comment = None
        idx = 0
        while idx < len(lines):
            #print(lines[idx].lineno, lines[idx].line)
            parts = tokenise_stringliterals(lines[idx].line)
            #print(lines[idx].lineno)
            #for part in parts:
            #    print("   ", part)
            partidx = 0
            while partidx < len(parts):
                # Is this is a tokenised string part?
                if partidx % 2 == 1:
                    if in_comment is not None:
                        parts[partidx] = ''
                    partidx = partidx + 1
                    continue
                if in_comment is not None:
                    ce = parts[partidx].find('*/')
                    if ce != -1:
                        parts[partidx] = parts[partidx][ce+2:]
                        # Do I need to merge lines due to a multi line comment?
                        if in_comment < idx:
                            for n in xrange(in_comment, idx):
                                del lines[in_comment + 1]
                            idx = in_comment
                            # Insert the parts before the comment before me
                            parts.insert(0, '')
                            parts.insert(0, lines[idx].line)
                            partidx = partidx + 2
                        in_comment = None
                    else:
                        parts[partidx] = ''
                if in_comment is None:
                    while 1:
                        cb = parts[partidx].find('/*')
                        ce = parts[partidx].find('*/', cb) if cb != -1 else -1
                        if cb != -1 and ce != -1:
                            parts[partidx] = parts[partidx][:cb] + ' ' + parts[partidx][ce+2:]
                            continue
                        if ce == -1 and cb != -1:
                            parts[partidx] = parts[partidx][:cb] + ' '
                            in_comment = idx
                        cb = parts[partidx].find('//')
                        if cb != -1:
                            parts[partidx] = parts[partidx][:cb]
                            parts = parts[:partidx]
                        break
                partidx = partidx + 1
            #print(lines[idx].lineno, parts)
            lines[idx].line = ''.join(parts)
            idx = idx + 1
        if index == -1:
            self.__lines.extend(lines)
        else:
            self.__lines = self.__lines[:index] + lines + self.__lines[index:]

    def get_lines(self, lineno = True):
        """Returns internal store of lines ready for writing to output.
           lineno=True means emit #line directives to maintain link to
           original source files"""
        lines = []
        lastfilepath = None
        lastlineno = -1
        for line in self.__lines:
            if lineno:
                lastlineno += 1
                if line.filepath != lastfilepath or line.lineno != lastlineno:
                    lines.append('# %d "%s"\n' % (line.lineno, line.filepath))
                    lastlineno = line.lineno
                    lastfilepath = line.filepath
            lines.append(line.line+'\n')
        return lines
        
    def preprocess(self):
        """Executes preprocessing on the internal store of lines, expanding
           macros and calculations as execution proceeds"""
        lineidx = 0
        while lineidx < len(self.__lines):
            self.__currentline = self.__lines[lineidx]
            try:
                # Is this line a preprocessor command line?
                result = preprocessor_command.match(self.__currentline.line)
                if result is not None:
                    cmd = result.group(1)
                    if cmd in self.__cmds:
                        if self.__cmds[cmd](result.group(2)):
                            # Munch this line
                            del self.__lines[lineidx]
                            continue
                    else:
                        self.cmd_warning("#"+result.group(1)+" not understood by this implementation")
                else:
                    # Expand any macros in this line
                    self.__lines[lineidx].line = expand_macros(self.__lines[lineidx].line, self.__macro_objects)
            except Exception as e:
                self.cmd_error(traceback.format_exc())
            lineidx += 1
        self.__currentline = None
        #for macro in self.__macro_objects:
        #    print(macro)
                        

if __name__ == "__main__":
    #if len(sys.argv)<3:
    #    print("Usage: "+sys.argv[0]+" outputpath [-Iincludepath...] [-Dmacro...] header1 [header2...]", file=sys.stderr)
    #    sys.exit(1)
    start = time.time()
    path='test/test-c/n_std.c'
    p = Preprocessor(quiet=True)
    p.cmd_define('__STDC__ 1')
    p.cmd_define('__STDC_VERSION__ 199901L')
    with open(path, 'rt') as ih:
        p.add_raw_lines(ih.readlines(), path)
    p.preprocess()
    with open('test/n_std.i', 'w') as oh:
        oh.writelines(p.get_lines())
    end = time.time()
    print("Preprocessed", path, "in ", end-start, "seconds")
    sys.exit(p.return_code)
        
