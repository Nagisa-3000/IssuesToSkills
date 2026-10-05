# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:8747:repair:8614ccf21aa7`.

The report describes `inconsistent-return-statements` on a caller that returns `1` in a `try` branch and calls a `NoReturn`-annotated method in its exception handler. The reporter reproduced the warning with Pylint 2.15.8 and 2.17.4.

Historical reproduction command:

```sh
pylint --disable=all --enable=inconsistent-return-statements repro.py
```

The investigation states that `node.func.inferred()[0]` for the method call produces `astroid.BoundMethod`, whereas `_is_function_def_never_returning` only inspects `nodes.FunctionDef`.

## Implementation and assertions

At revision `8614ccf21aa760cdcff537150a30e5ae59a6d3a6`, in `pylint/checkers/refactoring/refactoring_checker.py`, the helper's input declaration changed to `nodes.FunctionDef | astroid.BoundMethod`. Its argument documentation was updated. The guard changed from:

```python
isinstance(node, nodes.FunctionDef) and node.returns
```

to:

```python
isinstance(node, (nodes.FunctionDef, astroid.BoundMethod)) and node.returns
```

The existing annotation checks remained. The supplied diff explicitly shows the `nodes.Attribute` branch checking `attrname == "NoReturn"`; it does not support inventing additional annotation forms.

`tests/functional/i/inconsistent/inconsistent_returns_noreturn.py` added three method-call contrasts:

- `typing.NoReturn`, implemented with `sys.exit(1)`: no return-consistency warning expected for the caller.
- `int`, implemented with `return 1`: warning expected for the caller's fallthrough exception path.
- `typing.NoReturn`, incorrectly implemented with `return 1`: no warning expected for the caller because this check trusts the annotation.

The corresponding `.txt` expected-diagnostics file added only the ordinary-returning caller. These are committed assertions, not evidence of historical execution. Historical CI/test-execution status is unknown.

## Evidence index

- [Title](evidence/title.md)
- [Report and inference investigation](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertions](evidence/regression.md)

## Validation-only qualification audit

The supplied independent report was checked at `2026-10-04T18:27:43.547189+00:00`. Its identity pins:

- Issue: `pylint-dev/pylint:8747`.
- Fix: `pylint-dev/pylint:pr:8750`.
- Original base: `1ef3b0be3c018ab4f2928932ab1f46ee244b79bb`.
- Merged revision: `8614ccf21aa760cdcff537150a30e5ae59a6d3a6`.
- Relationship: verified direct closure; historical artifact and issue relationship verified.

The complete supplied controls were inspected. All three runs used the same runtime hash, adopted the workspace, and did not time out. Original base passed all five selected cases with exit code 0. Base with the committed regressions passed four and failed `inconsistent_returns_noreturn` with exit code 1, reporting unexpected warnings at lines 67 and 87. Historical fixed passed all five with exit code 0.

The report lists one fail-to-pass case and five original-base pass-to-pass cases. These lists use different controls; the NoReturn suite appears in both. This is a validation-only causal comparison, not a historical CI event.

Exact qualification scope: `changed-test-files-with-original-base-control`.

Exact scope limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

Whole-project regression was not checked and this was not a formal SWE run. No contemporary runtime or replay command is promoted to historical mechanism or current executable guidance. Qualification does not backdate knowledge and did not execute the authored functional cases. Report identity, hashes, control outcomes, and limits are recorded in [provenance](provenance.json).
