A C99 preprocessor written in pure Python
=========================================
.. role:: c(code)
   :language: c

\(C) 2017 Niall Douglas http://www.nedproductions.biz/ and (C) 2007-2017 David Beazley http://www.dabeaz.com/

PyPI: https://pypi.python.org/pypi/pcpp Github: https://github.com/ned14/pcpp

A pure Python v2 C preprocessor implementation very useful for preprocessing header only
C++ libraries into single file includes and other such build or packaging stage malarky.
The implementation can be used as a Python module or as a command line tool ``pcpp`` which
can stand in for a conventional C preprocessor (i.e. it'll accept similar arguments).
Extensive ability to hook and customise the preprocessing is provided, for example one
can pass through preprocessor logic if any inputs are undefined (instead of treating
undefined macros as if 0). This aids easy generation of low compile time single file
includes for some header only library.

``pcpp`` passes a modified edition of the `mcpp <http://mcpp.sourceforge.net/>`_ unit
test suite. Modifications done were to clarify ternary operators with extra brackets,
plus those testing the unusual special quirks in expression evaluation (see detailed
description below). It also passes the list of "preprocessor torture" expansion fragments
in the C11 standard, correctly expanding some very complex recursive macro expansions
where expansions cause new macro expansions to be formed. In this, it handily beats
the MSVC preprocessor and ought to handle most simple C99 preprocessor metaprogramming.
If you compare its output side-by-side to that of GCC or clang's preprocessor, results
are extremely close indeed with blank line collapsing being the only difference.

The most non-conforming part is :c:`#if` expression
parsing (donations of a proper yacc based parser for executing :c:`#if` expressions based on
http://www.dabeaz.com/ply/ are welcome). In practice, in most real world code, you
won't notice the departures and if you do, the application of extra brackets to
group subexpressions so Python's :c:`eval()` executes right will fix it.

A full, detailed list of known non-conformance with the C99 standard is below.

Note that most of this preprocessor was written originally by David Beazley to show
off his excellent Python Lex-Yacc library PLY (http://www.dabeaz.com/ply/) and is
hidden in there without being at all obvious given the number of Stackoverflow
questions which have asked for a pure Python C preprocessor implementation. This
implementation fixes a lot of conformance bugs (the original was never intended to
rigidly adhere to the C standard) and adds in a test suite based on the C11 preprocessor
torture samples plus the mcpp preprocessor test suite. Still, this project would
not be possible without David's work, so please take off your hat towards him.

What's working:
---------------
- Digraphs and Trigraphs
- line continuation operator '``\``'
- C99 correct elimination of comments and maintenance of whitespace in output.
- :c:`__DATE__`, :c:`__TIME__`, :c:`__FILE__`, :c:`__LINE__`. Note that :c:`__STDC__` et al are NOT defined by
  default, you need to define those manually before starting preprocessing.
- :c:`__COUNTER__`, a very common extension
- Object :c:`#define`
- Function :c:`#define macro(...)`

  - Retokenisation and reexpansion after expansion is C99 compliant.

- :c:`#undef`
- :c:`#include "path"`, :c:`<path>` and :c:`PATH`
- :c:`defined` operator
- C operators:

  - :c:`+, -, !, ~`
  - :c:`*, /, %`
  - :c:`+, -`
  - :c:`<<, >>`
  - :c:`<, <=, >, >=`
  - :c:`==, !=`
  - :c:`&`
  - :c:`^`
  - :c:`|`
  - :c:`&&`
  - :c:`||`
  - :c:`x ? y : z` (partial support, see known bugs)

- :c:`#if`, :c:`#ifdef`, :c:`#ifndef`, :c:`#elif`, :c:`#else`, :c:`#endif`
- Stringizing operator #
- Token pasting operator ##

Implementable by overriding :c:`PreprocessorHooks`:
---------------------------------------------------
- :c:`#error` (default implementation prints to stderr)
- :c:`#warning` (default implementation prints to stderr)
- :c:`#pragma` (ignored)
- :c:`#line num`, :c:`num "file"` and :c:`NUMBER FILE` (no default implementation, so ignored)

This is the default `PreprocessorHooks`, simply subclass `Preprocessor` to override with your own:

.. code-block:: python

    def on_error(self,file,line,msg):
        """Called when the preprocessor has encountered an error, e.g. malformed input.
        The default simply prints to stderr and increments the return code.
        """
        print >> sys.stderr, "%s:%d error: %s" % (file,line,msg)
        self.return_code += 1
        
    def on_include_not_found(self,is_system_include,curdir,includepath):
        """Called when a #include wasn't found. Return None to ignore, raise
        OutputDirective to pass through, else return a suitable path. Remember
        that Preprocessor.add_path() lets you add search paths."""
        self.on_error(self.lastdirective.source,self.lastdirective.lineno, "Include file '%s' not found" % includepath)
        
    def on_unknown_macro_in_expr(self,tok):
        """Called when an expression passed to an #if contained something unknown.
        Return what value it should be, raise OutputDirective to pass through,
        or None to pass through the mostly expanded #if expression apart from the
        unknown item."""
        tok.type = self.t_INTEGER
        tok.value = self.t_INTEGER_TYPE("0L")
        return tok
    
    def on_directive_handle(self,directive,toks):
        """Called when there is one of
        define, include, undef, ifdef, ifndef, if, elif, else, endif
        Return True to ignore, raise OutputDirective to pass through, else execute
        the directive"""
        self.lastdirective = directive
        
    def on_directive_unknown(self,directive,toks):
        """Called when the preprocessor encounters a #directive it doesn't understand.
        This is actually quite an extensive list as it currently only understands:
        define, include, undef, ifdef, ifndef, if, elif, else, endif
        
        The default handles #error and #warning here simply by printing to stderr
        and ignores everything else. You can raise OutputDirective to pass it through.
        """
        if directive.value == 'error':
            print >> sys.stderr, "%s:%d error: %s" % (directive.source,directive.lineno,''.join(tok.value for tok in toke))
            self.return_code += 1
        elif directive.value == 'warning':
            print >> sys.stderr, "%s:%d warning: %s" % (directive.source,directive.lineno,''.join(tok.value for tok in toks))


Known bugs (ordered from worst to least worst):
-----------------------------------------------
**Expression evaluation is a bit broken**
 Currently :c:`#if` expressions are evaluated by converting them into Python
 expressions and calling :c:`eval()` on them. This works surprisingly well
 most of the time, but because Python is not C, corner cases break.
 These are the known such broken corner cases:

 - Unary operator evaluation will break for evil expressions such as :c:`-!+!9`
   because logical NOT in Python results in a boolean, not an integer, and
   a unary plus or negative boolean is invalid syntax in Python
 - Similarly expressions which assume that boolean operations output either
   a zero or a one will fail e.g. :c:`(2 || 3) == 0`
 - Python has no concept of an unsigned integer and C expressions relying
   on unsigned integer semantics will fail badly e.g. :c:`-1 <= 0U`
   is supposed to be evaluated as false in the C preprocessor, but it will be
   evaluated as true under this implementation. To be honest
   if your preprocessor logic is relying on those sorts of behaviours, you should rewrite it.
   For reference, unsigneds are mapped to long (signed) integers in Python, as are long longs.
 - Without a back tracking parser, the C ternary operator is hard to accurately
   convert into a Python ternary operation, so you need to help it by using one
   of these two forms:

   - :c:`(x) ? y : z` (z gets evaluated according to Python not C precedence)
   - :c:`(x ? y : z)` (preferred, evaluates correctly, we inject brackets
     around the subexpessions before sending to Python)

 Code donations of a proper lexing parser based on http://www.dabeaz.com/ply/ are welcome!

**_Pragma used to emit preprocessor calculated #pragma is not implemented.**
 It would not be hard to add, it was simply a case of the author having no need of it.
 Patches adding support are welcome.
