# Historical episode

SourceRecord: `pylint-dev/pylint:4379:repair:95c05e024cf4`.

The [title](evidence/title.md) reports a crash in a new min/max refactoring checker. The [original report](evidence/body.md) supplies:

```python
var = 1
if var == -1:
    var = None
```

Running `pylint a.py` reportedly raised `AttributeError: 'UnaryOp' object has no attribute 'value'` inside `_check_consider_using_min_max_builtin`. The reported environment was pylint 2.8.0.dev1, astroid 2.5.3, and Python 3.9.4. These are historical observations, not current dependency requirements.

The [merged implementation](evidence/fix.md) changed the extraction branch from “Name, otherwise read `.value`” to “Name, Const, otherwise return.” The change left the subsequent equality check against the body assignment value in place.

Historical implementation owner:
`pylint/checkers/refactoring/refactoring_checker.py`.

The [committed regression assertions](evidence/regression.md) added the original negative-literal example and a comparison using membership in a list:

```python
var2 = 1
if var2 in [1, 2]:
    var2 = None
```

Historical regression owner:
`tests/functional/c/consider/consider_using_min_max_builtin.py`.

The supplied core evidence contains committed assertions but no historical execution result. Do not infer a historical CI pass.

## Separate qualification audit

The supplied independent report pins original base
`00a2394ec7d5aedc3e768260bf1073c85821430e`,
repair revision `95c05e024cf4d74fa25ee1a8cbcc5e08ebc1407f`,
issue 4379, and PR 4380. It records a verified direct-closure relationship and historical-artifact verification.

Its three controls used the same selected public functional tests and the same runtime digest:

- Original base: exit 0, 14 selected tests passed.
- Base with committed regressions: exit 1, target min/max functional case failed with the reported UnaryOp attribute error; 13 neighboring cases passed.
- Historical fixed revision: exit 0, all 14 selected tests passed.

All three runs report no timeout, adopted workspaces, and the same isolation configuration. The target belongs to both the fail-to-pass comparison against base-with-regression and the pass-to-pass comparison against original base; these are different controls, not contradictory observations.

Qualification time is `2026-10-04T10:42:47.590199+00:00`. This is validation-only information, not pre-cutoff historical learned content. Scope is changed test files with original-base control; whole-project regression and cross-project transfer remain untested. This report did not execute the newly authored Skill evaluation cases.

See [provenance](provenance.json) for exact source identity and qualification hash, and [Workflow](workflow.md) for the authored conditional realization.
