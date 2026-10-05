# Historical episode

SourceRecord: `pylint-dev/pylint:8536:repair:b63c8a1c148e`.

The [title](evidence/title.md) and [report](evidence/body.md) identify a scope-specific naming false negative. Under the reported `pylint t.py` invocation, an incorrectly named top-level explicit alias received `C0103: invalid-name`, but an incorrectly named function-local explicit alias did not. Reported versions were Pylint 2.17.2, astroid 2.15.2, and Python 3.11.2.

The [implementation](evidence/fix.md) changed the eligible function-local branch in historical path `pylint/checkers/base/name_checker/checker.py`. Inside existing local-membership, argument-exclusion, and import-redefinition guards, it replaced unconditional variable-category naming with:

```python
if isinstance(assign_type, nodes.AnnAssign) and self._assigns_typealias(
    assign_type.annotation
):
    self._check_name("typealias", node.name, node)
else:
    self._check_name("variable", node.name, node)
```

These symbols and paths are historical observations, not automatic current bindings.

The [regression](evidence/regression.md) extended historical files `tests/functional/t/typealias_naming_style_default.py` and `tests/functional/t/typealias_naming_style_default.txt`. It added good and bad explicit local aliases, a good union-valued explicit alias, and an ordinary local union annotation followed by assignment. The new expectation identifies `local_bad_name` at historical line 39, columns 4 through 18, in `my_function`, with type-alias wording and HIGH confidence. Deletion statements provided fixture hygiene. Existing expectations remained.

The release fragment recorded that function-defined `TypeAlias` variables are now checked for `invalid-name` and stated `Closes #8536`. The core evidence does not establish historical CI or test execution.

## Validation-only qualification review

The supplied independent qualification pins original base `b5f2b01635edd23fecc1546f3fdb2a41e6a51995`, merge revision `b63c8a1c148e85e1ad4e645b7fffd8c8772d6201`, issue 8536, and fix PR 8537. It verifies historical artifacts and a direct-closure relationship.

All three supplied controls use runtime SHA256 `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, identical selected-test argv, and the same isolation mechanism. None timed out:

- Original base: exit 0; 20 passed, 1 skipped, 802 deselected.
- Base with committed regression: exit 1; 1 failed, 19 passed, 1 skipped, 802 deselected. The default alias naming fixture failed because the expected local `invalid-name` at line 39 was absent.
- Historical fixed revision: exit 0; 20 passed, 1 skipped, 802 deselected.

The default fixture is fail-to-pass under regression transplantation and also passes in the original-base comparison. The skipped Jython tokenize case is not a passing control. The report records one fail-to-pass and twenty pass-to-pass cases.

Checked at `2026-10-04T17:38:51.753104+00:00`; scope `changed-test-files-with-original-base-control`; exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.` This validation was not a formal SWE run and did not execute the newly authored Skill functional cases. Later replay logs and dependencies are not historical mechanisms or pre-cutoff learned content.

The authored Actions and Workflow are conditional contracts derived from the public repair, not claims of newly executed historical operations.
