# Historical episode

- SourceRecord: `PyCQA/pyflakes:395:repair:066ba4a93c10`
- Repository: `PyCQA/pyflakes`
- Bug cluster: `PyCQA/pyflakes:395`
- Fix: `PyCQA/pyflakes:pr:396`
- Revision: `066ba4a93c1077f9154d6ff3806fe1e3a66843a1`

## Reported behavior

The [title](evidence/title.md) identifies a module-level undefined-name diagnostic. The [report](evidence/report.md) describes Python 3.7.1 and pyflakes 2.0.0 checking:

```python
a: int = 2
print(__annotations__)
```

The reported diagnostic was `t.py:3: undefined name '__annotations__'`. The report proposed the special-global registry as a repair location. That proposal is evidence about the historical episode, not an instruction to modify an uninspected current checkout.

## Merged implementation

The [implementation](evidence/implementation.md) changed historical `pyflakes/checker.py`:

- Replaced `PY34 = sys.version_info < (3, 5)` with `PY35_PLUS = sys.version_info >= (3, 5)`.
- Added `PY36_PLUS = sys.version_info >= (3, 6)`.
- Reversed the loop-type branch to use `PY35_PLUS`, keeping `ast.AsyncFor` on Python 3.5 and later and retaining synchronous types on older versions.
- Preserved `_MAGIC_GLOBALS = ['__file__', '__builtins__', 'WindowsError']`.
- Added `if PY36_PLUS: _MAGIC_GLOBALS.append('__annotations__')`.

This is a checker registry allowance, not proof that every runtime module initializes the name.

## Historical regression assertion

The [test diff](evidence/regression.md) added the following in historical `pyflakes/test/test_undefined_names.py`:

```python
@skipIf(version_info < (3, 6), 'new feature in 3.6')
def test_moduleAnnotations(self):
    """
    Use of the C{__annotations__} in module scope should not emit
    an undefined name warning when version is greater than or equal to 3.6.
    """
    self.flakes('__annotations__')
```

The added assertion checks a bare module-level reference, not only a module containing an annotation. The assertion was available at the historical commit; no historical test execution log is supplied.

## Qualification and reuse

The later supplied qualification reports one fail-to-pass and 61 pass-to-pass cases for changed test files with original-base control. Whole-project regression and cross-project transfer are untested. Its 2026 date remains in [provenance](provenance.json), separate from pre-cutoff evidence.

The [Workflow](workflow.md) reconstructs reusable operations from the report, implementation, and assertion. It does not claim that the historical author executed this exact inspection or validation sequence. Current owners, commands, and outcomes require independent public binding.
