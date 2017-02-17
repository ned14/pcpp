A C99 preprocessor written in pure Python
=========================================
.. role:: c(code)
   :language: c

\(C) 2017 Niall Douglas http://www.nedproductions.biz/

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
test suite. Modifications done were to clarify ternary operators with extra brackets
and to disable the digraph and trigraph tests, plus those testing the unusual special
quirks in expression evaluation (see detailed description below).

Processing speed is pretty good for Python and far in excess of a `Ply <http://www.dabeaz.com/ply/>`_
implementation, but this was achieved using a mostly
non-tokenising parser for speed with a zero copy fast path line processing if no
processing is done for some line. This makes preprocessing large numbers of lines
with no macros being expanded in them very low cost as they are basically passed
through with no memory allocation done. The sacrifice is that output from this
preprocessor is nonconforming in outputting more whitespace than is permitted because
we don't modify lines without comments or macros, and we are supposed to collapse all
whitespace in all lines. That said, side by side comparisons with the output from clang
or GCC's preprocessor are very comparable, and not at all like MSVC's preprocessor.

Other than excessive whitespace, the non-tokenising parser is the main source of
departures from the standard with the most non-conforming part being :c:`#if` expression
parsing (donations of a proper tokenising parser for executing :c:`#if` expressions based on
http://www.dabeaz.com/ply/ are welcome). In practice, in most real world code, you
won't notice the departures and if you do, the application of extra brackets to
group subexpressions so Python's :c:`eval()` executes right will fix it.

A full, detailed list of known non-conformance with the C99 standard is below.

What's working:
---------------
- line continuation operator '``\``'
- C99 correct elimination of comments
- :c:`__DATE__`, :c:`__TIME__`, :c:`__FILE__`, :c:`__LINE__` and the very common
  extension :c:`__COUNTER__`. Note that :c:`__STDC__` et al are NOT defined by
  default, you need to define those manually before starting preprocessing.
- Object :c:`#define`
- Function :c:`#define macro(...)`

  - correctly expands recursively, and each macro only ever expanded once
    as per C99 rules

- :c:`#undef`
- :c:`#include "path"`, :c:`<path>` and :c:`PATH`

  - Handler :c:`include_not_found(system_include, curdir, includepath)`
    is called to find non-curdir headers, this includes any system headers
    which are NOT found automatically

- :c:`#error`
- :c:`#warning`
- :c:`#pragma` (ignored)
- :c:`#line num`, :c:`num "file"` and :c:`NUMBER FILE`
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

What won't be implemented:
--------------------------
- Digraphs and Trigraphs

Known bugs (ordered from worst to least worst):
-----------------------------------------------
**Function macro expansion is wrong**
 This is tricky to get right, after all MSVC's preprocessor gets it wrong.
 I've disabled stringizing and token pasting temporarily, the current design is incapable
 of applying those operators across string literals. **Work to fix this is in progress**.

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
 - Without a back tracking tokenising lexer, the C ternary operator is hard to accurately
   convert into a Python ternary operation, so you need to help it by using one
   of these two forms:

   - :c:`(x) ? y : z` (z gets evaluated according to Python not C precedence)
   - :c:`(x ? y : z)` (preferred, evaluates correctly, we inject brackets
     around the subexpessions before sending to Python)

 Code donations of a proper lexing parser based on http://www.dabeaz.com/ply/ are welcome!

**#line override isn't observed during empty line collapsing**
 :c:`#line` can be used to override :c:`__FILE__` and :c:`__LINE__`, this works as per the
 standard. However long runs of empty lines are collapsed into an automatically
 emitted :c:`#line no "file"` during the final stage, and these do not observe any
 :c:`#line` overrides, rather they always report the original file and line number.

 Fixing this would not be hard, patches adding support are welcome.

**Numbers are not tokenised any differently to strings**
 It is rare you will notice this in real world code, but something like
 this shows the problem:

  .. code-block:: c

    #define EXP 1
    #define str(a) #a
    #define xstr(a) str(a)
    // FAILS, xE+y should not expand y as anything of the form xE+y should
    // be tokenised as a single number, even if invalid
    assert( strcmp( xstr( 12E+EXP), "12E+EXP") == 0);

 Patches adding support are welcome.

**_Pragma used to emit preprocessor calculated #pragma is not implemented.**
 It would not be hard to add, it was simply a case of the author having no need of it.
 Patches adding support are welcome.

**Multiple whitespace are supposed to be collapsed into single whitespace throughout the file, including in non-macro parts.**
 We don't do this outside macro or comment modified lines because it causes a ton load more line modifications
 which slows down processing very significantly as we have a no-new-string
 fast path for when a line contains no macros. Being standards compliant
 here confers little benefit for a huge loss in performance.
