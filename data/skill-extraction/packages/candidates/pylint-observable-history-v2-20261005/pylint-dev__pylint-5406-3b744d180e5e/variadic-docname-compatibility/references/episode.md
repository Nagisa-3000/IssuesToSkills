# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:5406:repair:3b744d180e5e`.

The [title](evidence/title.md) labels a v2.12 regression. The [report](evidence/body.md) enables `pylint.extensions.docparams` and describes a function declaring `*args`. Sphinx-style `:param args:` produced missing and differing parameter diagnostics. Unescaped `:param *args:` avoided the checker diagnostics but produced a Sphinx emphasis warning. Escaped notation in a non-raw Python string produced a separate anomalous-backslash warning.

The [merged implementation](evidence/fix.md) repaired both style-specific extraction and signature/documentation comparison. Historical owners were `pylint/extensions/_check_docs_utils.py` and `pylint/extensions/docparams.py`. Historical regression fixtures were under `tests/functional/ext/docparams/parameter/`, including the Google, NumPy, and Sphinx required-parameter fixtures. These are historical locators only.

The [committed assertions](evidence/regression.md) add bare `kwargs` for Google and NumPy, bare `args` and `kwargs` for Sphinx, and escaped `*args` for Google. Existing genuine missing-parameter expectations remain. Changelog closure of #5815 is not a second independent source in this package.

The authored Workflow describes the evidenced mechanism and semantic prerequisites, not an assertion about the historical author's exact work sequence. Historical CI execution is unknown.

## Validation-only qualification

The supplied independent report pins original base `ba08c9d1ab8b624b4491a29bfc2f274dc00eeab8`, fixed revision `3b744d180e5ee7add0553780d0a92b5f87f14f6f`, repair identity, and direct closure. All three runs have the same runtime digest and no timeout.

Original base passed 11 selected tests. Base with regression assertions failed the Google, NumPy, and Sphinx fixtures and passed eight. Historical fixed code passed 11. The report's 11 pass-to-pass entries compare original-base tests with fixed tests; the three fail-to-pass entries compare base-with-regression with fixed tests. These are not disjoint populations.

The report was checked in 2026; this is validation time, not historical knowledge available in 2022. Its scope is changed test files with original-base controls, not whole-project regression, cross-project transfer, or a formal SWE run. No authored Skill evaluation has executed.
