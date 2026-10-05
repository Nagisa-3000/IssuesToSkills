# Historical episode

Authoritative SourceRecord ID: `pylint-dev/pylint:3763:repair:5d5f65727829`.

The [title](evidence/title.md) identifies a Python 3.8 ternary assignment false positive. The [body](evidence/body.md) reports that:

```python
foo if (foo := 3 - 2) > 0 else 0
```

evaluates to `1`, but `pylint somefile.py` emits E0601. Reported versions were Pylint 2.5.3, astroid 2.4.2, and Python 3.8.3. These are historical observations, not prescribed current dependencies.

The merged revision `5d5f65727829240ffcb84b7be8c5d1e4dcefa0ed`, available at `2021-03-26T21:01:46Z`, changed these historical resources:

- `pylint/checkers/variables.py`: widened the conditional-expression statement gate from `astroid.Assign` to `Assign`, `AnnAssign`, `AugAssign`, and `Expr`, retaining the `IfExp` value, same-frame, and ancestor conditions.
- The same checker: added a pre-3.9 equal-line fallback restricted to assignment-like statements with `JoinedStr` values.
- `pylint/constants.py`: added `PY39_PLUS = sys.version_info[:2] >= (3, 9)`.
- `tests/functional/a/assignment_expression.py` and `.txt`: added positive fixtures, multiline f-string examples, and expected diagnostics while retaining genuine early-read E0601 expectations.
- `ChangeLog`: recorded improved assignment-expression handling and closure of #3763 and #4238.

The co-mentioned #4238 is not a second independently qualified source. The standalone reproduction expects `pointless-statement`, not E0601. Expected-message line offsets changed because fixtures were inserted; those offsets are historical, not portable owner bindings.

The [implementation card](evidence/fix.md) and [regression card](evidence/regression.md) describe committed artifacts. Original historical test execution is unknown.

Later validation-only qualification inspected the original base, that base with the committed regression, and the historical fixed revision. It reports a regression-induced assignment-expression failure and a fixed pass under consistent runtime hashes. Its scope does not establish every runtime branch or whole-project correctness. No newly authored Skill evaluation was executed.

The [Workflow](workflow.md) is an authored representation of the sourced mechanism. Its inspection and validation instructions are conditional operations for current use, not newly discovered historical execution events.
