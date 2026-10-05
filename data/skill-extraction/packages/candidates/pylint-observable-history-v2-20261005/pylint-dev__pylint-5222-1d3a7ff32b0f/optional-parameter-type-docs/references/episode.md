# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:5222:repair:1d3a7ff32b0f`.

The [title](evidence/title.md) and [report](evidence/body.md) describe a false `missing-param-doc` diagnostic for a NumPy-style parameter without `: type`. Both function parameters have Python annotations; only the second omits an inline docstring type. The report also complains about `missing-return-type-doc`, but the supplied repair does not establish a separate return-type mechanism.

Historical locators:

- `pylint/extensions/_check_docs_utils.py`: `NumpyDocstring.re_param_line` and added `NumpyDocstring.match_param_docs`.
- `tests/extensions/test_check_docs.py`: `TestParamDocChecker.test_finds_args_without_type_numpy`.
- `ChangeLog` and `doc/whatsnew/2.12.rst`: notes closing issue 5222.

The [implementation](evidence/fix.md) accepts colon or newline after an optionally starred identifier, adjusts optional type capture, and introduces separate documentation/type set collection for ordinary and keyword parameter sections. The supplied diff also includes a debug print and uses the delimiter capture as the description value in its description-only branch. These details constrain what the historical evidence establishes.

The [regression](evidence/regression.md) mixes an explicitly typed entry, an annotated description-only entry, an unannotated description-only entry, and `*args :` with a description. Its exact expectation is only `missing-type-doc` for `untyped_arg`. Assertions are known; original execution is unknown.

## Validation-only qualification audit

The supplied independent report pins base `76a7553066130a7dbf4d10922b2530161b2ec5b0` and fixed revision `1d3a7ff32b0f6d819b17ce18345502fbc47b48c9`, verifies the issue/fix identity and direct closure, and supplies all three controls:

- Original base: exit 0, 126 tests passed.
- Base with committed regression: exit 1, 125 passed and the targeted test failed. Actual diagnostics included erroneous `missing-param-doc` for `typed_arg, untyped_arg` in addition to the legitimate `missing-type-doc`.
- Historical fixed: exit 0, 126 passed.

All controls share the supplied runtime digest, did not time out, and used the changed test file. The aggregate pass-to-pass list includes the changed test's original version; it is not evidence of 126 distinct unchanged regressions.

Qualification was checked on 2026-10-04. This is validation time, never historical availability or new Skill execution. Whole-project regression, cross-project transfer, and formal SWE acceptance were not tested. Hashes and audit identity are retained in [provenance](provenance.json).
