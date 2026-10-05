# Historical episode

Authoritative SourceRecord ID: `pylint-dev/pylint:5200:repair:8c7e2fae6fee`.

## Report

The [title](evidence/title.md) was “Wrong ternary suggested.” The [body](evidence/body.md) supplied:

```python
a = True
b = False
c = True
x = (a and b) or c
print(x)             # True
print(b if a else c)  # False
```

The reported command was `pylint test.py`. The output reported `R1706: Consider using ternary (b if a else c) (consider-using-ternary)` at line 6. The reporter listed Pylint 2.11.1, astroid 2.8.0, Python 3.9.7, and Fedora 34.

## Implementation and committed assertions

The [merged implementation](evidence/fix.md), available at `2021-10-29T19:44:19Z`, changed `pylint/checkers/refactoring/refactoring_checker.py`:

```python
inferred_truth_value = utils.safe_infer(truth_value)
if inferred_truth_value is None or inferred_truth_value == astroid.Uninferable:
    truth_boolean_value = True
else:
    truth_boolean_value = inferred_truth_value.bool_value()
```

Previously, the guard used membership in `(None, astroid.Uninferable)` and the final line called `truth_value.bool_value()`. The existing branch for `truth_boolean_value is False` selected `simplify-boolean-expression`. The ChangeLog and release notes state a fix when the condition can be inferred as False and close issue #5200.

The [regression assertions](evidence/regression.md) added `func5` in `tests/functional/t/ternary.py`, assigning `falsy_value = False` and returning `condition and falsy_value or false_value`. The expected-output addition in `tests/functional/t/ternary.txt` requires `simplify-boolean-expression` at line 39, with “Boolean expression may be simplified to false_value.” The adjacent existing `func4`, assigning `truth_value = 42`, retains `consider-using-ternary` at line 33.

These paths identify historical artifacts only. Locate current semantic owners before applying the [Workflow](workflow.md). Committed assertions are not evidence of historical execution; historical CI and test execution status remain unknown.

## Validation-only qualification audit

The supplied independent qualification report was inspected across all three controls. It pins original base `e8713873813bfab5fafb04b0fb8b5221011faa41`, fixed revision `8c7e2fae6fee28944764e643e65e729a58a5473c`, PR 5227, and issue 5200. The report verifies the historical artifact, direct closure relationship, and consistent runtime hash `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70` across controls.

At validation time `2026-10-04T11:59:31.691091+00:00`:

- Original base: exit 0, 12 passed, 1 skipped.
- Base with the committed regression: exit 1, 11 passed, 1 failed, 1 skipped. The ternary fixture expected `simplify-boolean-expression` at line 39 but received `consider-using-ternary`.
- Historical fixed: exit 0, 12 passed, 1 skipped.

The three observations include the same selected fixtures: `consider_ternary_expression`, `ternary`, `test_compile`, `tokenize_error`, `tokenize_error_jython`, `trailing_comma_tuple`, `trailing_newlines`, `trailing_whitespaces`, `try_except_raise`, `try_except_raise_crash`, `typedDict`, `typing_generic`, and `typing_use`. `tokenize_error_jython` was skipped in every control. The twelve pass-to-pass observations compare original-base and fixed behavior; one fail-to-pass observation compares the regression-bearing base and fixed ternary fixture. No control timed out, and each used the same reported runtime.

Qualification scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; cross-project transfer is unsupported. This was not a formal SWE run and did not execute newly authored Skill cases.

The report's closure event reference and replay details are validation-only context, not additional historical evidence cards. The report hash and observation hash are preserved in [provenance](provenance.json). Nothing in this audit backdates contemporary validation into historical knowledge.
