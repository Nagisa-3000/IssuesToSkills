# Historical episode

Source: `pylint-dev/pylint:5557:repair:2a69387352bd`.

The original report compared a parameter to `typing.Any` and reported W0143, `comparison-with-callable`, using Pylint 2.12.2, astroid 2.9.0, and Python 3.10.0. No callable-comparison warning was expected. Missing-docstring messages were unrelated.

At revision `2a69387352bd1c941759faaa22458de3609b7627`, the diagnostic owner was `ComparisonChecker` in `pylint/checkers/base.py`. The repair replaced a bare-callable count comprehension with an explicit loop over the left operand and the first right operand. Each operand used `utils.safe_infer`. An inferred bare callable counted only if its decorator names lacked `typing._SpecialForm` and no immediate body element was a `nodes.Raise`. Emission still required exactly one eligible bare callable.

Committed assertions:
- `tests/functional/c/comparison_with_callable.py` added `eventually_raise`, which calls `print()` then raises `Exception`, and a comparison expected not to warn.
- `tests/functional/c/comparison_with_callable_typing_constants.py` added comparisons to `Any` and `Optional`, expected not to warn. Its comment explains that `Optional` raises through `typing._SpecialForm.__call__()` rather than its own body.

These assertions were available on 2021-12-21 at 13:58:16 UTC. Historical CI/test execution is unknown.

## Validation-only qualification audit

The supplied complete qualification report was inspected for identity, causal controls, direct closure, and runtime consistency. It pins:
- original base: `ca06014c8de155d76b1da7eebb4be877cba40007`;
- fix: `pylint-dev/pylint:pr:5563`;
- historical fixed revision: `2a69387352bd1c941759faaa22458de3609b7627`;
- checked at: `2026-10-04T12:44:57.817112+00:00`;
- report hash: `b40ca7e36aa470fc6cd1487b5f7daa4dd37c1efe8d69edb7b46ef4a3b04ce82e`;
- observation hash: `bd804731e23054ea86b07c8c0286632fdd5c1db5bcced1e6e573a9d698bf0a90`;
- common runtime hash: `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

The original-base control exited 0 with 18 passed and 1 skipped. The new typing fixture was absent. The original callable-comparison fixture passed.

The base with committed regressions exited 1 with 2 failed, 17 passed, and 1 skipped. Unexpected callable-comparison diagnostics appeared at the `Any` and `Optional` comparisons and the `eventually_raise` comparison.

The historical-fixed control exited 0 with 19 passed and 1 skipped. Both changed fixtures passed. All three runs used matching selected-test argv, the same runtime hash, and reported no timeout. `continue_in_finally` was skipped throughout. The report lists 2 fail-to-pass cases and 18 pass-to-pass cases; the existing callable-comparison fixture participates in both comparisons because its original assertions passed before new regressions were added.

The direct-closure relationship and historical artifact identity were reported verified. Its closure-event locator is validation metadata, not an additional historical evidence card.

Qualification scope is `changed-test-files-with-original-base-control`. Selected neighboring controls are not proof of whole-project regression safety. Whole-project checks and cross-project transfer were not performed. The later replay date is never backdated; replay runtime details do not define the historical mechanism. This qualification did not execute the newly authored Skill's functional cases.
