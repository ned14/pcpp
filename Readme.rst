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
test suite. Modifications done were to clarify ternary operators with extra brackets
and to disable the digraph and trigraph tests, plus those testing the unusual special
quirks in expression evaluation (see detailed description below).

The most non-conforming part is :c:`#if` expression
parsing (donations of a proper yacc based parser for executing :c:`#if` expressions based on
http://www.dabeaz.com/ply/ are welcome). In practice, in most real world code, you
won't notice the departures and if you do, the application of extra brackets to
group subexpressions so Python's :c:`eval()` executes right will fix it.

A full, detailed list of known non-conformance with the C99 standard is below.

What's working:
---------------
- Digraphs and Trigraphs
- line continuation operator '``\``'
- C99 correct elimination of comments
- :c:`__DATE__`, :c:`__TIME__`, :c:`__FILE__`, :c:`__LINE__`. Note that :c:`__STDC__` et al are NOT defined by
  default, you need to define those manually before starting preprocessing.
- Object :c:`#define`
- Function :c:`#define macro(...)`

  - currently retokenisation and reexpansion after expansion is not implemented

- :c:`#undef`
- :c:`#include "path"`, :c:`<path>` and :c:`PATH`

  - Handler :c:`include_not_found(system_include, curdir, includepath)`
    is called to find non-curdir headers, this includes any system headers
    which are NOT found automatically

- :c:`#error`
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

Still to implement:
-------------------
- :c:`__COUNTER__`
- :c:`#warning`
- :c:`#pragma` (ignored)
- :c:`#line num`, :c:`num "file"` and :c:`NUMBER FILE`

Known bugs (ordered from worst to least worst):
-----------------------------------------------
**Function macro expansion is wrong**
 This is tricky to get right, after all MSVC's preprocessor gets it wrong.
 **Work to fix this is in progress**.

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

**_Pragma used to emit preprocessor calculated #pragma is not implemented.**
 It would not be hard to add, it was simply a case of the author having no need of it.
 Patches adding support are welcome.
