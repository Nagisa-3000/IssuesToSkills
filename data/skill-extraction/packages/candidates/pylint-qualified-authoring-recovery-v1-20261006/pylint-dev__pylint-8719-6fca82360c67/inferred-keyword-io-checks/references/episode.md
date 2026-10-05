# Historical episode

Authoritative source: `pylint-dev/pylint:8719:repair:6fca82360c67`.

The [report](evidence/body.md) described W1514 for:
```python
CSV_KWARGS = {"newline": "", "encoding": "utf-8"}
with open("foo.csv", **CSV_KWARGS):
    pass
```

The reported command was `pylint --score=false a.py`. Reported versions were Pylint 2.17.4, astroid 2.15.4, and Python 3.10.10. These are historical report context, not current environment requirements.

The [implementation](evidence/fix.md) added dictionary-keyword inference in `pylint/checkers/utils.py` and integrated it into `pylint/checkers/stdlib.py`. Ordinary lookup remained first; mode and encoding confidence were initialized separately.

Historical regression resources:
- `tests/functional/b/bad_open_mode.txt`
- `tests/functional/u/unspecified_encoding_py38.py`
- `tests/functional/u/unspecified_encoding_py38.txt`

The release fragment `doc/whatsnew/fragments/8719.false_positive` says “Closes #8719.” Committed assertions cover binary mode, text encoding, invalid mode, and explicit `None`; their historical execution status is unknown.

## Validation-only qualification audit

The supplied complete original-base, base-with-regression, and historical-fixed observations and run outputs were inspected. Pinned identity agrees with issue 8719, PR 8728, direct closure, and repair revision `6fca82360c674990eee6de8a6303c834b77bef61`.

- Original base `893b98e47594440904684b70d4448d06d3d7c251`: exit 0; 37 passed, 1 skipped.
- Base with committed regression assertions: exit 1; 2 failed, 35 passed, 1 skipped.
- Historical fixed revision: exit 0; 37 passed, 1 skipped.
- All controls deselected 794 tests, were not timed out, and used adopted isolated workspaces.
- The two augmented targets failing against the base were `bad_open_mode` and `unspecified_encoding_py38`. The former exposed confidence mismatches. The latter exposed missed inferred invalid modes and false-positive encoding warnings.
- The 37 original-base-to-fixed preservation targets include those two targets with their original assertions. One target was skipped in all controls.
- All controls shared runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.
- The report verifies historical artifacts and direct closure. Its closure-event locator is validation metadata, not an additional historical evidence card.

Checked at `2026-10-04T18:12:27.405790+00:00`. This is not pre-cutoff learned content or a formal SWE run. Scope: `changed-test-files-with-original-base-control`. Limits: “Changed test files only; whole-project regression and cross-project transfer are untested.”

This source qualification does not constitute execution of the newly authored Skill cases. Historical CI status remains unknown.
