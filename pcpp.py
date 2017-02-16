#!/usr/bin/python
# Python C99 conforming preprocessor useful for generating single include files for C and C++ libraries
# (C) 2017 Niall Douglas http://www.nedproductions.biz/
# Started: Feb 2017

from __future__ import print_function
import sys, os, re, datetime, traceback, time

debug = False

tailwhitespace             = re.compile(r".*(\s+)")
multiwhitespace            = re.compile(r"(\s\s+)")
nameerror_extract          = re.compile(r"name '(.*)' is not defined")
preprocessor_command       = re.compile(r"\s*#\s*([a-z]+)\s*(.*)")
preprocessor_continuation  = re.compile(r"\s*#\s*([a-z]+)\s*(.*)\s*\\")
preprocessor_stringliteral = re.compile(r"(.*)\"(\\.|[^\"])*\"(.*)")
preprocessor_multicomment  = re.compile(r"(.*)/\*.*?\*/(.*)")
preprocessor_singlecomment = re.compile(r"(.*)//")
preprocessor_punctuator    = re.compile(r"[ \t\n\r\f\v{}\[\]#()!+\-*/,;:]")
preprocessor_macro_name    = re.compile(r"([a-zA-Z_][a-zA-Z_0-9]*)")
preprocessor_macro_object  = re.compile(r"([a-zA-Z_][a-zA-Z_0-9]*)\s+(.+)")
preprocessor_macro_function= re.compile(r"([a-zA-Z_][a-zA-Z_0-9]*\([^)]*\))\s*(.*)")
preprocessor_include       = re.compile(r"[<\"](.+)[>\"]")
preprocessor_line          = re.compile(r"([0-9]+)")
preprocessor_line2         = re.compile(r"([0-9]+)\s+(.*)\s*(.*)")
preprocessor_defined       = re.compile(r"(defined\s*)\(*([^ \t\n\r\f\v)]+)\)*")
preprocessor_number_long   = re.compile(r"([0-9]+)(L|l)")
preprocessor_number_long_long = re.compile(r"([0-9]+)(LL|ll)")
preprocessor_number_unsigned_long_long = re.compile(r"([0-9]+)(ULL|ull)")
preprocessor_number_unsigned_long = re.compile(r"([0-9]+)(UL|ul)")
preprocessor_number_unsigned = re.compile(r"([0-9]+)(U|u)")
preprocessor_ternary1      = re.compile(r"(\(.+\)\s*)\?(.+):(.+)")
preprocessor_ternary2      = re.compile(r"\((.+)\?(.+):(.+)\)")
def is_preprocessor_punctuator(c):
    """Returns true if a preprocessor delimiter"""
    result = preprocessor_punctuator.match(c)
    return result is not None

class string_view(object):
    """A string like view onto some other string"""
    def __init__(self, s, start=0, end=-1):
        assert isinstance(s, str)
        if end == -1:
            end = len(s)
        self.__string = s
        self.__start = start
        self.__end = end
        if self.__start >= self.__end or self.__start >= len(s):
            self.__start = 0
            self.__end = 0

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
        return "'"+self.__string[self.__start:self.__end]+"'"
        
    def __str__(self):
        return self.__string[self.__start:self.__end]

    def __contains__(self, item):
        if isinstance(item, str):
            return -1 != self.__string.find(item, self.__start, self.__end)
        raise ValueError, "Cannot find type %s in a string_view" % repr(item)        
        
    def find(self, sub, start=0, end=-1):
        idx = self.__string.find(sub, self.__start + start, self.__end if end == -1 else self.__start + end)
        return idx - self.__start if idx != -1 else -1

    def rfind(self, sub, start=0, end=-1):
        idx = self.__string.rfind(sub, self.__start + start, self.__end if end == -1 else self.__start + end)
        return idx - self.__start if idx != -1 else -1

