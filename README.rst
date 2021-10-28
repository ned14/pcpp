A C99 preprocessor written in pure Python
=========================================
.. role:: c(code)
   :language: c

.. |travis| image:: https://github.com/ned14/pcpp/workflows/CI/badge.svg?branch=master
    :align: middle
    :target: https://github.com/ned14/pcpp/actions

\(C) 2018-2021 Niall Douglas http://www.nedproductions.biz/ and (C) 2007-2020 David Beazley http://www.dabeaz.com/

PyPI: https://pypi.python.org/pypi/pcpp Github: https://github.com/ned14/pcpp API reference docs: https://ned14.github.io/pcpp/

Travis master branch all tests passing for Python v2, v3 and PyPy v2, v3: |travis|

A pure universal Python C (pre-)preprocessor implementation very useful for pre-preprocessing header only
C++ libraries into single file includes and other such build or packaging stage malarky.
The implementation can be used as a Python module (`see API reference <https://ned14.github.io/pcpp/>`_)
or as a command line tool ``pcpp`` which
can stand in for a conventional C preprocessor (i.e. it'll accept similar arguments).
Works great under PyPy, and you can expect performance gains of between 0.84x and 2.62x
(average = 2.2x, median = 2.31x).

Your includes can be benchmarked for heft in order to improve your build times! See
the ``--times`` and ``--filetimes`` options, and you can see graphs from pcpp for the
C++ STLs at https://github.com/ned14/stl-header-heft.

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

**passthru-magic-macros**
  Don't expand ``__DATE__``, ``__TIME__``, ``__FILE__``, ``__LINE__`` nor ``__COUNTER__``.

**passthru-includes**
  Don't expand those ``#include`` whose arguments match the supplied regular expression
  into the output, however still execute those includes. This lets you generate output
  with macros from nested includes expanded, however those ``#include`` matching
  the regular expression are passed through into the output.


Standards (non-)compliance
--------------------------
``pcpp`` passes a very slightly modified edition of the `mcpp <http://mcpp.sourceforge.net/>`_
unit test suite. The only modifications done were to disable the digraph and trigraphs tests.
It also passes the list of "preprocessor torture" expansion fragments
in the C11 standard, correctly expanding some very complex recursive macro expansions
where expansions cause new macro expansions to be formed. In this, it handily beats
the MSVC preprocessor and ought to handle most C99 preprocessor metaprogramming.
If you compare its output side-by-side to that of GCC or clang's preprocessor, results
are extremely close indeed with blank line collapsing being the only difference.

As of v1.30 (Oct 2020), a proper yacc based expression evaluator for :c:`#if`
expressions is used which is standards conforming, and fixes a large number of
problems found in the previous Python :c:`eval()` based expression evaluator.

A full, detailed list of known non-conformance with the C99 standard is below.
Pull requests with bug fixes and new unit tests for the fix are welcome.

If you are on Python 2, files are parsed as strings, and unicode is not supported.
On Python 3, input and output files can have your choice of encoding, and you can
hook file open to inspect the encoding using ``chardet``.

Note that most of this preprocessor was written originally by David Beazley to show
off his excellent Python Lex-Yacc library PLY (http://www.dabeaz.com/ply/) and is
hidden in there without being at all obvious given the number of Stack Overflow
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
                [--passthru-magic-macros] [--passthru-includes <regex>]
                [--disable-auto-pragma-once] [--line-directive [form]] [--debug]
                [--time] [--filetimes [path]] [--compress]
                [--assume-input-encoding <encoding>]
                [--output-encoding <encoding>] [--write-bom] [--version]
                [input [input ...]]

    A pure universal Python C (pre-)preprocessor implementation very useful for
    pre-preprocessing header only C++ libraries into single file includes and
    other such build or packaging stage malarky.

    positional arguments:
      input                 Files to preprocess (use '-' for stdin)

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
      --passthru-magic-macros
                            Pass through double underscore magic macros unmodified
      --passthru-includes <regex>
                            Regular expression for which #includes to not expand.
                            #includes, if found, are always executed
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
      --assume-input-encoding <encoding>
                            The text encoding to assume inputs are in
      --output-encoding <encoding>
                            The text encoding to use when writing files
      --write-bom           Prefix any output with a Unicode BOM
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
false in ``pcpp``. However, it causes ``pcpp`` to execute the define of ``__cpp_constexpr`` to 190000:

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
- :c:`#pragma` anything other than :c:`once`.
- :c:`_Pragma` used to emit preprocessor calculated #pragma.
- :c:`#line num`, :c:`num "file"` and :c:`NUMBER FILE`.

Known bugs (ordered from worst to least worst):
-----------------------------------------------
None presently known.

Customising your own preprocessor:
==================================
See the API reference docs at https://ned14.github.io/pcpp/

You can find an example of overriding the ``on_*()`` processing hooks at https://github.com/ned14/pcpp/blob/master/pcpp/pcmd.py

History:
========
v1.30 (29th October 2021):
--------------------------
- Thanks to a 5km limit covid lockdown in my country, a public holiday where we were
  supposed to be away meant I was stuck at home instead. I took the full day to finish
  the https://github.com/ned14/pcpp/tree/yacc_expression_evaluator branch which is a
  proper C preprocessor expression evaluator based on http://www.dabeaz.com/ply/ 's
  yacc module. This was a very long outstanding piece of work which had been in
  progress for nearly two years. It just needed a full day of my time to get it done,
  and now it is indeed done at long last.
- BREAKING CHANGE: Thanks to the new expression evaluator, fix a long standing bug
  where unknown function macros in expressions were parsed as ``0(0)`` which obviously
  enough does not work. Fixing this changes how the ``on_unknown_macro_in_expr()``
  hook works, and there is now an added ``on_unknown_macro_function_in_expr()`` hook.
- Add a new passthru option ``--passthru-includes`` which enables selected ``#include``
  to be passed through, in addition to being executed. Thanks to schra for suggesting
  this, including a PR. The original implementation had some subtle corner case bugs,
  thanks to trelau for reporting those.
- Fix a token expansion ordering bug whereby if a function macro used the same
  macro in more than one argument, expansion in one argument evaluation caused overly
  eager expansion in later argument evaluations. This fix ought to fix pcpp's ability
  to parse Boost (untested). Thanks to joaquintides for reporting this.
- Now that pcpp no longer ever calls ``eval()``, pcpp is PyPy compatible and is
  probably also compatible with Pyston (untested). Typical speedup is about 2.2x-2.3x,
  though it can also be slower occasionally for some inputs. PyPy compatibility is now
  being tested by CI to ensure it remains working going forth.
- Fix internal preprocessor error and failure to insert newlines before ``#include``
  caused by certain sequence of line continuations in a macro. Thanks to dslijepcevic
  for reporting this.

v1.22 (19th October 2020):
--------------------------
- Fix bug where outputting to stdout did not combine with anything which
  printed to stdout. Thanks to Fondesa for reporting this.
- Fix extra newlines being inserted after a multiline comment. Thanks to virtuald
  for sending a PR fixing this.
- Fix not being able to actually specify an empty line directive. Thanks to kuri65536
  for sending a PR fixing this.
- Update ply submodule to latest from trunk.
- Emit line continuations as tokens, rather than collapsing lines during parsing.
  Thanks to MathieuDuponchelle for the pull request implementing this.
- Enable parsing and emission of files in arbitrary text encodings. This is supported
  in Python 3 or later only. Thanks to MathieuDuponchelle for the suggestion.
- Fix bad regex for parsing floats, so now floats are correctly tokenised. Thanks
  to LynnKirby for reporting this.
- BREAKING CHANGE: Passthrough for ``#include MACRO`` was not supported. This was not
  intentional, and to fix it required modifying the ``on_include_not_found()``
  customisation point which is a source breaking change. Thanks to schra for reporting this.

v1.21 (30th September 2019):
----------------------------
- Fix bug where token pasting two numeric tokens did not yield a numeric token. Thanks
  to Sei-Lisa for reporting this.
- BREAKING CHANGE: Paths emitted by pcpp into ``#line`` directives now are relative to the
  working directory of the process when ``Preprocessor`` is initialised. This includes
  added search paths - files included from those locations will be emitted with a sequence
  of ``../`` to relativise the path emitted. If no path exists between the working
  directory and the path of the file being emitted, an absolute path is emitted instead.

  If you wish to disable this new behaviour, or use different behaviour, you can
  customise the new `rewrite_paths` member variable of ``Preprocessor``.
- Fix bug where ``__LINE__`` was expanding into the line number of its definition instead
  of its use. Thanks to Sei-Lisa for reporting this.
- Add ``--passthru-magic-macros`` command line option.
- BREAKING CHANGE: The ``PreprocessorHooks`` and ``OutputDirective`` interface has
  changed. One now must specify the kind of ``OutputDirective`` abort one wants, and one
  can now both ignore AND remove directives. ``on_directive_handle()`` and
  ``on_directive_unknown()`` now take an extra parameter ``precedingtoks``, these are the
  tokens from the ``#`` up to the directive.
- Fix a corner case where ``FUNC(void)foo()`` expanded to ``voidfoo()`` and not
  ``void foo()`` which is a very common non-conforming extension of the C preprocessor.
  Thanks to OmegaDoom for reporting this.
- Add tokens for all the C operators, to help implementation of an expression evaluator.
- Updated embedded ply to HEAD (2019-04-25)
- Fix ``#include`` not working if no ``-I`` parameters were supplied. Thanks to csm10495
  for reporting this.

v1.20 (7th January 2019):
-------------------------
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
