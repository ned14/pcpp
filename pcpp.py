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
#   - correctly expands recursively, and each macro only ever expanded once
#     as per C99 rules
# - #undef macro
# - #include "path", <path> and PATH
#   - include_not_found(system_include, curdir, includepath) handler
#     is called to find non-curdir headers, this includes any system headers
# - #error
# - #warning
# - #pragma (ignored)
# - #line no, no "file" and NUMBER FILE
# - defined operator
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
#
#
# What remains to implement:
# - Stringizing operator #
# - Token pasting operator ##
# - #define macro(...) expr

from __future__ import print_function
import sys, os, re, datetime, traceback, time

tailwhitespace             = re.compile(r".*(\s+)")
nameerror_extract          = re.compile(r"name '(.*)' is not defined")
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
preprocessor_defined       = re.compile(r"(defined)[ \t\n\r\f\v(]*([^ )]+)")
def is_preprocessor_punctuator(c):
    """Returns true if a preprocessor delimiter"""
    result = preprocessor_punctuator.match(c)
    return result is not None

class string_view(object):
    """A string like view onto some other string"""
    def __init__(self, s, start=0, end=-1):
        self.__string = s
        self.__start = start
        self.__end = len(s) if end == -1 else end
        if self.__start >= self.__end or self.__start >= len(s):
            self.__start = 0
            self.__end = 0;

    def __len__(self):
        return self.__end - self.__start

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = key.start
            end = key.end
            start += self.__end if start < 0 else self.__start
            end += self.__end if end < 0 else self.__start
            return string_view(self.__string, start, end) if key.step == 1 else self.__string[start:end:step]
        elif isinstance(key, int):
            key += self.__end if key < 0 else self.__start
            return self.__string[key]
        else:
            raise TypeError, "Invalid key type"

    def __getslice__(self, start, end):
        if end == 2147483647:
            end = self.__end - self.__start
        start += self.__end if start < 0 else self.__start
        end += self.__end if end < 0 else self.__start
        return string_view(self.__string, start, end)

    def __add__(self, other):
        if isinstance(other, str) or isinstance(other, string_view):
            return str(self) + other
        raise ValueError, "Cannot add string_view to type %s" % repr(other)

    def __radd__(self, other):
        if isinstance(other, str) or isinstance(other, string_view):
            return other + str(self)
        raise ValueError, "Cannot add string_view to type %s" % repr(other)

    def __repr__(self):
        return self.__string[self.__start:self.__end]
        
    def __str__(self):
        return self.__string[self.__start:self.__end]

    def __contains__(self, item):
        if isinstance(item, str):
            return -1 != self.__string.find(item, self.__start, self.__end)
        raise ValueError, "Cannot find type %s in a string_view" % repr(other)        
        
    def find(self, sub, start=0, end=-1):
        return self.__string.find(sub, self.__start + start, self.__end if end == -1 else self.__start + end)

    def rfind(self, sub, start=0, end=-1):
        return self.__string.rfind(sub, self.__start + start, self.__end if end == -1 else self.__start + end)

def tokenise_stringliterals(line):
    """Split string literals in line, literals always end up at odd indices in returned list.
       NOTE we return string views of input line, NOT copies"""
    line_view = string_view(line)
    out = []
    idx = 0
    while 1:
        dq = line.find('"', idx)
        sq = line.find("'", idx)
        if dq == -1 and sq == -1:
            out.append(line_view[idx:])
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
                if line_view[end-1]!='\\':
                    break
            out.append(line_view[idx:dq])
            out.append(line_view[dq:end+1])
            idx = end+1
        if sq != -1:
            end = sq
            while 1:
                end = line.find("'", end+1)
                if end == -1:
                    end = len(line)
                    break
                if line_view[end-1]!='\\':
                    break
            out.append(line_view[idx:sq])
            out.append(line_view[sq:end+1])
            idx = end+1

