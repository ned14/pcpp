# A C99 preprocessor written in pure Python

(C) 2017 Niall Douglas http://www.nedproductions.biz/

Very useful for preprocessing header only C++ libraries into single file includes
and other such malarky. There is a special mode to pass through preprocessor logic if any
inputs are undefined (instead of treating undefined macros as if 0).

Processing speed is pretty good. We use a mostly non-tokenising parser with a
zero copy fast path line processing if no processing is done for some line. This
makes preprocessing large numbers of lines with no macros being expanded in them
very low cost as they are basically passed through with no memory allocation done.

## What's working:
- line continuation operator \
- C99 correct elimination of comments
- `__DATE__`, `__TIME__`, `__FILE__`, `__LINE__`
- Object `#define`
  - correctly expands recursively, and each macro only ever expanded once
    as per C99 rules
- `#undef`
- `#include "path"`, `<path>` and `PATH`
  - Handler `include_not_found(system_include, curdir, includepath)`
    is called to find non-curdir headers, this includes any system headers
    which are NOT found automatically
- `#error`
- `#warning`
- `#pragma` (ignored)
- `#line num`, `num "file"` and `NUMBER FILE`
- `defined` operator
- C operators:
  - `+, -, !, ~`
  - `*, /, %`
  - `+, -`
  - `<<, >>`
  - `<, <=, >, >=`
  - `==, !=`
  - `&`
  - `^`
  - `|`
  - `&&`
  - `||`
  - `x ? y : z` (partial support, see known bugs)
- `#if`, `#ifdef`, `#ifndef`, `#elif`, `#else`, `#endif`

## What isn't working:
- Stringizing operator #
- Token pasting operator ##
- _Pragma operator
- Function `#define macro(...)`

## What won't be implemented:
- Trigraphs

## Known bugs:
- `#line` override tracks lines incorrectly when there are multiline comments.

  A hack workaround exists that if `#line` is used to reset to next line,
  we disable the override which restores correct line tracking and this
  bug appears to disappear :)

- Multiple whitespace are supposed to be collapsed into single whitespace
  throughout the file, including in non-macro parts.

  We don't do this outside modified lines because it causes a ton load more line modifications
  which slows down processing very significantly as we have a no-new-string
  fast path for when a line contains no macros. Being standards compliant
  here confers little benefit for a huge loss in performance.

- Expression evaluation is a bit broken (code donations of a proper lexing parser based on http://www.dabeaz.com/ply/ are welcome!)

  Currently `#if` expressions are evaluated by converting them into Python
  expressions and calling `eval()` on them. This works surprisingly well
  most of the time, but because Python is not C, weird corner cases break.
  These are the known such broken corner cases:
  - Unary operator evaluation will break for evil expressions such as `-!+!9`
  because logical NOT in Python results in a boolean, not an integer, and
  a unary plus or negative boolean is invalid syntax in Python
  - Python has no concept of an unsigned integer and C expressions relying
  on say unsigned integer overflow working will fail badly. To be honest
  if your preprocessor logic is relying on that anyway, you should rewrite it.
  For reference, unsigneds are mapped to long integers in Python, as are long longs.
  - Without a tokenising lexer, the C ternary operator is hard to accurately
  convert into a Python ternary operation, so you need to help it by using one
  of these two forms:
    - `(x) ? y : z` (z gets evaluated according to Python not C precedence)
    - `(x ? y : z)` (preferred, evaluates correctly)
