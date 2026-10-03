# Historical episode

Authoritative source: `PyCQA/pyflakes:507:repair:be8803601900`.

## Report

The [title](evidence/title.md) and [body](evidence/report.md) describe an unused-import false positive on `Foo` in:

```python
from datetime import datetime as Foo, time as Bar

def x(a: Foo, /, *, b: Bar):
    pass
```

The reporter used Pyflakes 2.1.1 on CPython 3.8.1/Linux, also through flake8 3.7.9. Both tools reported `datetime.datetime as Foo` imported but unused. The supplied output did not report `Bar` unused.

## Merged implementation

The [implementation evidence](evidence/implementation.md) records this addition in historical `pyflakes/checker.py`, inside the existing nonlegacy argument-processing branch:

```python
if PY38_PLUS:
    for arg in node.args.posonlyargs:
        args.append(arg.arg)
        annotations.append(arg.annotation)
```

It precedes the retained loop over `node.args.args + node.args.kwonlyargs`. The repair therefore collects both positional-only parameter names and annotations while leaving ordinary and keyword-only collection in place.

Current adaptations must locate the semantic collector and determine the supported-runtime policy; the historical path and `PY38_PLUS` identifier are not automatic current bindings.

## Committed regression assertion

The [regression evidence](evidence/regression.md) records an addition in historical `pyflakes/test/test_type_annotations.py`:

```python
@skipIf(version_info < (3, 8), 'new in Python 3.8')
def test_positional_only_argument_annotations(self):
    self.flakes("""
    from x import C

    def f(c: C, /): ...
    """)
```

The call supplies no expected diagnostic argument. It asserts no diagnostics for an import used only in a positional-only annotation. The evidence records an assertion available at the historical commit; it does not supply a historical execution log.

## Qualification and authoring limits

The later qualification, checked at `2026-10-03T19:13:23.292673+00:00`, reports verified resolution, one fail-to-pass case, and 24 pass-to-pass cases under `changed-test-files-with-original-base-control`. Its scope is changed test files only. Whole-project regression and cross-project transfer are untested.

The attestation is recorded separately in [provenance](provenance.json), not backdated to the repair. Conditional current probes, expanded adjacent checks, and task-context requirements are authored operational guidance, not additional verified historical events. Package functional evaluations remain unexecuted.
