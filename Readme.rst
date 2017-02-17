A C99 preprocessor written in pure Python
=========================================
.. highlight:: c

(C) 2017 Niall Douglas http://www.nedproductions.biz/

Very useful for preprocessing header only C++ libraries into single file includes
and other such malarky. There is a special mode to pass through preprocessor logic if any
inputs are undefined (instead of treating undefined macros as if 0).

Processing speed is pretty good. We use a mostly non-tokenising parser for speed with a
zero copy fast path line processing if no processing is done for some line. This
makes preprocessing large numbers of lines with no macros being expanded in them
very low cost as they are basically passed through with no memory allocation done.

The non-tokenising parser is the main source of departures from the standard and
donations of a proper tokenising parser especially for executing ``#if`` expressions based on
http://www.dabeaz.com/ply/ are welcome. In practice, in most real world code, you
won't notice the departures and if you do, the application of extra brackets to
group subexpressions so Python's ``eval()`` executes right will fix it.

What's working:
---------------
- line continuation operator \
- C99 correct elimination of comments
- ``__DATE__``, ``__TIME__``, ``__FILE__``, ``__LINE__``
- Object ``#define``
- Function ``#define macro(...)``
  - correctly expands recursively, and each macro only ever expanded once
    as per C99 rules
- ``#undef``
- ``#include "path"``, ``<path>`` and ``PATH``
  - Handler ``include_not_found(system_include, curdir, includepath)``
    is called to find non-curdir headers, this includes any system headers
    which are NOT found automatically
- ``#error``
- ``#warning``
- ``#pragma`` (ignored)
- ``#line num``, ``num "file"`` and ``NUMBER FILE``
- ``defined`` operator
- C operators:
  - ``+, -, !, ~``
  - ``*, /, %``
  - ``+, -``
  - ``<<, >>``
  - ``<, <=, >, >=``
  - ``==, !=``
  - ``&``
  - ``^``
  - ``|``
  - ``&&``
  - ``||``
  - ``x ? y : z`` (partial support, see known bugs)
- ``#if``, ``#ifdef``, ``#ifndef``, ``#elif``, ``#else``, ``#endif``
- Stringizing operator #
- Token pasting operator ##

What won't be implemented:
--------------------------
- Digraphs and Trigraphs

Known bugs (ordered from worst to least worst):
-----------------------------------------------
- Function macro expansion order is wrong (it's being worked on right now)

- Expression evaluation is a bit broken (code donations of a proper lexing
  parser based on http://www.dabeaz.com/ply/ are welcome!)

  Currently ``#if`` expressions are evaluated by converting them into Python
  expressions and calling ``eval()`` on them. This works surprisingly well
  most of the time, but because Python is not C, corner cases break.
  These are the known such broken corner cases:
  - Unary operator evaluation will break for evil expressions such as ``-!+!9``
  because logical NOT in Python results in a boolean, not an integer, and
  a unary plus or negative boolean is invalid syntax in Python
  - Similarly expressions which assume that boolean operations output either
  a zero or a one will fail e.g. ``(2 || 3) == 0``
  - Python has no concept of an unsigned integer and C expressions relying
  on unsigned integer semantics will fail badly e.g. ``-1 <= 0U``
  is supposed to be evaluated as false in the C preprocessor, but it will be
  evaluated as true under this implementation. To be honest
  if your preprocessor logic is relying on those sorts of behaviours, you should rewrite it.
  For reference, unsigneds are mapped to long (signed) integers in Python, as are long longs.
  - Without a back tracking tokenising lexer, the C ternary operator is hard to accurately
  convert into a Python ternary operation, so you need to help it by using one
  of these two forms:
    - ``(x) ? y : z`` (z gets evaluated according to Python not C precedence)
    - ``(x ? y : z)`` (preferred, evaluates correctly, we inject brackets
    around the subexpessions before sending to Python)

- ``#line`` override isn't observed during empty line collapsing

  ``#line`` can be used to override ``__FILE__`` and ``__LINE__``, this works as per the
  standard. However long runs of empty lines are collapsed into an automatically
  emitted ``# lineno "file"`` during the final stage, and these do not observe any
  ``#line`` overrides, rather they always report the original file and line number.
  Fixing this would not be hard, patches adding support are welcome.

- Numbers are not tokenised any differently to strings

  It is rare you will notice this in real world code, but something like
  this shows the problem::

    #define EXP 1
    #define str(a) #a
    #define xstr(a) str(a)
    // FAILS, xE+y should not expand y as anything of the form xE+y should
    // be tokenised as a single number, even if invalid
    assert( strcmp( xstr( 12E+EXP), "12E+EXP") == 0);

  Patches adding support are welcome.

- ``_Pragma`` used to emit preprocessor calculated ``#pragma`` is not implemented.

  It would not be hard to add. Patches adding support are welcome.

- Multiple whitespace are supposed to be collapsed into single whitespace
  throughout the file, including in non-macro parts.

  We don't do this outside modified lines because it causes a ton load more line modifications
  which slows down processing very significantly as we have a no-new-string
  fast path for when a line contains no macros. Being standards compliant
  here confers little benefit for a huge loss in performance.

