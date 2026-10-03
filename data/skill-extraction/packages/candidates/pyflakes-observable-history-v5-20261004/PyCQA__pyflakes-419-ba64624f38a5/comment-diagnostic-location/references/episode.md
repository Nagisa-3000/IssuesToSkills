# Historical episode

## Report

Authoritative source: `PyCQA/pyflakes:419:repair:ba64624f38a5`.

The January 30, 2019 report concerned Pyflakes 2.1.0 on macOS High Sierra and Ubuntu Xenial. Its console reproduction reported `test_file_libtiff.py:196: syntax error in type comment 'dummy value'`; grep located the actual comment on line 208. The file was pinned to Pillow revision `a656a0bd603bcc333184ad1baf61d118925b3772`. The reporter stated Pyflakes 2.0.0 did not report the issue at all. These are supplied reporter observations, not executions performed while authoring this package.

## Merged implementation

At repair revision `ba64624f38a55f162b90120b4c0ba62018c6fd08`, historical `pyflakes/checker.py` gained:

```python
class DummyNode(object):
    """Used in place of an `ast.AST` to set error message positions"""
    def __init__(self, lineno, col_offset):
        self.lineno = lineno
        self.col_offset = col_offset
```

In the deferred `functools.partial` call to `handleStringAnnotation`, the diagnostic node argument changed from `node` to `DummyNode(lineno, col_offset)`. The call retained `part`, explicit `lineno` and `col_offset`, and `messages.CommentAnnotationSyntaxError`.

This separates the positional carrier used by diagnostics from the statement AST node associated with the comment. It does not establish a general fix for every parser location bug.

## Regression assertion

Historical `pyflakes/test/test_type_annotations.py` gained `test_typeCommentsSyntaxErrorCorrectLine`. Its fixture was:

```python
x = 1
# type: definitely not a PEP 484 comment
```

The test called `self.flakes` expecting `m.CommentAnnotationSyntaxError`, then asserted `checker.messages[0].lineno == 2`.

These assertions were present at the historical repair commit. No historical execution log is supplied. The excerpt shows the neighboring test name `test_typeCommentsAssignedToPreviousNode`, but does not supply its complete assertions.

## Resolution qualification

The authoritative source records a verified resolution. A later attestation checked at `2026-10-03T19:13:09.449669+00:00` reports one fail-to-pass and fourteen pass-to-pass cases, scoped to changed test files with original-base control.

That attestation is retained in provenance, not backdated into historical evidence. Whole-project regression and cross-project transfer are untested. This package's functional eval definitions are not executed.
