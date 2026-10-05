# Historical episode

Authoritative SourceRecord: `pylint-dev/pylint:6557:repair:5fcccc13f1f7`.

## Report, implementation, and assertion

The [title](evidence/title.md) reported an Attribute without `name`. The [body](evidence/body.md) supplied an `.items()` loop that assigns its item to an instance attribute and then accesses `my_dict[a.input_output[0]]`. Its traceback failed at `value.value.name` in dictionary-lookup refactoring analysis.

Historical implementation owner:
`pylint/checkers/refactoring/refactoring_checker.py`, method `_check_unnecessary_dict_index_lookup`.

Historical regression owner:
`tests/functional/u/unnecessary/unnecessary_dict_index_lookup.py`.

These paths are historical locators only. Current execution must bind equivalent semantic owners independently.

The [merged implementation](evidence/fix.md) inserted `or not isinstance(value.value, nodes.Name)` before the name comparison. It retained the existing AssignName target check and dictionary-expression comparison. Short-circuit evaluation excludes Attribute bases from the Name-specific branch before the unsafe field read.

The [committed regression](evidence/regression.md) assigns the iteration item to `f.input_output`, then analyzes `print(d[f.input_output[0]])`. It adds no unnecessary-dict-index-lookup expectation annotation to this case.

The repair and assertion became available at `2022-05-11T14:20:18Z`, strictly before the authoritative cutoff. Historical CI/test execution remains unknown. The authored [Workflow](workflow.md) states source-derived repair and validation obligations, not a newly observed historical execution.

## Validation-only qualification audit

The complete supplied controls, run observations, identity, closure relationship, and runtime consistency were inspected.

- Report schema: `historical-causal-verification-v1`.
- Issue: `pylint-dev/pylint:6557`.
- Fix: `pylint-dev/pylint:pr:6579`.
- Original base: `3721bef16691c25a7ad8a95a141253619bdccaa8`.
- Fixed revision: `5fcccc13f1f7eceb9d8dc8ea4c5595df30746d5c`.
- Repair availability: `2022-05-11T14:20:18Z`.
- Exclusive cutoff: `2024-01-01T00:00:00Z`.
- Resolution relationship: `direct_closure`.
- Closure locator in the validation report: `pylint-dev/pylint:6557:event:CE_lADOAtdnV85JRaL8zwAAAAGI2KdI`.

The report marks historical artifact and issue relationship verified. The closure locator is validation audit context, not an additional historical evidence card.

| Supplied control | Exit code | Observed result |
|---|---:|---|
| Original base with original assertions | 0 | 12 passed, 748 deselected |
| Base with added regression | 1 | Target dictionary-lookup fixture failed with the reported AttributeError; 11 others passed |
| Historical fixed code with regression | 0 | 12 passed, 748 deselected |

The regression-bearing base fails at the same inner-base `.name` comparison. All three runs report identical runtime hashes, consistent test selection and isolation, adopted workspaces, and no timeout. The original-base target fixture passed with original assertions; the regression-bearing target failed on base and passed on fixed code. Consequently the reported 12 pass-to-pass count includes the target under original assertions, while the fail-to-pass count of 1 concerns the added regression.

The replay selected unnecessary_comprehension, unnecessary_dict_index_lookup, unnecessary_direct_lambda_call, unnecessary_dunder_call, unnecessary_ellipsis, unnecessary_lambda, unnecessary_lambda_assignment, unnecessary_lambda_assignment_py38, unnecessary_list_index_lookup, unnecessary_list_index_lookup_py38, unnecessary_not, and unnecessary_pass. Its command used `python3 -m pytest tests/test_functional.py -k ... -q`; run argv also requested JUnit output. This later selection is audit context, not a historical mechanism or current execution binding.

- Checked at: `2026-10-04T14:29:33.893201+00:00`.
- Qualification report hash: `b14976a504e249fa4baef17aec906f62f06d3e11fe66910eb195eb93db96377d`.
- Observations hash: `546de8bc74b680d0858cdb33f784c8cd4045d7bdea2293797952b2613e5f93d3`.
- Runtime hash: `862d62a256e5167c238ee0e366b67c2bdaae0f003eb53900c745a1f90dcf7e70`.

Exact scope: `changed-test-files-with-original-base-control`.

Exact limits: “Changed test files only; whole-project regression and cross-project transfer are untested.”

`whole_project_regression_checked` and `formal_SWE_run` are false. Qualification does not backdate learned content, establish broader correctness, or execute the newly authored Skill functional cases.
