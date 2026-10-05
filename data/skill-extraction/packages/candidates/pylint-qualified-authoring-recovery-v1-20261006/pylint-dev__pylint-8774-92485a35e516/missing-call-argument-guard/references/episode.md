# Historical episode

SourceRecord: `pylint-dev/pylint:8774:repair:92485a35e516`.

The [title](evidence/title.md) and [report](evidence/body.md) describe analysis of:

```python
from copy import copy
copy()
```

The reported command was `pylint a.py`. The checker attempted to obtain positional argument zero. `NoSuchArgumentError` escaped from `get_argument_from_call`, and the linter wrapped it in `AstroidError`. The report named pylint 3.0.0b1, astroid 3.0.0a6-dev0, and Python 3.11.2. Expected behavior was no crash.

## Historical implementation

At revision `92485a35e51618a0fd8397cc60746e14541444e7`, the relevant owner was `pylint/checkers/stdlib.py`, method `StdlibChecker._check_shallow_copy_environ`.

The [implementation evidence](evidence/fix.md) shows:
- initialize confidence to `HIGH`;
- request positional argument zero or keyword `x`;
- catch `utils.NoSuchArgumentError`;
- try `utils.infer_kwarg_from_call(node, keyword="x")`;
- return when that does not yield an argument;
- use `INFERENCE` for the fallback;
- retain the existing `astroid.InferenceError` early return;
- emit `shallow-copy-environ` only for an inferred value whose qualified name equals `OS_ENVIRON`, now with explicit confidence.

The patch also added `doc/whatsnew/fragments/8774.bugfix`. An unrelated IDE documentation URL changed in the same diff; it is not part of this Skill's repair mechanism.

## Historical committed assertions

The [regression evidence](evidence/regression.md) concerns `tests/functional/s/shallow_copy_environ.py` and its `.txt` expectation file.

The new cases include no argument, direct `x`, unpacked `x`, unpacked wrong `y`, and direct wrong `y`. Existing direct positional warnings changed expected confidence from `UNDEFINED` to `HIGH`; the unpacked `x` warning expects `INFERENCE`.

The fixture visible in supplied qualification controls also includes dictionary copying, an imported alias, an uninferable object, and `copy.deepcopy(os.environ)`. These are adjacent cases retained in the qualified selected test. Later replay visibility is not used to invent additional historical evidence cards.

The historical commit supplies assertions, not evidence of historical test execution. Historical CI/test execution remains unknown.

## Validation-only qualification audit

The supplied independent report pins:
- base: `507dfc5ebd0cd9712ac4840cae3bea8623206554`;
- fix: `pylint-dev/pylint:pr:8784`;
- merge: `92485a35e51618a0fd8397cc60746e14541444e7`;
- issue: `pylint-dev/pylint:8774`;
- repair availability: `2023-06-18T14:43:15Z`;
- relationship: verified direct closure.

The report's closure event reference is audit metadata, not an additional packaged historical evidence card.

The complete supplied controls show:
- original base: 17 selected tests passed, exit 0;
- base with committed regression: the shallow-copy-environ test failed with the missing-argument crash, 16 others passed, exit 1;
- historical fixed revision: 17 selected tests passed, exit 0.

All three runs used the same reported runtime digest, adopted workspaces, and the same isolation configuration; none timed out. The shallow-copy-environ test is both the fail-to-pass regression comparison and a pass-to-pass comparison against its original-base fixture. These are different controls, not a contradiction.

Checked at `2026-10-04T18:32:27.076449+00:00`.
Scope: `changed-test-files-with-original-base-control`.
Limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

This qualification is validation-only. It is not backdated historical execution and did not execute this Skill's newly authored functional cases.
