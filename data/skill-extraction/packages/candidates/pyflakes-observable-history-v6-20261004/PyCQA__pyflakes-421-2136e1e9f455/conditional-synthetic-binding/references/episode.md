# Historical episode

SourceRecord: `PyCQA/pyflakes:421:repair:2136e1e9f455`

The [title](evidence/title.md) and [report](evidence/body.md) describe Pyflakes 2.1.0 on Python 3.6.7 with doctest checking enabled. The public reproduction was:

```python
import foo as _

def x():
    """doc

    >>> x()
    >>> x()
    """
```

The reported historical command was:

```console
PYFLAKES_DOCTEST=1 pyflakes t.py
```

This is a historical shell command, not a current Oracle binding.

The traceback went from deferred doctest handling through `handleDoctests`, `addBinding`, and `getParent`, ending with `AttributeError: 'NoneType' object has no attribute 'parent'`. The reported insertion was `self.addBinding(None, Builtin('_'))`.

## Resolution

The [implementation evidence](evidence/fix.md) records a guard in historical `pyflakes/checker.py`. After retaining the module scope and pushing `DoctestScope`, the code changed from unconditional insertion to:

```python
if '_' not in self.scopeStack[0]:
    self.addBinding(None, Builtin('_'))
```

This prevents insertion of the source-less placeholder when the module scope already contains `_`. It does not change parent traversal generally.

The [regression evidence](evidence/regression.md) records `test_globalUnderscoreInDoctest` in historical `pyflakes/test/test_doctests.py`. It passes a module import `from gettext import ugettext as _` and a function doctest containing `>>> pass` to `self.flakes`, expecting `m.UnusedImport`.

This assertion checks both non-crashing analysis and retention of the ordinary unused-import diagnostic. The supplied historical evidence does not include a test-run log.

## Qualification boundary

The later supplied attestation is dated `2026-10-03T19:13:11.810728+00:00`. It reports verified resolution, one fail-to-pass case, and 229 pass-to-pass cases under `changed-test-files-with-original-base-control`. It explicitly excludes whole-project regression and cross-project transfer. It is recorded in provenance, not treated as an event before the `2024-01-01T00:00:00Z` cutoff.

The Workflow cards describe reusable, conditional operations reconstructed from this repair. They do not assert that a new checkout has been inspected, edited, or tested.
