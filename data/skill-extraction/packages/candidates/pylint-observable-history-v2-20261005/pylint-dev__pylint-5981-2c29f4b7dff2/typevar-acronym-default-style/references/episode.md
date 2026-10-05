# Historical episode

SourceRecord ID: `pylint-dev/pylint:5981:repair:2c29f4b7dff2`.

The reporter described Pylint 2.13.0 rejecting `HVACModeT` and `IPAddressT` with C0103 `invalid-name`, and requested acceptance of initial uppercase abbreviations.

The merged repair at `2c29f4b7dff26730a067f135ee18f7a3c18263e3`, available at `2022-03-26T09:00:28Z`, changed the default TypeVar expression in the historical owner `pylint/checkers/base/name_checker/checker.py`.

The mixed-case branch changed from:

```python
(?:[^\W\da-z_][^\WA-Z_]+)+T?(?<!Type)
```

to:

```python
(?:[^\W\da-z_]+[^\WA-Z_]+)+T?(?<!Type)
```

The added `+` permits uppercase runs. The surrounding branches, Unicode-aware character classes, leading underscore allowance, optional terminal `T`, `Type` exclusion, and variance suffix syntax remain unchanged.

The historical fixture `tests/functional/t/typevar_naming_style_default.py` adds accepted `HVACModeT` and `_IPAddress` and rejected `IPAddressU`. Its companion `.txt` file updates diagnostic positions and retains existing negative and variance assertions. `doc/user_guide/options.rst` adds `IPAddressT` as a good example. The changelog describes the relaxation and closes #5981.

These are historical paths, not automatic current bindings.

## Evidence

- [Title](evidence/title.md)
- [Original report](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertions](evidence/regression.md)

Committed assertions are historical evidence; original CI/test execution is unknown. The authored locate, repair, and validate contracts reconstruct the supported mechanism and its verification obligations; they do not establish that newly authored operations were executed historically.

## Validation-only qualification review

The supplied independent report was checked at `2026-10-04T13:42:32.713653+00:00`. This is validation time, not historical learned-content availability.

Identity and closure agree with the authoritative source:
- original base: `8d21ab212789b5e11417bbb3486546f06c33cb0c`;
- repaired revision: `2c29f4b7dff26730a067f135ee18f7a3c18263e3`;
- issue: `pylint-dev/pylint:5981`;
- fix: `pylint-dev/pylint:pr:5983`;
- repair availability: `2022-03-26T09:00:28Z`;
- relationship: verified direct closure.

The supplied closure locator `pylint-dev/pylint:5981:event:CE_lADOAtdnV85GaJJczwAAAAF4L92n` is qualification metadata, not an added historical evidence card.

The complete supplied controls show:
- **Original base:** exit 0; 15 passed, 1 skipped.
- **Base with committed regressions:** exit 1; 14 passed, 1 skipped. The default TypeVar naming case failed with unexpected `invalid-name` diagnostics at fixture lines 33 and 34.
- **Historical fixed revision:** exit 0; 15 passed, 1 skipped.

All three controls use the same selected functional-test invocation and runtime digest, report adopted workspaces, and report no timeout. The Jython tokenize-error case is skipped throughout. Per-case observations retain the neighboring ternary, compilation, tokenize, whitespace, exception, TypedDict, custom TypeVar expression, incorrect variance, generic typing, and typing-use results. Only the default TypeVar naming case changes from failure with the committed regressions to passing at the fixed revision.

The report's 15 pass-to-pass identities compare original base against fixed revision; they do not mean all 15 passed in the base-with-regression control.

Runtime digest: `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

Observation digest: `b0d4b948e216546ed08935b0156c1fd290679617e07a58f849013c63d6be2b93`.

Authoritative report hash: `7383db5f8aa1b2586b6e3b059aa87c4d240f23c5278f8b6c06145ff590a2a198`.

Scope: `changed-test-files-with-original-base-control`. The report is not a formal SWE run. Whole-project regression and cross-project transfer were not checked. Contemporary runtime, isolation, and log details are validation-only, not historical repair mechanisms. This qualification does not execute the newly authored functional evaluations.
