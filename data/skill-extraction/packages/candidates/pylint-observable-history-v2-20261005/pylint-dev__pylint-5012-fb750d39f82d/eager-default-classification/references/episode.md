# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:5012:repair:fb750d39f82d`.

The report compared two functions defined inside a loop. `def f(*, _i=i)` received W0640 at its default expression; `def g(_i=i)` did not. Both bodies printed `_i`. Defaults evaluate when the function is defined, so these references are eager capture rather than late-bound body capture.

The historical semantic owner was `is_default_argument` in `pylint/checkers/utils.py`. Its FunctionDef/Lambda branch searched only `scope.args.defaults`. The repair combined positional defaults with non-None entries from `scope.args.kw_defaults`, recursively traversed name descendants, and retained `default_name_node is node`.

The historical regression owner was `tests/functional/c/cellvar_escaping_loop.py`, with expected diagnostics in the companion `.txt` file. The added good case appended keyword-only and positional-default functions to a list and returned that list. Existing genuine closure warnings remained, with locations shifted by 16 lines.

The ChangeLog described the keyword-only parameter default false positive and stated closure of #5012. Supplied historical material contains implementation and committed assertions, not historical CI execution results.

## Evidence

- [Issue title](evidence/title.md)
- [Original reproduction](evidence/body.md)
- [Merged implementation](evidence/fix.md)
- [Committed regression assertions](evidence/regression.md)

## Qualification inspection: validation only

The supplied independent report has schema `historical-causal-verification-v1` and was checked at `2026-10-04T11:47:00.792006+00:00`. Its identity pins:

- issue: `pylint-dev/pylint:5012`;
- fix: `pylint-dev/pylint:pr:5045`;
- original base: `24cbf8c33120db595c3dd9443418e1b8472839fd`;
- fixed revision: `fb750d39f82dd58342a7683ac5e03b38ba64ae4a`;
- repair availability: `2021-09-20T20:11:44Z`;
- resolution relationship: verified direct closure;
- closure locator: `pylint-dev/pylint:5012:event:CE_lADOAtdnV847a5KrzwAAAAE9u_gy`.

The closure locator is validation metadata, not an additional historical evidence card.

Report hash: `0797398d6d7026fc2b072cf12d0ec4177b90a3984a680b273a4f72bd1935bed9`.

Observations hash: `69e1b4e1aee56fb16482db1a6497ecf99f4d5dbfdfad44bf765663398e8971b0`.

All three controls used the same runtime digest, `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`, adopted workspaces, the same reported isolation, and no timeouts. Their argv used the same selected public functional tests, with a JUnit output path. These are contemporary replay conditions, not historical repair guidance.

| Functional case | Original base | Base with regression | Historical fixed |
|---|---|---|---|
| cached_property | passed | passed | passed |
| cellvar_escaping_loop | passed | failed | passed |
| class_attributes | passed | passed | passed |
| class_members | passed | passed | passed |
| class_members_py30 | passed | passed | passed |
| class_scope | passed | passed | passed |
| class_variable_slots_conflict_exempted | passed | passed | passed |
| classes_meth_could_be_a_function | passed | passed | passed |
| classes_protected_member_access | passed | passed | passed |
| comparison_with_callable | passed | passed | passed |
| condition_evals_to_constant | passed | passed | passed |
| confidence_filter | passed | passed | passed |
| confusing_with_statement | passed | passed | passed |
| continue_in_finally | skipped | skipped | skipped |
| control_pragmas | passed | passed | passed |
| crash_missing_module_type | passed | passed | passed |
| ctor_arguments | passed | passed | passed |
| genexp_in_class_scope | passed | passed | passed |

Original base exited 0 with 17 passed and 1 skipped. Base with regression exited 1 with 16 passed, 1 failed, and 1 skipped; its failure reported an unexpected `cell-var-from-loop` at line 102. Historical fixed exited 0 with 17 passed and 1 skipped. Each run reported 538 deselected and 9 warnings.

The report's fail-to-pass set contains the loop regression. Its 17 original-base-to-fixed pass-to-pass entries include that loop test. The skip is not a passing assurance.

The report verifies artifact identity and resolution within `changed-test-files-with-original-base-control`. It explicitly records that whole-project regression was not checked and that this was not a formal SWE run. It establishes neither cross-project transfer nor execution of the newly authored Skill evals. Contemporary validation does not backdate knowledge; historical CI execution remains unknown.
