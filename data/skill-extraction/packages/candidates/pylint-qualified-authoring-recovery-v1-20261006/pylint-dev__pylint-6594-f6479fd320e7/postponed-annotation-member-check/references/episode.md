# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:6594:repair:f6479fd320e7`.

## Report and repair

The [title](evidence/title.md) identifies a `no-member` annotation error. The [report](evidence/body.md) describes Pylint 2.14.0-b1, astroid 2.12.0-dev0, and Python 3.9.12. With postponed evaluation enabled, an annotation using `ast.Match` reportedly produced E1101. The reporter expected these checks to be left to a type checker, similarly to string annotations.

The [implementation](evidence/fix.md) imported `is_node_in_type_annotation_context` into `pylint/checkers/typecheck.py`. Before `node.expr.infer()`, it returned when both `is_postponed_evaluation_enabled(node)` and `is_node_in_type_annotation_context(node)` held.

The [regression](evidence/regression.md) replaced the `print_function` future import with `annotations` in `tests/functional/g/generated_members.py` and added:

```python
print(Klass.X)  # [no-member]
var: "Klass.X"
var2: Klass.X
```

The expected-output file retained the missing `spam` diagnostic and added a missing `X` diagnostic for runtime access only. These are committed assertions. Original historical CI/test execution is unknown.

The [Workflow](workflow.md) reconstructs reusable inspection, editing, and validation operations from this evidence. It does not assert that the newly authored contracts or evaluation cases ran historically.

## Independent qualification audit — validation only

The supplied complete controls were inspected for pinned identity, closure, causal outcomes, and runtime consistency.

- Base: `0c37d4c6875e0c1c81a51cd1a02ee270d50c53df`.
- Historical fixed revision: `f6479fd320e78c0f8c7e4ab0751c302e656c64bf`.
- Issue: `pylint-dev/pylint:6594`.
- Fix: `pylint-dev/pylint:pr:6608`, pull number 6608.
- Relationship: `direct_closure`.
- Supplied closure audit locator: `pylint-dev/pylint:6594:event:CE_lADOAtdnV85Jk81MzwAAAAGJ2x6M`.
- Historical artifact and issue relationship were reported verified; legacy register checking was not required.
- Repair availability: `2022-05-13T18:48:10Z`, before the exclusive cutoff `2024-01-01T00:00:00Z`.

The closure locator is validation-only audit metadata, not an additional core historical evidence card.

All three controls used this replay argv:

```text
python3 -m pytest tests/test_functional.py -k "__init__ or generated_members or genexp_in_class_scope or genexpr_variable_scope or globals" -q --junitxml=/workspace/verification-results.xml
```

This later replay command is not a current Skill oracle binding.

| Test | Original base | Base with regression | Historical fixed |
|---|---|---|---|
| generated_members | passed | failed | passed |
| genexp_in_class_scope | passed | passed | passed |
| genexpr_variable_scope | passed | passed | passed |
| globals | passed | passed | passed |

Original base exited 0: 4 passed, 756 deselected, 2.17 seconds. Base with regression exited 1: 1 failed, 3 passed, 756 deselected, 2.39 seconds. Its mismatch reported unexpected `28: no-member`. Historical fixed exited 0: 4 passed, 756 deselected, 2.47 seconds.

The report identifies one fail-to-pass case and four pass-to-pass entries, including the original generated_members control. All runs reported `timed_out: false`, `workspace_adopted: true`, and isolation `linux-copied-user-mount-pid-net-chroot-nobody-no-capabilities-v1`; the backend was `namespace-copy`.

All three runs and the report share runtime SHA-256:
`862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

Observations SHA-256:
`de9cedd69a4da8519783e4d697cb667c32ae08418224783d5d35cdf6885e18cd`.

Qualification report hash:
`9cb6d48ae21859d9619b9bb9748fa382982a36daf44e3eb5f71e81dcc331c18a`.

Checked at `2026-10-04T14:34:59.698801+00:00`, using schema `historical-causal-verification-v1`. This was not a formal SWE run. Whole-project regression was not checked.

Exact scope: `changed-test-files-with-original-base-control`.

Exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

These observations qualify the already-public historical repair; they do not backdate new information, supply historical mechanisms from contemporary runtime details, or execute this Skill's functional cases. Historical execution remains unknown; authored evaluation suites remain `not_executed`.
