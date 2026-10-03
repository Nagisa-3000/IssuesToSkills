# Historical episode

Authoritative SourceRecord: `PyCQA/pyflakes:744:repair:e0d7a6be8959`.

The [title](evidence/title.md) framed the issue as an internal error on an invalid Python-2-style print statement. The [report](evidence/report.md) supplied `print *= -1` under flake8 6.0.0 and pyflakes 3.0.0. Its Python 3.10 traceback reached `AUGASSIGN`, `handleNodeLoad`, and `getParent`, then failed with:

```text
AttributeError: 'Name' object has no attribute '_pyflakes_parent'
```

The early load call occurred before ordinary target handling. The parent lookup was inside the builtin-`print` diagnostic branch.

The [merged implementation](evidence/fix.md), historically in `pyflakes/checker.py`, changed `handleNodeLoad(self, node)` to `handleNodeLoad(self, node, parent)`. Ordinary `NAME` load dispatch supplied `self.getParent(node)`; `AUGASSIGN` supplied `node`. The builtin-print branch stopped retrieving the parent internally, while retaining its `ast.BinOp` and `ast.RShift` diagnostic condition. Value handling and target handling remained in their existing order after the early load.

The [regression](evidence/regression.md), historically in `pyflakes/test/test_other.py`, added `TestIncompatiblePrintOperator.test_print_augmented_assign`, calling `self.flakes('print += 1')` with the comment “nonsense, but shouldn't crash pyflakes”.

Historical paths and symbols are evidence, not automatic current bindings. The inspection and validation Actions reconstruct useful operations supported by this mechanism; they do not assert that a historical investigator executed those exact operations.

## Resolution and test status

The SourceRecord marks the resolution verified. Historical regression assertions were available at the merged revision; no historical execution transcript is supplied.

A qualification checked at `2026-10-03T19:13:45.835410+00:00` reports one fail-to-pass and 126 pass-to-pass results, scoped to changed test files with original-base control. It is contemporary provenance, not pre-cutoff learned content. Whole-project regression and cross-project transfer were not tested.
