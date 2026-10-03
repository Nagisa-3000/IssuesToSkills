# Historical episode

## Identity

- SourceRecord: `PyCQA/pyflakes:421:repair:2136e1e9f455`
- Repository: `PyCQA/pyflakes`
- Issue cluster: `PyCQA/pyflakes:421`
- Fix: `PyCQA/pyflakes:pr:452`
- Revision: `2136e1e9f4559930114c82ba316daada7d31836a`
- Repair evidence available: `2019-07-09T13:37:43Z`
- Catalog cutoff: `2024-01-01T00:00:00Z`

## Reported failure

The report identified Pyflakes 2.1.0 on Python 3.6.7/Linux. Its source imported `foo as _` and defined a function containing two `>>> x()` examples. The historical invocation was:

```console
PYFLAKES_DOCTEST=1 pyflakes t.py
```

The traceback passed through `handleDoctests`, which called `self.addBinding(None, Builtin('_'))`, then through `addBinding` and `getParent`, ending with:

```text
AttributeError: 'NoneType' object has no attribute 'parent'
```

This is a historical reproduction, not an executed current-checkout command. See [report](evidence/body.md) and [title](evidence/title.md).

## Repair

In the historical `pyflakes/checker.py`, doctest setup retained the module scope, pushed a `DoctestScope`, and changed unconditional synthetic initialization to:

```python
if '_' not in self.scopeStack[0]:
    self.addBinding(None, Builtin('_'))
```

The relevant owner is the doctest initializer. The repair avoided the collision by guarding initialization, rather than changing the general AST-parent helper. See [implementation](evidence/fix.md).

## Regression assertion

The historical `pyflakes/test/test_doctests.py` added `test_globalUnderscoreInDoctest`. It analyzed a module containing:

```python
from gettext import ugettext as _

def doctest_stuff():
    '''
        >>> pass
    '''
```

The assertion was `self.flakes(..., m.UnusedImport)`. It requires analysis to complete and report the imported `_` as unused. This is an assertion available at the historical commit, not evidence of historical test execution. See [regression](evidence/regression.md).

## Qualification boundary

A supplied attestation checked the changed test files against the original base on `2026-10-03T19:13:11.810728+00:00`. It reports verified resolution, one fail-to-pass case, and 229 pass-to-pass cases. It explicitly excludes whole-project regression and cross-project transfer.

The attestation is retained in provenance. Its post-cutoff timestamp is not backdated, and it does not create another historical evidence card or independent source.
