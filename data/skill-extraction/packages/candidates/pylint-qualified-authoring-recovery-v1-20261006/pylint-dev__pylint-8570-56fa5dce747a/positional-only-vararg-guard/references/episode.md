# Historical episode

Authoritative source: `pylint-dev/pylint:8570:repair:56fa5dce747a`.

The [report](evidence/body.md) demonstrated W1113 / `keyword-arg-before-vararg` for `def name(param1=True, /, *args): ...`. Because that parameter is positional-only, supplying it by keyword does not produce the keyword/positional collision motivating this diagnostic.

The [implementation](evidence/fix.md), published at revision `56fa5dce747a46f1dcba6eca003bb22fcc347247`, changed historical `pylint/checkers/typecheck.py`. Within `if node.args.vararg and node.args.defaults:`, it inserted a return when `node.args.posonlyargs` was nonempty and `node.args.args` was empty. The async visitor remained an alias of the ordinary visitor.

The [regression](evidence/regression.md) added:
- `tests/functional/k/keyword_arg_before_vararg_positional_only.py`
- `tests/functional/k/keyword_arg_before_vararg_positional_only.rc`
- `tests/functional/k/keyword_arg_before_vararg_positional_only.txt`

The fixture required Python 3.8 or newer and asserted warnings only for its three mixed signatures. Historical execution/CI status is unknown. The authored operations describe the repair's semantic dependencies, not a claim that this newly authored task plan was historically executed.

## Validation-only qualification audit

The supplied independent qualification report was checked at `2026-10-04T17:54:45.337117+00:00`, after the historical cutoff. Its complete controls pin:
- Original base: `0cd41b1fb15e31eb311b61f93bc27f7cacc2f7ac`.
- Fixed/merge revision: `56fa5dce747a46f1dcba6eca003bb22fcc347247`.
- Issue `pylint-dev/pylint:8570`, fix `pylint-dev/pylint:pr:8571`, direct closure.
- Repair availability `2023-04-13T06:46:51Z`.

The report verifies historical artifact identity and direct closure, citing validation-only relationship reference `pylint-dev/pylint:8570:event:CE_lADOAtdnV85jOcw_zwAAAAIYCiur`. This is not an additional packaged historical evidence ID.

Original-base control passed the existing `keyword_arg_before_vararg` test, exit 0. Base-with-regression passed that control but failed `keyword_arg_before_vararg_positional_only`, exit 1, with unexpected warnings on lines 10, 12, and 13. Historical-fixed passed both tests, exit 0. All runs used adopted isolated workspaces, reported no timeout, and shared runtime hash `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

The replay command was `python3 -m pytest tests/test_functional.py -k "__init__ or keyword_arg_before_vararg or keyword_arg_before_vararg_positional_only" -q`, with a JUnit output argument in the individual runs. This is validation-only replay metadata, not current execution guidance.

Exact scope: `changed-test-files-with-original-base-control`.

Exact limits: `Changed test files only; whole-project regression and cross-project transfer are untested.`

There was one fail-to-pass and one pass-to-pass test. Whole-project regression was not checked; this was not a formal SWE run. The replay establishes scoped source qualification, not newly executed Skill evals, pre-cutoff runtime knowledge, or broad transfer.
