# Historical episode

SourceRecord: `pylint-dev/pylint:7626:repair:00b6aa8482f0`.

The report concerned Pylint 2.15.4 with astroid 2.12.11. Two flags started as `False` and were changed to `True` in different loop branches. The expression `(flag_a and flag_b) or returns_false()` received a suggestion to simplify it to `returns_false()`, although the supplied program returned `True`. Removing the final `or returns_false()` removed the reported diagnostic.

The merged repair at `00b6aa8482f007090c7b5224cf8e2ac42f34eec6` added keyword-only `compare_constants=False` to `safe_infer` in historical `pylint/checkers/utils.py`. When enabled, unequal inferred `nodes.Const` values are ambiguous even if their inferred types agree. Existing type ambiguity handling remained in place.

The historical consumer in `pylint/checkers/refactoring/refactoring_checker.py` called `safe_infer(truth_value, compare_constants=True)`. It returned without a diagnostic if inference yielded `None` or `astroid.Uninferable`, instead of treating uncertainty as truthy. Remaining emitted messages used `confidence=INFERENCE`.

Historical `tests/functional/t/ternary.py` introduced definite `TRUE_VALUE` and `FALSE_VALUE` controls, unknown `maybe_true`/`maybe_false` operands, and a loop-reassignment regression. `ternary.txt` retained expected definite-value diagnostics and changed their confidence to `INFERENCE`. These are committed assertions, not proof of historical execution.

## Qualification audit, not historical mechanism evidence

The supplied independent qualification pinned original base
`88cfb80ccc695dbb717ad3d54af2e3bae9c3af5d`, the above merge revision, issue `7626`, and pull request `7627`. It reported verified direct closure. The original-base, base-with-regression, and historical-fixed runs used the same runtime digest and the same selected public test command.

Original base: 17 passed, 1 skipped.
Base with regression: 16 passed, 1 skipped, 1 failed; `ternary` failed with extra `consider-using-ternary` and `simplify-boolean-expression` diagnostics.
Historical fixed: 17 passed, 1 skipped.
All three runs completed without timeout; exit codes were 0, 1, and 0 respectively.

The failing regression thus distinguished the supplied historical base and repair within the stated scope. The report's pass-to-pass list has 17 entries, including the original `ternary` behavior; this does not mean 17 additional independent regression tests.

Qualification occurred at `2026-10-04T16:10:59.527984+00:00`. It is validation-only and must not be backdated into historical knowledge. Its scope is exactly `changed-test-files-with-original-base-control`. Its supplied limits are exactly: “Changed test files only; whole-project regression and cross-project transfer are untested.”

The original historical CI/test-execution status remains unknown. No newly authored Skill functional case was executed.

## Resources

- [Title evidence](evidence/title.md)
- [Report evidence](evidence/body.md)
- [Implementation evidence](evidence/fix.md)
- [Regression evidence](evidence/regression.md)
- [Workflow](workflow.md)
- [Provenance](provenance.json)
