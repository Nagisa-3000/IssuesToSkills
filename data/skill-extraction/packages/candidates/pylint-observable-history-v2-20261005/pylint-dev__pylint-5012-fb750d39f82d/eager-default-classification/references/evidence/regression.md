# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5012:regression",
  "source_id": "pylint-dev/pylint:5012:repair:fb750d39f82d",
  "available_at": "2021-09-20T20:11:44Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff added `good_case_issue_5012` to `tests/functional/c/cellvar_escaping_loop.py`. Inside a loop it defines functions with `(*, _i=i)` and `(_i=i)`, whose bodies print `_i`, appends both to a list, and returns the list. The companion expected-output file adds no warning for this good case and retains 13 existing loop-cell warnings with their line numbers increased by 16. These are committed assertions available at the fix revision; the supplied historical evidence does not establish their CI execution."
}
```