def tokenise_stringliterals(line, in_comment = False):
    """Split string literals in line, literals always end up at odd indices in returned list.
       NOTE we return string views of input line, NOT copies

    >>> tokenise_stringliterals('str( a)')
    ['str( a)']
    >>> tokenise_stringliterals('str( a,x)')
    ['str( a,x)']
    >>> tokenise_stringliterals('"niall" is here')
    ['', '"niall"', ' is here']
    >>> tokenise_stringliterals('"\\\\"niall\\\\"" is here')
    ['', '"\\"niall\\""', ' is here']
    """
    if isinstance(line, string_view):
        line_view = line
    else:
        line_view = string_view(line)
    out = []
    idx = 0
    idx2 = 0
    while 1:
        dq = line.find('"', idx)
        sq = line.find("'", idx)
        cs = 0 if in_comment and idx == 0 else line.find("/*", idx)
        if dq == -1 and sq == -1 and cs == -1:
            out.append(line_view[idx2:])
            return out
        if dq != -1 and sq != -1:
            if dq < sq:
                sq = -1
            else:
                dq = -1
        if cs != -1 and dq != -1:
            if cs < dq:
                dq = -1
            else:
                cs = -1
        if cs != -1 and sq != -1:
            if cs < sq:
                sq = -1
            else:
                cs = -1
        # Now exactly one of dq, sq or cs is not -1
        # If it's dq or sq, split the string literals into odd indices but
        # if it's a cs, skip idx to the end of the comment
        if cs != -1:
            end = line.find("*/", cs)
            if end == -1:
                end = len(line)
            idx = end+2
        elif dq != -1:
            end = dq
            while 1:
                end = line.find('"', end+1)
                if end == -1:
                    end = len(line)
                    break
                if line[end-1]!='\\':
                    break
            out.append(line_view[idx2:dq])
            out.append(line_view[dq:end+1])
            idx = idx2 = end+1
        elif sq != -1:
            end = sq
            while 1:
                end = line.find("'", end+1)
                if end == -1:
                    end = len(line)
                    break
                if line[end-1]!='\\':
                    break
            out.append(line_view[idx2:sq])
            out.append(line_view[sq:end+1])
            idx = idx2 = end+1

def tokenise_arguments(contents):
    """Converts a bracket and comma sequence into a list of string_views and chars consumed

    >>> tokenise_arguments('str( a)')
    ([' a'], 7)
    >>> tokenise_arguments('str( a,x)')
    ([' a', 'x'], 9)
    >>> tokenise_arguments('sub( ( a), ( b))')
    ([' ( a)', ' ( b)'], 16)
    """
    start = contents.find('(')
    parameters = []
    line_view = string_view(contents, start + 1)
    parts = tokenise_stringliterals(line_view)
    inbracket = 0
    lastcomma = 0
    idxbase = 0
    partidx = 0
    while partidx < len(parts):
        thispart = parts[partidx]
        idx = 0
        while idx < len(thispart) and inbracket >= 0:
            cb = thispart.find(',', idx) if inbracket == 0 else -1
            bb = thispart.find('(', idx)
            be = thispart.find(')', idx)
            #print(cb, bb, be, thispart)
            if cb == -1 and bb == -1 and be == -1:
                break
            if cb != -1 and bb != -1:
                if cb < bb:
                    bb = -1
                else:
                    cb = -1
            if be != -1 and bb != -1:
                if be < bb:
                    bb = -1
                else:
                    be = -1
            if be != -1 and cb != -1:
                if be < cb:
                    cb = -1
                else:
                    be = -1
            if bb != -1:
                inbracket += 1
                idx = bb + 1
            elif be != -1:
                inbracket -= 1
                idx = be + 1
            elif cb != -1:
                parameters.append(line_view[lastcomma:idxbase + cb])
                lastcomma = idxbase + cb + 1
                idx = cb + 1
        if inbracket < 0:
            parameters.append(line_view[lastcomma:idxbase + be])
            return (parameters, idxbase + be + start + 2)
        idxbase += len(thispart) + len(parts[partidx + 1]) if partidx < len(parts) - 1 else 0
        partidx += 2
    # No closing bracket
    parameters.append(line_view[lastcomma:])
    return (parameters, -1)

def remove_multiwhitespace(contents, preserve_indent = False):
    """Removes any instances of multiple whitespace"""
    indent = ''
    if preserve_indent:
        contents2 = contents.lstrip()
        indent = contents[:len(contents)-len(contents2)]
        contents = contents2
    while 1:
        result = multiwhitespace.search(contents)
        if result is None:
            return indent + contents
        contents = contents[:result.start(1)] + ' ' + contents[result.end(1):]

def stringize(contents):
    """Convert contents into a valid C string, escaped if necessary"""
    contents = str(contents).rstrip().lstrip().replace('\\', '\\\\')
    contents = contents.replace('"', '\\"')
    return contents

