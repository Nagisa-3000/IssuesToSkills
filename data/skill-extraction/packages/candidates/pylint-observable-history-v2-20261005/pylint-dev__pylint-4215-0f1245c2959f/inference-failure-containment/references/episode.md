# Historical episode

Authoritative source: `pylint-dev/pylint:4215:repair:0f1245c2959f`.

The [title](evidence/title.md) was `NameInferenceError`. The [report](evidence/body.md) reproduced the failure with:

```python
if len(dont_care[0]):
    pass
```

The reported environment was Pylint 2.7.2, astroid 2.5.1, and Python 3.9.2 on Windows. Analysis emitted `missing-module-docstring`, then crashed. The traceback reached historical `pylint/checkers/refactoring/len_checker.py`, `LenChecker.visit_call`, at `instance = next(len_arg.infer())`. Subscript inference attempted to resolve `dont_care` and raised `NameInferenceError`.

The [merged implementation](evidence/fix.md), available at 2021-03-08T16:55:45Z, protected that expression:

```python
try:
    instance = next(len_arg.infer())
except astroid.InferenceError:
    return
```

The preceding generator/comprehension branch and subsequent base-class inspection remained outside the catch.

The [regression assertions](evidence/regression.md) added the following to historical `tests/functional/l/len_checks.py`:

```python
if len(undefined_var):  # [undefined-variable]
    pass
if len(undefined_var2[0]):  # [undefined-variable]
    pass
```

Historical `tests/functional/l/len_checks.txt` added undefined-variable expectations for both names. These are committed assertions, not a record of historical execution. Historical CI/test execution remains unknown.

## Validation-only qualification

The supplied complete qualification report pins original base `ba4941b96c12f32d1eb91868c1ce040f3f7f48e2`, fix `pylint-dev/pylint:pr:4216`, merged revision `0f1245c2959f16dd68a2f7cf191c3cee0fcc08c2`, and direct closure. Its three controls have matching runtime hashes and completed without timeout.

At validation time 2026-10-04T10:30:07.806225+00:00:

- Original base: 16 selected functional tests passed.
- Base with committed regressions: `len_checks` failed at argument inference with `NameInferenceError`; 15 selected tests passed.
- Historical fixed revision: 16 selected functional tests passed.

The one fail-to-pass comparison uses base-with-regression versus historical-fixed. The 16 pass-to-pass comparisons use original-base versus historical-fixed. These comparisons are distinct.

Scope is `changed-test-files-with-original-base-control`. Whole-project regression and cross-project transfer were not tested. The report is validation-only, not historical CI evidence, a formal SWE run, or execution of newly authored Skill cases. Its runtime and logs do not prescribe historical dependencies or current commands.
