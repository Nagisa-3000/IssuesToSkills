# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:7319:repair:7fdf8d9ee090`.

## Public historical evidence

The [title](evidence/title.md) and [report](evidence/body.md) describe this constructor:

```python
class CustomError(Exception):
    def __init__(self, message="default"):
        super().__init__(message)
```

The reporter ran `pylint a.py` using Pylint 2.14.5, astroid 2.11.7, and Python 3.9.13 on macOS 12.4. Reported output was W0235, `useless-super-delegation`, at `a.py:3:4`. The reporter expected no warning because the override introduced a default argument.

The [merged implementation](evidence/fix.md) added the following disjunct to the existing early-return condition in `pylint/checkers/classes/class_checker.py`:

```python
or (meth_node.args.args is None and function.argnames() != ["self"])
```

Its comment says arguments to builtins such as `Exception.__init__()` cannot be inspected. The existing parameter-default comparison was retained. The new fragment `doc/whatsnew/fragments/7319.bugfix` describes preventing `useless-parent-delegation` for delegation to C-written builtins with non-self arguments and states `Closes #7319`.

The [regression assertion](evidence/regression.md) appends the same constructor to `tests/functional/u/useless/useless_parent_delegation.py` without an expected diagnostic annotation. These implementation and assertion facts were available at revision `7fdf8d9ee09076515739fc997837b6c7c79a6072` on `2022-08-21T14:02:23Z`. Historical CI execution is unknown.

The operational Workflow is authored from this evidence; it is not a claim that the historical maintainer executed the newly authored Actions.

## Separate validation-only qualification audit

The supplied complete qualification report was inspected. It was checked at `2026-10-04T15:22:04.119789+00:00`, not at the historical repair time. Its schema is `historical-causal-verification-v1`.

Identity controls pin issue `pylint-dev/pylint:7319`, fix `pylint-dev/pylint:pr:7329`, original base `29e74e45cfe7922fc97012c3c14b7e4b319d45be`, and merged revision `7fdf8d9ee09076515739fc997837b6c7c79a6072`. The exclusive cutoff is `2024-01-01T00:00:00Z`, and repair availability is `2022-08-21T14:02:23Z`.

The report marks artifact and issue-relationship verification true, with direct closure. The supplied relationship locator `pylint-dev/pylint:7319:event:CE_lADOAtdnV85QCUkbzwAAAAGuzrYu` is validation audit metadata, not an additional authored historical evidence card.

All three controls used the same selection:

```text
python3 -m pytest tests/test_functional.py -k "useless_else_on_loop or useless_object_inheritance or useless_parent_delegation or useless_parent_delegation_py38 or useless_return or useless_suppression or useless_with_lock" -q
```

Actual run argv additionally included `--junitxml=/workspace/verification-results.xml`.

| Selected case | Original base | Base with regression | Historical fixed |
|---|---|---|---|
| useless_else_on_loop | passed | passed | passed |
| useless_object_inheritance | passed | passed | passed |
| useless_parent_delegation | passed | failed | passed |
| useless_parent_delegation_py38 | passed | passed | passed |
| useless_return | passed | passed | passed |
| useless_suppression | passed | passed | passed |
| useless_with_lock | passed | passed | passed |

Original base exited 0 with 7 passed. Base with regression exited 1 with 1 failed and 6 passed, reporting unexpected `useless-parent-delegation` at line 431. Historical fixed exited 0 with 7 passed. Each run deselected 764 cases, adopted its workspace, and did not time out.

All three runtime hashes match:
`862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

Backend was `namespace-copy`; isolation was `linux-copied-user-mount-pid-net-chroot-nobody-no-capabilities-v1`. These contemporary runtime details are not historical mechanisms.

The fail-to-pass list contains the delegation case. The seven-entry pass-to-pass list compares original base to historical fixed, so it does not contradict the regression-only failure.

Exact scope: `changed-test-files-with-original-base-control`.

Exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

The report states `whole_project_regression_checked: false`, `formal_SWE_run: false`, and `verification_does_not_backdate_new_information: true`.

Report hash: `47ab5adbb4de6a5580f98ad8f94483d311d6d445b2284629947f0df1d294a968`.

Observations hash: `c7fb8e7c3704ad994cc7f74ed11bd0c58f8ae54c7a1e6bbc2f80c6e53fa5dc2c`.

This qualification supports the historical repair within that scope only. It does not establish whole-project correctness, transfer, historical CI execution, or execution of the authored Skill functional cases.
