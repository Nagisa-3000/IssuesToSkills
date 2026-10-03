# Historical episode

Authoritative repair source: `PyCQA/pyflakes:419:repair:ba64624f38a5`.

The [title](evidence/title.md) identifies an incorrect line number for a syntax error in a type comment. The [report](evidence/body.md) states that pyflakes 2.1.0 reported `'dummy value'` at line 196 of a Pillow test file, while the comment appeared at line 208. The reporter stated that version 2.0.0 did not report it.

## Implementation

At revision `ba64624f38a55f162b90120b4c0ba62018c6fd08`, historical `pyflakes/checker.py` introduced:

```python
class DummyNode(object):
    """Used in place of an `ast.AST` to set error message positions"""
    def __init__(self, lineno, col_offset):
        self.lineno = lineno
        self.col_offset = col_offset
```

The deferred `functools.partial` call to `handleStringAnnotation` changed from:

```python
part, node, lineno, col_offset,
messages.CommentAnnotationSyntaxError,
```

to:

```python
part, DummyNode(lineno, col_offset), lineno, col_offset,
messages.CommentAnnotationSyntaxError,
```

Thus the supplied [implementation diff](evidence/fix.md) changes the position-bearing argument while retaining the parsed part, explicit coordinates, and diagnostic class.

## Regression assertion

Historical `pyflakes/test/test_type_annotations.py` added `test_typeCommentsSyntaxErrorCorrectLine`. It called `self.flakes` with `x = 1` on line 1 and `# type: definitely not a PEP 484 comment` on line 2, requested `m.CommentAnnotationSyntaxError`, and asserted:

```python
self.assertEqual(checker.messages[0].lineno, 2)
```

The [regression diff](evidence/regression.md) also shows the neighboring `test_typeCommentsAssignedToPreviousNode`, whose comment describes association with a node above the type comment. The excerpt does not supply that test's full body.

These are implementation and assertion facts. Historical test execution is unknown from the supplied evidence.

## Later qualification

The attestation checked at `2026-10-03T19:13:09.449669+00:00` reports verified resolution under `changed-test-files-with-original-base-control`: one fail-to-pass and fourteen pass-to-pass cases. Its scope is changed test files only; whole-project regression and cross-project transfer are untested.

This post-cutoff attestation is retained in [provenance](provenance.json), not treated as a historical event available before the cutoff. It does not constitute execution of the package eval definitions.
