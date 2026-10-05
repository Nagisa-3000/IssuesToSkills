# Historical episode

Authoritative SourceRecord ID: `pylint-dev/pylint:8740:repair:331e48f74654`.

The [title](evidence/title.md) identifies an undefined-`__all__` inference failure. The [original report](evidence/body.md) supplies:

```python
import sys
if sys.version_info >= (3, 7):
    __all__ += runners.__all__
```

Neither `__all__` nor `runners` is defined. Reported output includes undefined-variable diagnostics for both names before a fatal analyzer error. The traceback reaches `VariablesChecker._check_all` at:

```python
assigned = next(node.igetattr("__all__"))
```

Consumption raises `astroid.exceptions.InferenceError`.

The [merged repair](evidence/fix.md) changes that boundary to:

```python
try:
    assigned = next(node.igetattr("__all__"))
except astroid.InferenceError:
    return
```

Existing `util.UninferableBase` handling and the subsequent list/tuple type check remain after the guard. The [committed regression](evidence/regression.md) contains `__all__ += []` and expects the undefined-variable diagnostic.

## Historical locators

These identify historical resources only:

- `pylint/checkers/variables.py`, `VariablesChecker._check_all`
- `tests/functional/u/undefined/undefined_all_variable_edge_case.py`
- `tests/functional/u/undefined/undefined_all_variable_edge_case.txt`
- `tests/functional/n/names_in__all__.py`, referenced in the new fixture
- `doc/whatsnew/fragments/8740.bugfix`

Current semantic owners must be independently located.

## Execution and qualification boundary

Historical CI/test execution is **unknown**. Assertions were available at the historical commit; no historical execution log is supplied.

The later independent qualification was checked at `2026-10-04T18:25:38.073035+00:00`. Its controls pin the original base, that base with the committed regression, and the historical fixed revision:

| Control | Observations |
| --- | --- |
| Original base | Nine neighboring cases passed; one case skipped; the new regression was absent. |
| Base with regression | The new regression failed with unexpected `astroid-error`; nine neighboring cases passed; one case skipped. |
| Historical fixed | The new regression passed; the same nine neighboring cases passed; the same case skipped. |

All three controls completed without timeout and recorded the same runtime digest. The original-base and historical-fixed runs exited zero; base-with-regression exited one. The qualification confirms historical artifact identity and the direct issue/fix closure relationship. The closure reference belongs to the validation audit, not an additional historical evidence card.

Qualification scope: `changed-test-files-with-original-base-control`.

Exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

This later replay is validation-only provenance, not historical learned content to backdate. Its runtime details do not define the repair mechanism or establish cross-project transfer. It did not execute the newly authored Skill evaluations. The [Workflow](workflow.md) reconstructs evidence-backed operations and verification obligations; it does not assert that these authored contracts were historically executed.
