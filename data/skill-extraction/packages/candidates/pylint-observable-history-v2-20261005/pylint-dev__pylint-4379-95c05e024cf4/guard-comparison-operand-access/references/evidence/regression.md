# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4379:regression",
  "source_id": "pylint-dev/pylint:4379:repair:95c05e024cf4",
  "available_at": "2021-04-19T19:36:37Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff appends two cases to tests/functional/c/consider/consider_using_min_max_builtin.py: var = 1; if var == -1: var = None, and var2 = 1; if var2 in [1, 2]: var2 = None. They are committed functional regression inputs without min/max expectation annotations. The supplied historical evidence does not record execution or CI status; that status is unknown."
}
```
