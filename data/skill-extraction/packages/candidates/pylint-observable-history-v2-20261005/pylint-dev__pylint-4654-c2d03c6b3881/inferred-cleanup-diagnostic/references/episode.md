# Historical episode

Authoritative source: `pylint-dev/pylint:4654:repair:c2d03c6b3881`.

The issue reported R1732 (`consider-using-with`) on five `open(...)` calls directly passed to `stack.enter_context(...)` inside `with contextlib.ExitStack() as stack`. The expected output contained no such warnings.

The reporter observed the issue with Pylint 2.9.3 and 3.0.0-a4 using astroid 2.6.2 on Python 3.8.9, and reported no issue with Pylint 2.8.3 and astroid 2.5.6. These are report observations, not comparisons executed by this Skill.

## Historical bindings and mechanism

The merged implementation changed historical path `pylint/checkers/refactoring/refactoring_checker.py`. It added `_will_be_released_automatically(node: astroid.Call) -> bool`, which:
- Requires `node.parent` to be an `astroid.Call`.
- Uses `utils.safe_infer(node.parent.func)`.
- Returns false when inference fails.
- Matches `func.qname()` against `contextlib._BaseExitStack.enter_context` and `contextlib.ExitStack.enter_context`.

The latter identity was documented as necessary for Python 3.6 compatibility. The diagnostic gate retained resource-candidate detection and the existing context-manager exemption, adding the new helper as an alternative exemption.

The regression was added at historical path `tests/functional/c/consider/consider_using_with.py`, in `test_suppress_in_exit_stack`:

```python
with contextlib.ExitStack() as stack:
    _ = stack.enter_context(
        open("/sys/firmware/devicetree/base/hwid,location", "r")
    )  # must not trigger
```

This is a static-analysis fixture; checking it does not require executing its firmware-file access. Nearby existing `subprocess.Popen` assertions preserve a warning for unmanaged allocation and no warning for direct `with` use.

Historical `ChangeLog` and `doc/whatsnew/2.9.rst` entries described the false-positive correction; `ChangeLog` included `Closes #4654`. Current Actions use semantic owners, not these historical paths.

The implementation recognizes registration-method identity; it does not establish that every inferred ExitStack instance is eventually closed. Its scope is narrower than complete resource-lifetime analysis.

## Validation-only qualification audit

The complete supplied qualification report was inspected separately from historical mechanism evidence. It pins:
- Base: `c02682670e0d267d9e055347f3c9043f2550e205`.
- Fixed revision: `c2d03c6b3881a9df7353432b109523984adf06f9`.
- Issue: `pylint-dev/pylint:4654`.
- Fix: `pylint-dev/pylint:pr:4665`.
- Direct closure relationship, with supplied verified issue relationship and historical artifact identity.
- Validation time: `2026-10-04T11:00:42.115808+00:00`, not a historical availability date.

The report selected 17 public functional cases. Original base passed all 17. Base with the committed regression failed only `tests.test_functional::test_functional[consider_using_with]`, with an unexpected `consider-using-with` diagnostic at line 163; the other 16 passed. Historical fixed passed all 17. Exit codes were 0, 1, and 0, respectively; none timed out.

All three runs reported runtime SHA-256 `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, consistent command selection, adopted workspaces, and matching isolation mode. The report's observation digest was `f778f31db2757cfb5ac85c91d17ee61efb8705c6dc2c832c21b3c2897d2ef713`.

The target case belongs to both the original-to-fixed pass-to-pass set and regression-added fail-to-pass set because these compare different controls. The reported qualification scope is changed-test-files with original-base control; whole-project regression was not checked and no formal SWE run was claimed.

These supplied validation observations support source qualification only. They are not historical CI observations, newly learned historical mechanisms, or execution results for the authored Skill functional definitions.
