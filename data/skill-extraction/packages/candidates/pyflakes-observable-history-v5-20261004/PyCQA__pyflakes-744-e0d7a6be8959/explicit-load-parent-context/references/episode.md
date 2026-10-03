# Historical episode

Source: `PyCQA/pyflakes:744:repair:e0d7a6be8959`.

The report described an internal analyzer exception under Python 3.10 with pyflakes 3.0.0 and flake8 6.0.0 when checking:

```python
print *= -1
```

The traceback passed through `AUGASSIGN`, `handleNodeLoad`, and `getParent`, ending with:

```text
AttributeError: 'Name' object has no attribute '_pyflakes_parent'
```

The merged implementation changed `handleNodeLoad(self, node)` to `handleNodeLoad(self, node, parent)`. It removed the internal `getParent(node)` call from the builtin-`print` check. Ordinary `NAME` loads supplied `self.getParent(node)`; `AUGASSIGN` supplied its own statement node. The augmented-assignment order remained load target, visit value, then visit target.

The regression added `test_print_augmented_assign` to `TestIncompatiblePrintOperator`, with `self.flakes('print += 1')` and the comment “nonsense, but shouldn't crash pyflakes.” The supplied diff does not show historical test execution.

Historical file locations were `pyflakes/checker.py` and `pyflakes/test/test_other.py`. They are historical locators, not automatic bindings to a current checkout.

Evidence:
- [Title](evidence/title.md)
- [Report and traceback](evidence/report.md)
- [Merged implementation](evidence/implementation.md)
- [Regression assertion](evidence/regression.md)

The qualification checked on 2026-10-03 is recorded separately in [provenance](provenance.json). It is not pre-cutoff learned content.
