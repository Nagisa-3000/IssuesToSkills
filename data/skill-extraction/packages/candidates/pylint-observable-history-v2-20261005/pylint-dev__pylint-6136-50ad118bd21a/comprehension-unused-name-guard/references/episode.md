# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:6136:repair:50ad118bd21a`.

The issue reported `W0612` for a local list named `project_id` used as the iterable in a generator expression whose target was also `project_id`. The reporter attributed this regression to #6073; that attribution is a reported observation, not a separately reconstructed cause.

The repair moved the existing comprehension-target membership exclusion above the argument/local-variable dispatch. Matching names then returned before either unused-name branch. The argument branch retained `_check_unused_arguments` for other names.

## Historical anchors

These paths identify historical artifacts only:

- `pylint/checkers/variables.py`: `VariablesChecker`, unused-name handling around `argnames = node.argnames()`.
- `tests/functional/u/unused/unused_variable.py`: added `func5()` with `x = []` and `assert [True for x in x]`.
- `tests/functional/u/undefined/undefined_variable_py38.py`: removed the unused-variable annotation on `my_int: int` before a comprehension binding `my_int`.
- `tests/functional/u/undefined/undefined_variable_py38.txt`: removed the corresponding expected unused-variable message while retaining nearby used-before-assignment records.
- `ChangeLog`: added `Closes #6136`.

Repair revision: `50ad118bd21a893af3771363bcc513bc0d430269`, available at `2022-04-03T13:18:22Z`.

## Evidence

- [Issue title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertions](evidence/regression.md)

## Independent qualification boundary

The supplied validation-only report pins original base `30302f2555008a83db77aa0d61696bf5da4b3c51`, issue #6136, PR #6154, the repair revision, and a verified direct-closure relationship. Its complete controls show:

- Original base with original assertions: 28 passed, exit 0.
- Base with committed regression changes: 26 passed and two failed, exit 1. The failures were unexpected `unused-variable` messages in `undefined_variable_py38` at line 126 and `unused_variable` at line 179.
- Historical fixed code: 28 passed, exit 0.

All three runs reported the same runtime digest, no timeout, and the same selected test harness. The report's 28 pass-to-pass identities describe original-base-to-fixed outcomes; they are not 28 passing controls in the base-with-regression run. Two modified fixtures also belong to the fail-to-pass set.

Qualification occurred at `2026-10-04T13:58:30.575326+00:00`. It is not pre-cutoff learned content and is not backdated. The report supports changed-test-file causal qualification, not whole-project regression coverage or transfer. Historical CI execution remains unknown. No newly authored Skill functional case was executed.

See [provenance](provenance.json) for exact source and qualification hashes.
