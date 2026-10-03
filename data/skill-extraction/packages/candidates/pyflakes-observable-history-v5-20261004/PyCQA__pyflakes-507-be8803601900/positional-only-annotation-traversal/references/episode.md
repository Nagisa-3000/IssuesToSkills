# Historical episode

SourceRecord: `PyCQA/pyflakes:507:repair:be8803601900`.

The report described Python 3.8.1 with Pyflakes 2.1.1 and Flake8 3.7.9. In a function with `a: Foo, /, *, b: Bar`, the analyzer reported the `Foo` import as unused. See [title](evidence/title.md) and [report](evidence/body.md).

The merged repair changed `pyflakes/checker.py`. In the existing non-legacy argument-collection branch, it added:

```python
if PY38_PLUS:
    for arg in node.args.posonlyargs:
        args.append(arg.arg)
        annotations.append(arg.annotation)
```

This preceded the existing loop over `node.args.args + node.args.kwonlyargs`. The implementation therefore collected positional-only names and their annotations while leaving the ordinary/keyword-only loop in place. See [implementation](evidence/fix.md).

The repair added `test_positional_only_argument_annotations` in `pyflakes/test/test_type_annotations.py`. It was skipped below Python 3.8 and called `self.flakes` on:

```python
from x import C

def f(c: C, /): ...
```

No expected diagnostic arguments were supplied. This is a historical regression assertion, not a supplied historical execution log. See [regression](evidence/regression.md).

The historical implementation and assertion support the repair mechanism. The inspection and validation instructions in the Action cards are reusable operations reconstructed from that evidence, not a claim that every listed operation was historically executed.

## Qualification boundary

A qualification attestation dated `2026-10-03T19:13:23.292673+00:00` reports verified resolution, one fail-to-pass case, and 24 pass-to-pass cases, using changed test files with original-base control. It explicitly leaves whole-project regression and cross-project transfer untested. It is retained in [provenance](provenance.json), separately from the pre-cutoff evidence.
