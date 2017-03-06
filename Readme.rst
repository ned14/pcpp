A C99 preprocessor written in pure Python
=========================================
.. role:: c(code)
   :language: c

.. |travis| image:: https://travis-ci.org/ned14/pcpp.svg?branch=master
    :align: middle
    :target: https://travis-ci.org/ned14/pcpp

\(C) 2017 Niall Douglas http://www.nedproductions.biz/ and (C) 2007-2017 David Beazley http://www.dabeaz.com/

PyPI: https://pypi.python.org/pypi/pcpp Github: https://github.com/ned14/pcpp API reference docs: https://ned14.github.io/pcpp/

Travis master branch all tests passing for Python v2 and v3: |travis|

A pure universal Python C (pre-)preprocessor implementation very useful for pre-preprocessing header only
C++ libraries into single file includes and other such build or packaging stage malarky.
The implementation can be used as a Python module (`see API reference <https://ned14.github.io/pcpp/>`_)
or as a command line tool ``pcpp`` which
can stand in for a conventional C preprocessor (i.e. it'll accept similar arguments).
Extensive ability to hook and customise the preprocessing is provided, for example one
can pass through preprocessor logic if any macros are undefined (instead of treating
undefined macros as if 0). This aids easy generation of low compile time single file
includes for some header only library, thus making ``pcpp`` a "pre-pre-processor".

``pcpp`` passes a modified edition of the `mcpp <http://mcpp.sourceforge.net/>`_ unit
test suite. Modifications done were to clarify ternary operators with extra brackets,
plus those testing the unusual special quirks in expression evaluation (see detailed
description below). It also passes the list of "preprocessor torture" expansion fragments
in the C11 standard, correctly expanding some very complex recursive macro expansions
where expansions cause new macro expansions to be formed. In this, it handily beats
the MSVC preprocessor and ought to handle most C99 preprocessor metaprogramming.
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
not be possible without David's work, so please take off your hat and give a bow towards him.

Command line tool ``pcpp``:
---------------------------
The help from the command line tool ``pcpp``::

    usage: pcpp [-h] [-o [path]] [-D macro[=val]] [-U macro] [-I path]
                [--passthru] [--version]
                [input]

    A pure Python v2 C (pre-)preprocessor implementation very useful for pre-
    preprocessing header only C++ libraries into single file includes and other
    such build or packaging stage malarky.

    positional arguments:
      input           File to preprocess

    optional arguments:
      -h, --help      show this help message and exit
      -o [path]       Output to a file
      -D macro[=val]  Predefine name as a macro [with value]
      -U macro        Undefine name as a macro
      -I path         Path to search for unfound #include's
      --passthru      Undefined macros or unfound includes cause preprocessor
                      logic to be passed through instead of treated as 0L
      --version       show program's version number and exit

    Note that so pcpp can stand in for other preprocessor tooling, it ignores any
    arguments it does not understand and any files it cannot open.

Pass through mode passes through any #define's and #undef's plus any #if logic
where any macro in the expression is unknown. In this mode, -U macro means that
that macro is to be assumed to be undefined and expanding to `0L` i.e. don't
perform pass through on that macro because it is undefined.

Let us look at an example for pass through mode. Here is the original:

.. code-block:: c

    #if !defined(__cpp_constexpr)
    #if __cplusplus >= 201402L
    #define __cpp_constexpr 201304  // relaxed constexpr
    #else
    #define __cpp_constexpr 190000
    #endif
    #endif
    #ifndef BOOSTLITE_CONSTEXPR
    #if __cpp_constexpr >= 201304
    #define BOOSTLITE_CONSTEXPR constexpr
    #endif
    #endif
    #ifndef BOOSTLITE_CONSTEXPR
    #define BOOSTLITE_CONSTEXPR
    #endif

Pass through mode will output:

.. code-block:: c

    #if !defined(__cpp_constexpr)
    #if __cplusplus >= 201402
    #define __cpp_constexpr 201304
    #else
    #define __cpp_constexpr 190000
    #endif
    #endif
    #ifndef BOOSTLITE_CONSTEXPR
    
    
    
    #endif
    #ifndef BOOSTLITE_CONSTEXPR
    #define BOOSTLITE_CONSTEXPR
    #endif
    
This is because the ``#define __cpp_constexpr 190000`` was executed as
`__cpp_constexpr` was not defined and is less than `201402`. Let's see the effect
of `-U BOOSTLITE_CONSTEXPR`:

.. code-block:: c

    #if !defined(__cpp_constexpr)
    #if __cplusplus >= 201402
    #define __cpp_constexpr 201304
    #else
    #define __cpp_constexpr 190000
    #endif
    #endif
    
    
    
    
    
    
    #define BOOSTLITE_CONSTEXPR
    
Because `BOOSTLITE_CONSTEXPR` is no longer passed through, its #if is executed and
removed from the output. That leaves the ``#define BOOSTLITE_CONSTEXPR`` as the earlier
logic is also executed and removed due to being fully known to the preprocessor.
        
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

This is the default ``PreprocessorHooks``, simply subclass ``Preprocessor`` to override with
your own behaviours (`see API reference <https://ned14.github.io/pcpp/>`_). If you need an example, the command line tool overrides the hooks to provide
partial pre-preprocessing.

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

Customising your own preprocessor:
----------------------------------
See the API reference docs at https://ned14.github.io/pcpp/

You can find an example of overriding the `on_*()` processing hooks at https://github.com/ned14/pcpp/blob/master/pcpp/pcpp_cmd.py
