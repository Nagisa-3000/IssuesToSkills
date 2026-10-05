# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:3413:repair:922f38969c32`.

The [title](evidence/title.md) and [body](evidence/body.md), available on 2020-02-19, requested a check for `open()` without `with`, with possible coverage of other resource-allocating library calls.

The merged repair was available at `2021-04-23T18:31:22Z`, revision `922f38969c326826344e2d25af499cf8c5f80d8c`. It introduced `R1732`, `consider-using-with`, with message text “Consider using 'with' for resource-allocating operations.” The ChangeLog stated “Closes #3413.”

## Historical owners and paths

- `pylint/checkers/refactoring/refactoring_checker.py`: message registry, finite callable-name sets, safe inference, and assignment/call routing.
- `tests/functional/c/consider/consider_using_with.py` and `.txt`: 22 expected messages and several direct-with negative examples.
- `tests/functional/c/consider/consider_using_with_open.py`, `.rc`, and `.txt`: builtin-open assertions with PyPy exclusion.
- `pylint/epylint.py` and `pylint/graph.py`: local subprocess/file lifetimes converted to `with`.
- Spelling, parallel linting, diagram writing, and test utilities: some allocation sites explicitly suppressed the suggestion.
- `ChangeLog` and `doc/whatsnew/2.8.rst`: public feature documentation.
- Message-control and non-iterator fixtures: suppression and expectation integration.

These paths identify historical realizations only. Current Actions bind semantic owners afresh.

The [implementation](evidence/fix.md) and [committed assertions](evidence/regression.md) support the mechanism. They do not establish historical test execution; historical CI status is unknown.

## Validation-only qualification audit

The complete supplied qualification report pins original base `81c7c50ad0273e2027f636edbddba9d410c8319a`, issue 3413, PR 4372, and the merged revision above. It reports verified direct closure and historical-artifact identity. All three controls used the same runtime digest, completed without timeout, and recorded adopted isolated workspaces.

At qualification time `2026-10-04T09:26:06.575051+00:00`:

- Original base: exit 0; 38 passed.
- Base with committed regression changes: exit 1; 3 failed, 37 passed.
- Historical fixed tree: exit 0; 40 passed.

The two new resource fixtures failed without the implementation and passed with it. The third intermediate failure, `non_iterator_returned`, was an unknown-message suppression producing `bad-option-value`; it passed on both original base and historical fixed tree. The report’s 38 original-to-fixed pass-to-pass cases therefore do not imply 38 intermediate passes.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression, cross-project transfer, and the newly authored Skill functional cases were not checked. The replay date is validation time, never backdated historical knowledge. Runtime and replay details do not supply additional historical mechanisms or commands for current tasks.
