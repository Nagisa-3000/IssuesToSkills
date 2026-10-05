# Historical episode and qualification boundary

SourceRecord: `pylint-dev/pylint:4291:repair:d0591ba2a097`.

## Historical mechanism

The [title](evidence/title.md) and [report](evidence/report.md) concern functional testing of configured badfunctions. The supplied configuration loads `pylint.extensions.bad_builtin` and sets `bad-functions=map,input,filter,print`. The reporter suspected that extension-loading code never executed. The report's plural `bad-builtins` annotations differ from the committed singular `bad-builtin` symbol.

The [implementation](evidence/implementation.md) changes `pylint/testutils/lint_module_test.py`. After `read_config_file(test_file.option_file)`, inside the existing `try`, it checks parser option `MASTER` / `load-plugins`, normalizes its value with `utils._splitstrip`, and calls `load_plugin_modules`. `load_config_file` follows. Existing `NoFileError` handling remains.

The [regressions](evidence/regressions.md) add `tests/functional/b/bad_builtins.py`, `.rc`, and `.txt`, asserting diagnostics for input, filter, map, and print. Changes to `tests/functional/f/fixture_docparams_missing.py` and its new `.txt` expectations cover missing return/yield documentation and types.

These paths identify historical artifacts only. The authored Workflow reconstructs the repair mechanism and public validation obligations; it does not claim its Actions were historically executed as an authored plan. Historical CI/test-execution status is unknown.

## Validation-only source qualification

The supplied complete controls pin original base `cd90e9ec218b4735c3406b757f48d4898a2aee5e`, fixed revision `d0591ba2a097312c41d544e4269eda5b809c47a0`, issue `pylint-dev/pylint:4291`, and fix `pylint-dev/pylint:pr:4332`. Historical artifact identity and direct closure were verified. Repair availability is `2021-04-09T19:13:14Z`, strictly before the exclusive cutoff.

Qualification was checked at `2026-10-04T10:38:40.560527+00:00`. The closure reference supplied in the validation report is `pylint-dev/pylint:4291:event:MDExOkNsb3NlZEV2ZW50NDU3NjAyNjUzMA==`; it is not an additional historical core evidence card.

| Control | Exit | Observations |
| --- | --- | --- |
| Original base | 0 | 29 passed, 1 skipped, 432 deselected |
| Base with committed regression changes | 1 | 2 failed, 28 passed, 1 skipped, 432 deselected |
| Historical fixed | 0 | 30 passed, 1 skipped, 432 deselected |

The new `bad_builtins` case is absent on original base. With committed regression changes on base, `bad_builtins` and `fixture_docparams_missing` fail because expected extension diagnostics are absent. Both pass on historical fixed. `bad_reversed_sequence_py37` is skipped in all controls; the other selected runnable neighbors remain passing.

The reported 29 pass-to-pass identities compare original base with historical fixed. They include `fixture_docparams_missing`, whose original expectations pass originally, strengthened expectations fail on base-with-regression, and strengthened expectations pass after the repair. The two fail-to-pass cases and 29 pass-to-pass identities therefore describe different comparisons.

All runs used adopted workspaces, reported no timeout, and had consistent isolation and runtime digest `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`. Observation digest: `af43c4fa23953ef5a596c8290a0f4441f8a2a410ea9f88a055a8d2d378a31611`. The exact authoritative qualification report hash is in [provenance](provenance.json).

Scope is `changed-test-files-with-original-base-control`. Whole-project regression was not checked; cross-project transfer is untested; this was not a formal SWE run. These later controls qualify the historical source only. They are not backdated historical knowledge, additional independent mechanism support, or results for the newly authored Skill evaluations.
