A C99 preprocessor written in pure Python
=========================================
.. role:: c(code)
   :language: c

.. |travis| image:: https://travis-ci.org/ned14/pcpp.svg?branch=master
    :align: middle
    :target: https://travis-ci.org/ned14/pcpp

\(C) 2018-2019 Niall Douglas http://www.nedproductions.biz/ and (C) 2007-2019 David Beazley http://www.dabeaz.com/

PyPI: https://pypi.python.org/pypi/pcpp Github: https://github.com/ned14/pcpp API reference docs: https://ned14.github.io/pcpp/

Travis master branch all tests passing for Python v2 and v3: |travis|

A pure universal Python C (pre-)preprocessor implementation very useful for pre-preprocessing header only
C++ libraries into single file includes and other such build or packaging stage malarky.
The implementation can be used as a Python module (`see API reference <https://ned14.github.io/pcpp/>`_)
or as a command line tool ``pcpp`` which
can stand in for a conventional C preprocessor (i.e. it'll accept similar arguments).

Your includes can be benchmarked for heft in order to improve your build times! See
the ``--times`` and ``--filetimes`` options.

A very unique facility of this C preprocessor is *partial* preprocessing so you can
programmatically control how much preprocessing is done by ``pcpp`` and how much is
done by the C or C++ compiler's preprocessor. The ultimate control is by subclassing
the :c:`Preprocessor` class in Python from which you can do anything you like, however
for your convenience the ``pcpp`` command line tool comes with the following canned
partial preprocessing algorithms:

**passthru-defines**
  Pass through but still execute #defines and #undefs if not always removed by
  preprocessor logic. This ensures that including the output sets exactly the same
  macros as if you included the original, plus include guards work.

**passthru-unfound-includes**
  If an :c:`#include` is not found, pass it through unmodified. This is very useful
  for passing through includes of system headers.

**passthru-undefined-exprs**
  This is one of the most powerful pass through algorithms. If an expression passed to
  :c:`#if` (or its brethern) contains an unknown macro, expand the expression with
  known macros and pass through *unexecuted*, and then pass through the remaining block.
  Each :c:`#elif` is evaluated in turn and if it does not contain unknown macros, it will be
  executed immediately. Finally, any :c:`#else` clause is always passed through *unexecuted*.
  Note that include guards normally defeat this algorithm, so those are specially detected and
  ignored.

**passthru-comments**
  A major use case for ``pcpp`` is as a preprocessor for the `doxygen <http://www.stack.nl/~dimitri/doxygen/>`_
  reference documentation tool whose preprocessor is unable to handle any preprocessing
  of any complexity. ``pcpp`` can partially execute the preprocessing which doxygen
  is incapable of, thus generating output which produces good results with doxygen.
  Hence the ability to pass through comments containing doxygen markup is very useful.

Standards (non-)compliance
--------------------------
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

A full, detailed list of known non-conformance with the C99 standard is below. We have
been told that ``pcpp`` does not pass the Boost.Wave preprocessor test suite, but
the chances of that biting most people is low. If it does, pull requests with bug
fixes and new unit tests for the fix are welcome.

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

    usage: pcpp [-h] [-o [path]] [-D macro[=val]] [-U macro] [-N macro] [-I path]
                [--passthru-defines] [--passthru-unfound-includes]
                [--passthru-unknown-exprs] [--passthru-comments]
                [--disable-auto-pragma-once] [--line-directive [form]] [--debug]
                [--time] [--filetimes [path]] [--version]
                [input [input ...]]

    A pure universal Python C (pre-)preprocessor implementation very useful for
    pre-preprocessing header only C++ libraries into single file includes and
    other such build or packaging stage malarky.

    positional arguments:
      input                 Files to preprocess

    optional arguments:
      -h, --help            show this help message and exit
      -o [path]             Output to a file instead of stdout
      -D macro[=val]        Predefine name as a macro [with value]
      -U macro              Pre-undefine name as a macro
      -N macro              Never define name as a macro, even if defined during
                            the preprocessing.
      -I path               Path to search for unfound #include's
      --passthru-defines    Pass through but still execute #defines and #undefs if
                            not always removed by preprocessor logic
      --passthru-unfound-includes
                            Pass through #includes not found without execution
      --passthru-unknown-exprs
                            Unknown macros in expressions cause preprocessor logic
                            to be passed through instead of executed by treating
                            unknown macros as 0L
      --passthru-comments   Pass through comments unmodified
      --disable-auto-pragma-once
                            Disable the heuristics which auto apply #pragma once
                            to #include files wholly wrapped in an obvious include
                            guard macro
      --line-directive [form]
                            Form of line directive to use, defaults to #line,
                            specify nothing to disable output of line directives
      --debug               Generate a pcpp_debug.log file logging execution
      --time                Print the time it took to #include each file
      --filetimes [path]    Write CSV file with time spent inside each included
                            file, inclusive and exclusive
      --compress            Make output as small as possible
      --version             show program's version number and exit

    Note that so pcpp can stand in for other preprocessor tooling, it ignores any
    arguments it does not understand.

Quick demo of pass through mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

``pcpp test.h --passthru-defines --passthru-unknown-exprs`` will output:

.. code-block:: c

    #if !defined(__cpp_constexpr)
    #if __cplusplus >= 201402
    #define __cpp_constexpr 201304
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
    
This is because ``__cpp_constexpr`` was not defined, so because of the ``--passthru-unknown-exprs`` flag
we pass through everything inside that if block **unexecuted** i.e. defines and undefs are NOT executed by
``pcpp``. Let's define ``__cpp_constexpr``:

``pcpp test.h --passthru-defines --passthru-unknown-exprs -D __cpp_constexpr``

.. code-block:: c

    #line 8 "test.h"
    #ifndef BOOSTLITE_CONSTEXPR



    #endif
    #ifndef BOOSTLITE_CONSTEXPR
    #define BOOSTLITE_CONSTEXPR
    #endif
    
So, big difference now. We execute the entire first if block as ``__cpp_constexpr`` is now defined, thus
leaving whitespace. Let's try setting ``__cpp_constexpr`` a bit higher:

``pcpp test.h --passthru-defines --passthru-unknown-exprs -D __cpp_constexpr=201304``

.. code-block:: c

    #line 8 "test.h"
    #ifndef BOOSTLITE_CONSTEXPR

    #define BOOSTLITE_CONSTEXPR constexpr

    #endif

As you can see, the lines related to the known ``__cpp_constexpr`` are executed and removed, passing through
any if blocks with unknown macros in the expression.

What if you want a macro to be known but undefined? The -U (to undefine) flag has an obvious meaning in pass
through mode in that it makes a macro no longer unknown, but known to be undefined.

``pcpp test.h --passthru-defines --passthru-unknown-exprs -U __cpp_constexpr``

.. code-block:: c

    #if __cplusplus >= 201402
    #define __cpp_constexpr 201304
    #else
    #define __cpp_constexpr 190000
    #endif
    
    #ifndef BOOSTLITE_CONSTEXPR
    
    
    
    #endif
    #ifndef BOOSTLITE_CONSTEXPR
    #define BOOSTLITE_CONSTEXPR
    #endif
    
Here ``__cpp_constexpr`` is known to be undefined so the first clause executes, but ``__cplusplus`` is
unknown so that entire block is passed through unexecuted. In the next test comparing ``__cpp_constexpr``
to 201304 it is still known to be undefined, and so 0 >= 201304 is the expressions tested which is false,
hence the following stanza is removed entirely.

Helping ``pcpp`` using source code annotation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can achieve a great deal using -D (define), -U (undefine) and -N (never define) on the command line,
but for more complex preprocessing it gets hard to pass through the correct logic without some source code
annotation.

``pcpp`` lets you annotate which part of an if block being passed through due to use of unknown macros
to also be executed in addition to the pass through. For this use ``__PCPP_ALWAYS_FALSE__`` or
``__PCPP_ALWAYS_TRUE__`` which tells ``pcpp`` to temporarily start executing the passed through
preprocessor commands e.g.

.. code-block:: c

    #if !defined(__cpp_constexpr)
    #if __cplusplus >= 201402L 
    #define __cpp_constexpr 201304
    #elif !__PCPP_ALWAYS_FALSE__     // pcpp please execute this next block
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

Note that ``__PCPP_ALWAYS_FALSE__`` will always be false in any other preprocessor, and it is also
false in ``pcpp``. However it causes ``pcpp`` to execute the define of ``__cpp_constexpr`` to 190000:

``pcpp test.h --passthru-defines --passthru-unknown-exprs``

.. code-block:: c

    #if !defined(__cpp_constexpr)
    #if __cplusplus >= 201402
    #define __cpp_constexpr 201304
    #elif 1
    #define __cpp_constexpr 190000
    #endif
    #endif
    #ifndef BOOSTLITE_CONSTEXPR



    #endif
    #ifndef BOOSTLITE_CONSTEXPR
    #define BOOSTLITE_CONSTEXPR
    #endif

This is one way of marking up ``#else`` clauses so they always execute in a normal preprocessor
and also pass through with execution with ``pcpp``. You can, of course, also place ``|| __PCPP_ALWAYS_FALSE__``
in any ``#if`` stanza to cause it to be passed through with execution, but not affect the
preprocessing logic otherwise.
        
What's implemented by the ``Preprocessor`` class:
=================================================
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
- :c:`#pragma once`, a very common extension

Additionally implemented by ``pcpp`` command line tool:
-------------------------------------------------------
- :c:`#error` (default implementation prints to stderr and increments the exit code)
- :c:`#warning` (default implementation prints to stderr)

Not implemented yet (donations of code welcome):
------------------------------------------------
- :c:`#pragma` anything other than once.
- :c:`_Pragma` used to emit preprocessor calculated #pragma.
- :c:`#line num`, :c:`num "file"` and :c:`NUMBER FILE`.

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

**We do not pass the Boost.Wave preprocessor test suite**
 A lot of bugs have been fixed since this was reported, however the chances are
 that ``pcpp`` still doesn't pass it. A TODO is to port the Wave test suite to
 Python and find out how bad things are. We suspect that any failures will be
 in highly estoric use cases i.e. known illegal input. If you only use valid
 input then we expect you generally won't have trouble.

Customising your own preprocessor:
==================================
See the API reference docs at https://ned14.github.io/pcpp/

You can find an example of overriding the ``on_*()`` processing hooks at https://github.com/ned14/pcpp/blob/master/pcpp/pcpp_cmd.py

History:
========
v1.20 (7th January 2019):
----------------------
- Now supports character literals in expressions. Thanks to untaugh for the pull request
  adding this.
- Stopped the default collapsing of whitespace in output, and made it optional via a
  new command line option ``--compress``.
- Fixed extraneous whitespace in ``--passthru-comments`` caused by multiline comments.
  Thanks to p2k for reporting this.
- Fixed bug where defining a macro via string did not set the source attribute in the
  token. Thanks to ZedThree for reporting this.
- Stop triggering an exception when no arguments are supplied to pcpp. Thanks to
  virtuald for reporting this.
- Rebase onto PLY latest from Dec 28th 2018 (https://github.com/dabeaz/ply/commit/a37e0839583d683d95e70ce1445c0063c7d4bd21). Latest
  PLY no longer works using pypi packaging, David wants people to include the source of
  PLY directly. pcpp does this via a git submodule, and has setuptools bundle the submodule.
- Add a formal LICENSE.txt file, as requested by Sei-Lisa.
- Fix failure to issue ``#line`` directive for first include file in a file. Thanks to
  Sei-Lisa for reporting this.

v1.1 (19th June 2018):
----------------------
- Added the ``--times`` and ``--filetimes`` features.
- Fix bug where macros containing operator `defined` were not being expanded properly.
- Added the ability to accept multiple inputs, they are concatenated into the output.
- Fix bug where lines beginning with `#` and no contents caused an internal preprocessor error.
- Fix bug where the macro expansion ``par par##ext`` was expanding into ``parext parext``.

v1.01 (21st Feb 2018):
----------------------
- Fix bug where in pass through mode, an #elif in an #if block inside an #if block in ifpassthru was failing to be passed through.
- Downgraded failure to evaluate an expression to a warning.
- Fix missing Readme.rst in pypi package.

v1.00 (13th Mar 2017):
----------------------
First release