def expand_macros(contents, macros, macros_dict, inside_macro):
    """Recursively expands any macro objects and functions in contents, returning the expanded line"""
    parts = tokenise_stringliterals(contents)
    partidx = 0
    changed = False
    while partidx < len(parts):
        thispart = parts[partidx]
        if inside_macro:
            # Expand any defined MACRO
            if 'defined' in thispart:
                thispart = str(thispart)
                changed = True
                while 1:
                    result = preprocessor_defined.search(thispart)
                    if result is None:
                        break
                    thispart = thispart[:result.start(1)] + thispart[result.end(1):result.start(2)] + ('1' if result.group(2) in macros_dict else '0') + thispart[result.end(2):]
                parts[partidx] = thispart
        # Do a quick search of the macro objects to expand first, if nothing early exit
        need_to_expand = False
        for macro in macros:
            if macro.name() in thispart:
                need_to_expand = True
                break
        if need_to_expand:
            changed = True
            macros_expanded = {}
            while 1:
                expanded = False
                # Search this part for macros to expand, expanding from end to start
                for midx in xrange(len(macros)-1, -1, -1):
                    macro = macros[midx]
                    macroname = macro.name()
                    if macroname in macros_expanded:
                        continue
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
                        macros_expanded[macroname] = None
                        expanded = True
                if not expanded:
                    break
        partidx += 2
    if not changed:
        return contents
    contents = ''
    for part in parts:
        contents += part
    return contents

def evaluate_expr(contents, undefined_means_zero):
    """Convert a C input expression into a Python one and evaluate it"""
    # First some early outs
    contents = contents.lstrip().rstrip()
    if contents == '0':
        return 0
    if contents == '1':
        return 1

    print(contents)        
    contents = contents.replace('!=', '<>')
    contents = contents.replace('!', ' not ')
    contents = contents.replace('||', ' or ')
    contents = contents.replace('&&', ' and ')
    vars = {}
    while 1:
        print("=>", contents)
        try:
            return int(eval(contents, vars, vars))
        except NameError as e:
            if not undefined_means_zero:
                return
            result = nameerror_extract.match(e.args[0])
            if result is None:
                raise
            vars[result.group(1)] = 0

class Timing(object):
    """Keeps timings"""
    def __init__(self):
        self.accumulated = 0.0
        self.calls = 0
        self.min = 1<<30
        self.max = 0
        self.lastclock = None
    def start(self):
        self.lastclock = time.clock()
    def stop(self):
        diff = time.clock() - self.lastclock
        self.accumulated += diff
        self.calls += 1
        if diff < self.min:
            self.min = diff
        if diff > self.max:
            self.max = diff
    def __repr__(self):
        if self.calls == 0:
            return "never executed"
        return "%f secs (%d calls, avrg %f/call, min %f, max %f)" \
                % (self.accumulated, self.calls, self.accumulated/self.calls, self.min, self.max)

class MacroObject(object):
    """Token replacing macro"""
    def __init__(self, name, contents=''):
        self.name = lambda: name
        self.contents = lambda: contents
    def __repr__(self):
        return '#define '+self.name()+' '+self.contents()
    def __cmp__(self, other):
        return -1 if self.name()<other.name() else 0 if self.name()==other.name() else 1
    def __hash__(self):
        return hash(self.name())

class Line(object):
    """A line from an original source file"""
    def __init__(self, line, filepath, lineno):
        result = tailwhitespace.match(line)
        if result is not None:
            self.line = line[:result.start(1)]
        else:
            self.line = line
        self.filepath = filepath
        self.lineno = lineno
        self.processedidx = None  # Set once this line has been executed

