# Historical episode

Authoritative source: `pylint-dev/pylint:4238:repair:5d5f65727829`.

The [title](evidence/title.md) and [report](evidence/body.md) describe a false `E0601` on a multiline f-string. A single-line version was reported clean. The environment was Python 3.8.8, Pylint 2.7.2, and astroid 2.5.1.

The [merged implementation](evidence/fix.md), available on 2021-03-26, changed `pylint/checkers/variables.py` and added `PY39_PLUS` in `pylint/constants.py`. It broadened a conditional-expression statement check from `Assign` to `Assign`, `AnnAssign`, `AugAssign`, and `Expr`. Separately, it added a pre-3.9 equal-line alternative for assignment-like statements with a `JoinedStr` value inside existing assignment-expression ordering logic.

The [committed assertions](evidence/regression.md) in `tests/functional/a/assignment_expression.py` covered ordinary, annotated, and augmented assignment f-strings and conditional-expression variants. Existing real earlier-read expectations remained. The expected-output file was updated for shifted lines and a `pointless-statement` diagnostic.

These are committed assertions, not evidence of historical execution. Historical CI/test-execution status is unknown.

## Validation-only source qualification

The supplied independent report was checked on 2026-10-04. Its identity pins base `09dce027f430498ba9c42c9f6502401b72f5c255`, merge `5d5f65727829240ffcb84b7be8c5d1e4dcefa0ed`, issue 4238, and PR 4253. It records verified direct closure and historical artifact identity.

The complete supplied observations and run controls were inspected:

- Original base: exit 0; 22 passed, 2 skipped.
- Base with committed regression changes: exit 1; 21 passed, 2 skipped, 1 failed. The `assignment_expression` fixture reported an unexpected `used-before-assignment` at line 13.
- Historical fixed revision: exit 0; 22 passed, 2 skipped.
- One fail-to-pass observation and 22 original-base-to-fixed pass-to-pass observations were recorded.
- All controls used the same runtime digest, reported no timeout, and adopted their isolated workspaces.

The failing fixture establishes changed-test causal support, not individual execution of the older multiline-coordinate branch. The scope is `changed-test-files-with-original-base-control`; whole-project regression and cross-project transfer were not checked.

The later report is validation-only provenance. Its date, logs, and runtime details are not backdated historical knowledge and did not execute this Skill's functional cases.
