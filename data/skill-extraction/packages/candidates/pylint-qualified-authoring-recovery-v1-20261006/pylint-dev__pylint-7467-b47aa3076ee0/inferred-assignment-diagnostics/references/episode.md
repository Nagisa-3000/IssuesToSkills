# Historical episode

Authoritative source: `pylint-dev/pylint:7467:repair:b47aa3076ee0`.

The [title](evidence/title.md) and [body](evidence/body.md) report an `AttributeError: 'ClassDef' object has no attribute 'value'` with this reproduction:

```python
class AnotherClass:
    ...

class Pylint7429:
    def foo(self):
        self.__class__, myvar = AnotherClass, "myvalue"
```

The historical command was `pylint /tmp/pylint7429.py`. The reported environment was Pylint 2.15.2, astroid 2.12.9, Python 3.8.13, NixOS 22.05. The traceback reached `safe_infer(node.parent.value)` in `_check_invalid_class_object`.

## Visible repair mechanism

The [supplied implementation](evidence/fix.md), historically in `pylint/checkers/classes/class_checker.py`, changes E0243 from `Invalid __class__ object` to:

```text
Invalid assignment to '__class__'. Should be a class definition but got a '%s'
```

Its emission adds `args=inferred.__class__.__name__` and retains `node=node` and `confidence=INFERENCE`. Visible context retains the uninferable-value return. No parent-access or unpacking-inference edit appears in the supplied diff.

The [committed assertions](evidence/regression.md), historically in `tests/functional/i/invalid/invalid_class_object.txt`, change five message texts: one `Instance` and four `Const`. Diagnostic symbols, locations, object labels, and confidence remain unchanged. These assertions were available at the historical revision; historical CI/test execution is unknown.

## Validation-only qualification audit

The supplied independent report was checked at `2026-10-04T15:35:43.286704+00:00`, after the historical cutoff. It pins original base `edba81bc48a7157ec0b1c366b89e0ec9a8af2ea7`, PR 7473, and merge revision `b47aa3076ee0c2dc3f7f6b238c268a48e2e67bdb`. It reports verified historical artifacts and a verified direct-closure issue/fix relationship.

Inspection of all three controls shows:

- Original base: exit 0, 31 selected tests passed.
- Base with regression expectations: exit 1, 30 passed and `invalid_class_object` failed on diagnostic text mismatch.
- Historical fixed revision: exit 0, 31 passed.
- All runs share runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`; none timed out, and all report adopted workspaces.
- The reported pass-to-pass list has 31 original-base/fixed successes, including the target. That differs from the 30 passing cases in the base-with-regression control.
- This was not a formal SWE run; whole-project regression was not checked.

The failed control demonstrates a diagnostic-text mismatch, not a replay of the reported crash. Qualification supports the narrow diagnostic/assertion transition and selected adjacent behavior. It does not supply a missing traversal repair.

Exact scope: `changed-test-files-with-original-base-control`.

Exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

The report and its runtime details are validation-only provenance, not backdated historical learning or execution of this Skill's functional cases. The report hash is preserved in [provenance](provenance.json).