class Preprocessor(object):
    """Instantiate one of these to preprocess some text!"""
    systemmacros = [ '__FILE__', '__LINE__', '__DATE__', '__TIME__' ]
    ifcmds = [ 'if', 'ifdef', 'ifndef', 'else', 'elif', 'endif' ]
    
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
        self.__macros_sorted = []  # List of MacroObject instances, sorted by length of name descending
        self.__macros_dict = {}    # Map of same MacroObject instances by macro name
        self.__lines = []          # List of Line instances each representing a line in a given file
        self.__currentline = None
        self.__fileoverride = None
        self.__lineoverride = 0
        self.__datetime = datetime.datetime.now()
        self.__cmds = {k[4:]:getattr(self, k) for k in dir(self) if k.startswith('cmd_')}
        self.__ifstack = []
        self.__isdisabled = False

        self.time_cmds = {k[4:]:Timing() for k in dir(self) if k.startswith('cmd_')}
        self.time_reading_files = Timing()
        self.time_adding_raw_lines = Timing()
        self.time_executing = Timing()
        self.time_expanding_macros = Timing()
        self.return_code = 0

        # Set up the magic macro objects
        self.cmd_define('__FILE__ x')
        self.cmd_define('__LINE__ x')
        self.cmd_define('__DATE__ x')
        self.cmd_define('__TIME__ x')
        self.__macros_dict['__FILE__'].contents = self.__file
        self.__macros_dict['__LINE__'].contents = self.__line
        self.__macros_dict['__DATE__'].contents = self.__date
        self.__macros_dict['__TIME__'].contents = self.__time

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
            macroname = result.group(1)
            macrocontents = result.group(2)
        else:
            # Is it a #define name?
            result = preprocessor_macro_name.match(contents)
            if result is None:
                raise RuntimeError('cmd_define("'+contents+'") does not match a #define')
            macroname = result.group(1)
            macrocontents = ''
        if macroname in self.__macros_dict:
            if macroname not in self.systemmacros:
                self.__macros_dict[macroname].contents = lambda: macrocontents
        else:
            m = MacroObject(macroname, macrocontents)
            self.__macros_sorted.append(m)
            self.__macros_sorted.sort(key=lambda x: len(x.name()))
            self.__macros_dict[macroname] = m
        #print(self.__macros_sorted)
        return not self.__passthru_undefined

    def cmd_elif(self, contents):
        """As if #elif expr"""
        print("#elif", contents)
        # If this if sequence is being evaluated and last stanza was false and no stanza has been executed yet
        if not self.__ifstack[-1][0] and self.__is_disabled and not self.__ifstack[-1][1]:
            self.cmd_endif('')
            self.cmd_if(contents)
        
    def cmd_else(self, contents):
        """As if #else"""
        print("#else", contents)
        if not self.__ifstack[-1][0]:
            self.__isdisabled = not self.__isdisabled
        return True

    def cmd_endif(self, contents):
        """As if #endif"""
        print("#endif", contents)
        self.__isdisabled = self.__ifstack.pop()[0]
        return True

    def cmd_error(self, contents):
        """As if #error contents"""
        if not self.__quiet:
            print(self.__currentline.filepath+":"+str(self.__currentline.lineno)+":: error: "+contents, file=sys.stderr)
        self.return_code += 1
        return not self.__passthru_undefined

    def cmd_if(self, contents):
        """As if #if expr"""
        print("#if", contents)
        if self.__isdisabled:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        contents = expand_macros(contents, self.__macros_sorted, self.__macros_dict, True)
        result = evaluate_expr(contents,not self.__passthru_undefined)
        if result is None:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        self.__isdisabled = result == 0
        self.__ifstack.append((self.__isdisabled, not self.__isdisabled, self.__currentline))
        return True
        
    def cmd_ifdef(self, contents):
        """As if #ifdef macro"""
        print("#ifdef", contents)
        if self.__isdisabled:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        self.__isdisabled = contents not in self.__macros_dict
        self.__ifstack.append((self.__isdisabled, not self.__isdisabled, self.__currentline))
        return True
        
    def cmd_ifndef(self, contents):
        """As if #ifndef macro"""
        print("#ifndef", contents)
        if self.__isdisabled:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        self.__isdisabled = contents in self.__macros_dict
        self.__ifstack.append((self.__isdisabled, not self.__isdisabled, self.__currentline))
        return True
        
    def cmd_include(self, contents):
        """As if #include contents, returns True if successfully included"""
        contents = expand_macros(contents, self.__macros_sorted, self.__macros_dict, True).lstrip().rstrip()
        self.__fileoverride = None
        self.__lineoverride = 0
        result = preprocessor_include.match(contents)
        if result is None:
            newpath = contents
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
            self.time_reading_files.start()
            with open(newpath, 'rt') as ih:
                rawlines = ih.readlines()
                self.time_reading_files.stop()
                self.add_raw_lines(rawlines, newpath, self.__lines.index(self.__currentline)+1)
            return True
        return False

    def cmd_line(self, contents):
        """As if #line contents"""
        contents = expand_macros(contents, self.__macros_sorted, self.__macros_dict, True)
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
            self.__macros_sorted.remove(MacroObject(result.group(1)))
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
        self.time_adding_raw_lines.start()
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
            changed = False
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
                        changed = True
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
                            changed = True
                            continue
                        if ce == -1 and cb != -1:
                            parts[partidx] = parts[partidx][:cb] + ' '
                            changed = True
                            in_comment = idx
                        cb = parts[partidx].find('//')
                        if cb != -1:
                            parts[partidx] = parts[partidx][:cb]
                            parts = parts[:partidx]
                            changed = True
                        break
                partidx = partidx + 1
            if changed:
                #print(lines[idx].lineno, parts)
                lines[idx].line = ''
                for part in parts:
                    lines[idx].line += part
            idx = idx + 1
        if index == -1:
            self.__lines.extend(lines)
        else:
            self.__lines = self.__lines[:index] + lines + self.__lines[index:]
        self.time_adding_raw_lines.stop()

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
                    self.time_executing.start()
                    try:
                        cmd = result.group(1)
                        if self.__isdisabled:
                            if cmd not in self.ifcmds:
                                cmd = None
                        if cmd in self.__cmds:
                            self.time_cmds[cmd].start()
                            if self.__cmds[cmd](result.group(2)):
                                # Munch this line
                                del self.__lines[lineidx]
                                continue
                        else:
                            self.cmd_warning("#"+result.group(1)+" not understood by this implementation")
                    finally:
                        if cmd in self.time_cmds:
                            self.time_cmds[cmd].stop()
                        self.time_executing.stop()
                elif not self.__isdisabled:
                    try:
                        self.time_expanding_macros.start()
                        # Expand any macros in this line
                        self.__lines[lineidx].line = expand_macros(self.__lines[lineidx].line, self.__macros_sorted, self.__macros_dict, False)
                    finally:
                        self.time_expanding_macros.stop()
            except Exception as e:
                self.cmd_error(traceback.format_exc())
            if self.__isdisabled:
                del self.__lines[lineidx]
            else:
                self.__currentline.processedidx = lineidx
                lineidx += 1
        self.__currentline = None
        #for macro in self.__macros_sorted:
        #    print(macro)
                        

if __name__ == "__main__":
    #if len(sys.argv)<3:
    #    print("Usage: "+sys.argv[0]+" outputpath [-Iincludepath...] [-Dmacro...] header1 [header2...]", file=sys.stderr)
    #    sys.exit(1)
    start = time.clock()
    path='test/test-c/n_std.c'
    p = Preprocessor(quiet=False)
    p.cmd_define('__STDC__ 1')
    p.cmd_define('__STDC_VERSION__ 199901L')
    with open(path, 'rt') as ih:
        p.add_raw_lines(ih.readlines(), path)
    p.preprocess()
    with open('test/n_std.i', 'w') as oh:
        oh.writelines(p.get_lines())
    end = time.clock()
    print("Preprocessed", path, "in ", end-start, "seconds")
    print("  Opening and reading files took", p.time_reading_files)
    print("  Decommenting and adding raw lines took", p.time_adding_raw_lines)
    print("  Executing preprocessor commands took", p.time_executing)
    print("  Expanding macros in lines took", p.time_expanding_macros)
    print("\n  Individual commands:")
    for cmd, time in p.time_cmds.iteritems():
        print("    #"+cmd+":", time)
    sys.exit(p.return_code)
        