def expand_defineds(contents, macros_dict):
    """Expand all 'defined macro' operators, returning the expanded line"""
    parts = tokenise_stringliterals(contents)
    partidx = 0
    changed = False
    while partidx < len(parts):
        thispart = parts[partidx]
        idx = len(thispart)
        while 1:
            idx = thispart.rfind('defined', 0, idx)
            if idx == -1:
                break
            if idx == 0 or is_preprocessor_punctuator(thispart[idx-1]):
                if idx+7 == len(thispart) or is_preprocessor_punctuator(thispart[idx+7]):
                    if isinstance(thispart, string_view):
                        thispart = str(thispart)
                    result = preprocessor_defined.match(thispart[idx:])
                    assert result is not None
                    thispart = thispart[:idx + result.start(1)] + ('1' if result.group(2) in macros_dict else '0') + thispart[idx + result.end(0):]
                    changed = True
        parts[partidx] = thispart
        partidx += 2
    if not changed:
        return contents
    contents = ''
    for part in parts:
        contents += part
    return contents

class UnfinishedMacroExpansion(Exception):
    """Thrown by expand_macros() when during a macro expansion the expansion did not finish due to an
    unexpected end of line. The caller should append the next line and retry."""
    pass

def expand_macros(contents, macros, rounds = 2**30):
    """Recursively expands any macro objects and functions in contents, returning the expanded line"""
    macros_expanded = {}
    while rounds > 0:
        rounds -= 1
        changed = False
        # Break line into non-literals (even) and string literals (odd)
        parts = tokenise_stringliterals(contents)
        # Do a quick search of the macro objects to expand first, if nothing early exit
        need_to_expand = False
        for macro in macros:
            macroname = macro.name()
            if macroname not in macros_expanded:
                for partidx in xrange(0, len(parts), 2):
                    if macroname in parts[partidx]:
                        need_to_expand = True
                        break
        if not need_to_expand:
            break
        
        # We search longest macro names first down to shortest
        # FIXME: We actually need to figure out any nesting of function like macro
        # invocations, expanding the innermost function like macros WITHOUT expanding
        # their arguments. After expanding the innermost function like macros, rounds
        # of expansion are performed until no more expansion, only THEN do we move up
        # to the next highest function like macro. NOTE that the macros_expanded
        # dictionary must be kept only per top level expansion rather than global to
        # the entire line at present which is a BUG.
        #
        # You should split the object and function macros so we can fast path any
        # pure object like macro expansion which the code below is perfect at.
        for midx in xrange(len(macros)-1, -1, -1):
            macro = macros[midx]
            macroname = macro.name()
            if macroname in macros_expanded:
                continue
            macronamelen = len(macroname)
            pls_remove = False
            partidx = 0
            idxbase = 0
            # Iterate only the non string literal parts
            while partidx < len(parts):
                thispart = [ parts[partidx] ]  # odd indices are expanded macros
                expanded = False
                thispartidx = 0
                # Expand the current macro in the current non string literal, placing the expansions
                # at odd indices
                while thispartidx < len(thispart):
                    idx = 0
                    while idx != -1:
                        p = thispart[thispartidx]
                        idx = p.find(macroname, idx)
                        #print('"'+p+'" "'+macroname+'"', idx)
                        if idx != -1:
                            if idx == 0 or is_preprocessor_punctuator(p[idx-1]):
                                if idx+macronamelen == len(p) or is_preprocessor_punctuator(p[idx+macronamelen]):
                                    # Function macros without parameters must be ignored
                                    if macro.parameters is None or (idx+macronamelen < len(p) and p[idx+macronamelen] == '('):
                                        if macro.parameters is None:
                                            args = []
                                        else:
                                            # Figure out where in the original line we are currently at
                                            originalidx = idxbase
                                            for part in xrange(0, thispartidx):
                                                originalidx += len(thispart[part])
                                            originalidx += idx
                                            args, consumed = tokenise_arguments(contents[originalidx:])
                                            if consumed == -1:
                                                raise UnfinishedMacroExpansion()
                                            macronamelen = consumed
                                            #print('PARSED ARGS TO CALL', macroname,'=', args, 'from', contents[originalidx:])
                                        # Replace the macro with its expanded contents
                                        thispart[thispartidx] = p[idx+macronamelen:]
                                        thispart.insert(thispartidx, macro.contents(*args))
                                        thispart.insert(thispartidx, p[:idx])
                                        pls_remove = True
                                        expanded = True
                                        changed = True
                                        idx -= 1
                            idx += 1
                    thispartidx += 2
                if expanded:
                    # We expanded the current macro at least once, so rejoin the list of expansions
                    # Check for stringizing and tokenising operators
                    for n in xrange(1, len(thispart), 2):
                        # Was this expanded part preceded by a stringizing operator?
                        sidx = thispart[n - 1].rfind('#')
                        if sidx != -1:
                            temp = str(thispart[n - 1]).rstrip()
                            if temp[-1] == '#' and (len(temp) < 2 or temp[-2] != '#'):
                                thispart[n - 1] = temp[:-1]
                                thispart[n] = '"' + stringize(thispart[n]) + '"'
                    old = parts[partidx]
                    parts[partidx] = ''
                    for n in thispart:
                        parts[partidx] += n
                    parts[partidx] = remove_multiwhitespace(parts[partidx], partidx == 0)
                    if 1: #debug:
                        print("expand_macros", macroname, old, "=>", parts[partidx])
                idxbase += len(parts[partidx]) + (len(parts[partidx + 1]) if partidx < len(parts) -1 else 0)
                partidx += 2
            # Mark the current macro as having been expanded, and retokenise the modified
            # line as sting literals may have been inserted into it
            if pls_remove:
                macros_expanded[macroname] = None
                contents = ''
                for part in parts:
                    contents += part
                parts = tokenise_stringliterals(contents)
        if not changed:
            break
        # Having completed one full round of macro expansion, we now apply the tokenising operator
        if '##' in contents:
            changed = False
            for partidx in xrange(0, len(parts), 2):
                idx = 0
                while 1:
                    thispart = parts[partidx]
                    idx = thispart.find('##', idx)
                    if idx == -1:
                        break
                    parts[partidx] = str(thispart[:idx]).rstrip() + str(thispart[idx+2:]).lstrip()
                    changed = True
            if changed:
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

    #print(contents)        
    contents = contents.replace('!=', '<>')
    contents = contents.replace('!', ' not ')
    contents = contents.replace('||', ' or ')
    contents = contents.replace('&&', ' and ')
    
    # Python's integer literals are different to C's:
    # - L -> nothing
    # - LL -> L
    # - ULL -> L
    # - UL -> L
    # - U -> L
    def helper(contents, re, replace):
        while 1:
            result = re.search(contents)
            if result is None:
                break
            contents = contents[:result.start(2)] + replace + contents[result.end(2):]
        return contents
    contents = helper(contents, preprocessor_number_long, '')
    contents = helper(contents, preprocessor_number_long_long, 'L')
    contents = helper(contents, preprocessor_number_unsigned_long_long, 'L')
    contents = helper(contents, preprocessor_number_unsigned_long, 'L')
    contents = helper(contents, preprocessor_number_unsigned, 'L')

    # Try to handle the C ternary operator
    while 1:
        result = preprocessor_ternary1.search(contents)
        if result is None:
            break
        contents = contents[:result.start(1)] + '(' + result.group(2)+ ') if ' + result.group(1) + ' else ' + contents[result.start(3):]
    while 1:
        result = preprocessor_ternary2.search(contents)
        if result is None:
            break
        contents = contents[:result.start(1)] + '(' + result.group(2)+ ') if (' + result.group(1) + ') else (' + result.group(3) + ')' + contents[result.end(3):]
        
    vars = {}
    while 1:
        #print("=>", contents)
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
        name = str(name)
        #print('MacroObject(', name, '=', contents, ')')
        if name[-1] == ')':
            self.parameters = [ str(p).rstrip().lstrip() for p in tokenise_arguments(name)[0] ]
            self.variadic = False
            if len(self.parameters) > 0 and '...' in self.parameters[-1]:
                self.variadic = True
                del self.parameters[-1]
            name = name[:name.find('(')]
            self.name = lambda: name
            self.contents = self.__contents
            self.__rawcontents = contents
        else:
            self.name = lambda: name
            self.contents = lambda: contents
            self.parameters = None
            self.variadic = False
        if debug:
            print(repr(self))
    def __repr__(self):
        n = '#define '+self.name()
        if self.parameters:
            n += '('
            first = True
            for p in self.parameters:
                n += p if first else ', '+p
                first = False
            n += ') '+self.__rawcontents
        else:
            n += ' '+self.contents()
        return n
    def __cmp__(self, other):
        return -1 if self.name()<other.name() else 0 if self.name()==other.name() else 1
    def __hash__(self):
        return hash(self.name())
    def __contents(self, *args):
        if len(args) < len(self.parameters) or (not self.variadic and len(args) > len(self.parameters)):
            raise RuntimeError("Macro "+repr(self)+" called with %d arguments when it takes %d" % (len(args), len(self.parameters)))
        # Define a local macro list mapping the macro parameters to the args
        macros = [MacroObject(name, value) for name, value in zip(self.parameters, args)]
        if self.variadic:
            vaargs = ''
            if len(args) > len(self.parameters):
                vaargs = ','.join(args[len(args)-len(self.parameters):])
            macros.append(MacroObject('__VA_ARGS__', vaargs))
        #print('EXPAND FUNCTION MACRO', self.name(), '(', macros, ') args =', args)
        macros.sort(key=lambda x: len(x.name()))
        return expand_macros(self.__rawcontents, macros, rounds = 1)

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
        if self.__currentline.filepath in self.__lineoverrides:
            return self.__lineoverrides[self.__currentline.filepath][1]
        return '"null"' if self.__currentline is None else '"'+self.__currentline.filepath+'"'
    def __line(self):
        if self.__currentline.filepath in self.__lineoverrides:
            return str(self.__currentline.lineno + self.__lineoverrides[self.__currentline.filepath][0])
        return '0' if self.__currentline is None else str(self.__currentline.lineno)
    def __date(self):
        d = self.__datetime.strftime('"%b %d %Y"')
        if d[5] == '0':
            d = d[:5] + ' ' + d[6:]
        return d
    def __time(self):
        return self.__datetime.strftime('"%H:%M:%S"')

    def __init__(self, passthru_undefined = False, quiet = False):
        self.__passthru_undefined = passthru_undefined
        self.__quiet = quiet
        self.__macros_sorted = []  # List of MacroObject instances, sorted by length of name descending
        self.__macros_dict = {}    # Map of same MacroObject instances by macro name
        self.__lines = []          # List of Line instances each representing a line in a given file
        self.__currentline = None
        self.__lineoverrides = {}
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
            macroname = result.group(1)
            macrocontents = result.group(2)
        else:
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
        m = MacroObject(macroname, macrocontents)
        macroname = m.name()
        if macroname in self.__macros_dict:
            m2 = self.__macros_dict[macroname]
            #if m2.parameters != m.parameters or m2.contents() != m.contents():
            #    raise RuntimeError('Redefinition of macro ' + macroname)
        else:
            self.__macros_sorted.append(m)
            self.__macros_sorted.sort(key=lambda x: len(x.name()))
            self.__macros_dict[macroname] = m
        #print(self.__macros_sorted)
        return not self.__passthru_undefined

    def cmd_elif(self, contents):
        """As if #elif expr"""
        # If this if sequence is being evaluated and last stanza was false and no stanza has been executed yet
        if not self.__ifstack[-1][0] and not self.__ifstack[-1][1]:
            self.cmd_endif('')
            self.cmd_if(contents)
        return True
        
    def cmd_else(self, contents):
        """As if #else"""
        if not self.__ifstack[-1][0]:
            # If some previous #elif executed, disable now, else enable now
            if self.__ifstack[-1][1]:
                self.__isdisabled = True
            else:
                self.__isdisabled = False
        return True

    def cmd_endif(self, contents):
        """As if #endif"""
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
        if self.__isdisabled:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        contents = expand_defineds(contents, self.__macros_dict)
        contents = expand_macros(contents, self.__macros_sorted)
        try:
            result = evaluate_expr(contents, not self.__passthru_undefined)
        except:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            raise
        if result is None:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        willtake = result != 0
        self.__ifstack.append((self.__isdisabled, willtake, self.__currentline))
        self.__isdisabled = not willtake
        return True
        
    def cmd_ifdef(self, contents):
        """As if #ifdef macro"""
        if self.__isdisabled:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        willtake = contents in self.__macros_dict
        self.__ifstack.append((self.__isdisabled, willtake, self.__currentline))
        self.__isdisabled = not willtake
        return True
        
    def cmd_ifndef(self, contents):
        """As if #ifndef macro"""
        if self.__isdisabled:
            self.__ifstack.append((self.__isdisabled, False, self.__currentline))
            return
        willtake = contents not in self.__macros_dict
        self.__ifstack.append((self.__isdisabled, willtake, self.__currentline))
        self.__isdisabled = not willtake
        return True
        
    def cmd_include(self, contents):
        """As if #include contents, returns True if successfully included"""
        contents = expand_macros(contents, self.__macros_sorted).lstrip().rstrip()
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
        contents = expand_macros(contents, self.__macros_sorted)
        result = preprocessor_line2.match(contents)
        if result is not None:
            lineoverride = int(result.group(1))
            fileoverride = result.group(2)
        else:
            result = preprocessor_line.match(contents)
            if result is None:
                raise RuntimeError('cmd_line("'+contents+'") does not match a #line')
            lineoverride = int(result.group(1))
            fileoverride = self.__file()
        self.__lineoverrides[self.__currentline.filepath] = (lineoverride - self.__currentline.lineno - 1, fileoverride)
        # Rewrite current line to match calculated line
        self.__currentline.line = '# ' + str(int(self.__line())+1) + ' ' + self.__file()
        return False  # always pass through

    def cmd_pragma(self, contents):
        """As if #pragma contents"""
        pass  # always pass through

    def cmd_undef(self, contents):
        """As if #undef contents"""
        result = preprocessor_macro_name.match(contents)
        if result is None:
            raise RuntimeError('cmd_undef("'+contents+'") does not match a #undef')
        if result.group(1) in self.__macros_dict:
            self.__macros_sorted.remove(self.__macros_dict[result.group(1)])
            del self.__macros_dict[result.group(1)]
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
            parts = tokenise_stringliterals(lines[idx].line, in_comment)
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
                # FIXME: Multiple whitespace needs to be collapsed into a single space
                if in_comment is not None:
                    ce = parts[partidx].find('*/')
                    if ce != -1:
                        parts[partidx] = parts[partidx][ce+2:]
                        changed = True
                        # Do I need to merge lines due to a multi line comment?
                        if in_comment < idx:
                            # Insert the parts before the comment before me
                            parts.insert(0, '')
                            parts.insert(0, lines[in_comment].line)
                            partidx = partidx + 2
                            # Retain the line where the multiline comment began, but delete all
                            # intermediate lines include the current one
                            for n in xrange(in_comment, idx):
                                del lines[in_comment + 1]
                            idx = in_comment
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
                lines[idx].line = lines[idx].line.rstrip().lstrip()
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
                if line.filepath != lastfilepath or (line.lineno != lastlineno and len(line.line.rstrip().lstrip())):
                    if line.lineno - lastlineno < 5:
                        while lastlineno < line.lineno:
                            lines.append('\n')
                            lastlineno += 1
                    else:
                        lines.append('# %d "%s"\n' % (line.lineno, line.filepath))
                    lastlineno = line.lineno
                    lastfilepath = line.filepath
            lines.append(line.line + '\n')
        # Eliminate all empty lines before a # line directive
        idx = 1
        while idx < len(lines):
            if lines[idx][0] == '#' and lines[idx][2].isdigit():
                while lines[idx-1].rstrip() == '':
                    del lines[idx-1]
                    idx -= 1
            idx += 1
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
                    try:
                        self.time_executing.start()
                        cmd = result.group(1)
                        if self.__isdisabled:
                            if cmd in self.ifcmds:
                                try:
                                    self.time_cmds[cmd].start()
                                    if self.__cmds[cmd](result.group(2)):
                                        # Munch this line
                                        del self.__lines[lineidx]
                                        continue
                                finally:
                                    self.time_cmds[cmd].stop()
                        elif cmd in self.__cmds:
                            try:
                                self.time_cmds[cmd].start()
                                if self.__cmds[cmd](result.group(2)):
                                    # Munch this line
                                    del self.__lines[lineidx]
                                    continue
                            finally:
                                self.time_cmds[cmd].stop()
                        else:
                            self.cmd_warning("#"+result.group(1)+" not understood by this implementation")
                    finally:
                        self.time_executing.stop()
                elif not self.__isdisabled:
                    try:
                        self.time_expanding_macros.start()
                        while 1:
                            # Expand any macros in this line
                            try:
                                self.__lines[lineidx].line = expand_macros(self.__lines[lineidx].line, self.__macros_sorted)
                                break
                            except UnfinishedMacroExpansion:
                                # Append the next line and try again
                                self.__lines[lineidx].line += self.__lines[lineidx + 1].line
                                del self.__lines[lineidx + 1]
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
                        

if __name__ == "__main__":
    if 1:
        import doctest
        failurecount, testcount = doctest.testmod()
        if failurecount > 0:
            sys.exit(1)
    #if len(sys.argv)<3:
    #    print("Usage: "+sys.argv[0]+" outputpath [-Iincludepath...] [-Dmacro...] header1 [header2...]", file=sys.stderr)
    #    sys.exit(1)
    start = time.clock()
    path='test/test-c/n_std.c'
    p = Preprocessor(quiet=False)
    p.cmd_define('__STDC__ 1')
    p.cmd_define('__STDC_VERSION__ 199901L')
    p.cmd_define('NO_SYSTEM_HEADERS')
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
        
