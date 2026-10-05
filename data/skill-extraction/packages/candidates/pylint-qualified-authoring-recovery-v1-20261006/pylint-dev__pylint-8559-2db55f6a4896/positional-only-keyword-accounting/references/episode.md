# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:8559:repair:2db55f6a4896`.

The [report](evidence/body.md) described no lint output from `pylint a.py` for `required_positional_with_var_kwargs(a=43)` when the function signature was `(a, /, **_kwargs)`. The expected diagnostic was `no-value-for-parameter`. Reported versions were Pylint 3.0.0b1, astroid 2.16.0dev0, and Python 3.8.10.

The [merged implementation](evidence/fix.md) inserted this branch in historical owner `pylint/checkers/typecheck.py`, before the normal assignment marking a matched parameter supplied:

```python
elif (
    keyword in [arg.name for arg in called.args.posonlyargs]
    and called.args.kwarg
):
    pass
```

Consequently, the captured keyword no longer marks the same-named positional-only parameter satisfied. The existing missing-required-parameter machinery remains responsible for reporting its absence.

The [committed regression](evidence/regression.md) added historical files:

- `tests/functional/a/arguments_positional_only.py`;
- `tests/functional/a/arguments_positional_only.rc`;
- `tests/functional/a/arguments_positional_only.txt`.

Only `name1(param1=43)` expects `no-value-for-parameter`; the four legal neighboring calls have no expected diagnostics. The configuration requires Python 3.8. The expected output names `param1` and line 11.

The changelog fragment `doc/whatsnew/fragments/8559.false_negative` records the false-negative correction and `Closes #8559`. Its prose says `*kwargs`; the implementation and test signatures concern `**kwargs`.

These are historical report, implementation, and assertion facts. Historical CI/test-execution status is unknown. The authored Action sequence is a conditional reconstruction, not newly verified historical execution.

## Validation-only qualification audit

The complete supplied independent report was inspected for pinned identity, direct closure, original-base control, base-with-regression failure, fixed-tree outcome, and runtime consistency. It pins original base `4c0a32334d9a5b73dcfe3f56868bb933da8e9a3f`, merge `2db55f6a48962aa7ff4cc3b0ee4b37177f605bdc`, issue 8559, and PR 8575.

Original base passed 20 selected cases without the new regression. Base with regression failed only `arguments_positional_only`, reporting the absent expected diagnostic, while the same 20 controls passed. The historical fixed tree passed all 21 selected cases. All three runs used runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, had no timeout, and adopted their workspaces. Exit codes were respectively 0, 1, and 0.

The report was checked at `2026-10-04T17:50:09.970472+00:00`. Its scope is exactly `changed-test-files-with-original-base-control`. Its limits are exactly: “Changed test files only; whole-project regression and cross-project transfer are untested.”

This later causal qualification is not a 2023 test event, a formal SWE run, a whole-project check, or execution of the newly authored Skill cases. Its supplied hash is retained in provenance. Contemporary replay commands and runtime details do not supply historical repair mechanisms.
