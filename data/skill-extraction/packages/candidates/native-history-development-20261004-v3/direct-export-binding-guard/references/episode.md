# Historical episode

Source `PyCQA/pyflakes:674` was resolved by PR 675 at revision
`1fae3dea5108a006d35da9e9ab785ca1ed1bc998`, available
2022-02-12T14:52:33Z.

## Report

With pyflakes 2.4.0, the reporter analyzed:

```python
__all__, = (
    "fizz",
    "buzz",
)
```

The historical command was `pyflakes foo.py`. The reported trace reached `source.value` and ended with:

```text
AttributeError: 'Tuple' object has no attribute 'value'
```

The reporter suggested an invalid-source diagnostic, but that suggestion was not the merged resolution. A later clarification said the spelling could be a typo discovered through flake8 and that the analyzer should not crash.

## Merged boundary

Historical implementation locator: `pyflakes/checker.py`.

The dispatcher previously selected `ExportBinding` from `name == '__all__'` and `ModuleScope`. The fix additionally required:

```python
isinstance(
    node._pyflakes_parent,
    (ast.Assign, ast.AugAssign, ast.AnnAssign),
)
```

The constructor call remained `ExportBinding(name, node._pyflakes_parent, self.scope)`. Earlier branches were retained.

Historical test locator: `pyflakes/test/test_imports.py`.

The added `TestSpecialAll.test_ignored_when_not_directly_assigned` asserted `m.UnusedImport` for:

```python
import bar
(__all__,) = ("foo",)
```

This supports ordinary unused-import analysis for indirect `__all__` binding, not a new invalid-assignment warning. No historical execution transcript was supplied; the test is an assertion available at the historical commit.

These paths are historical references, not automatic current bindings.

## Evidence index

- [Title](evidence/title.md)
- [Report and trace](evidence/body.md)
- [Maintainer question](evidence/question.md)
- [Reporter clarification](evidence/clarification.md)
- [Rename event](evidence/rename.md)
- [PR reference](evidence/pr-reference.md)
- [Implementation](evidence/fix.md)
- [Regression assertion](evidence/regression.md)

## Contemporary qualification

The separate attestation checked at 2026-10-03T17:33:12.467432+00:00 reports verified resolution, one fail-to-pass case, and 131 pass-to-pass cases. Its scope is changed test files with original-base control. Whole-project regression and cross-project transfer remain untested.

The attestation is retained in [provenance](provenance.json), not treated as pre-cutoff learned content or historical test execution.
