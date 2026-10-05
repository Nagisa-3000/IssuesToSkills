# Committed regression assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7319:regression",
  "source_id": "pylint-dev/pylint:7319:repair:7fdf8d9ee090",
  "available_at": "2022-08-21T14:02:23Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff appended CustomError(Exception) with __init__(self, message=\"default\") calling super().__init__(message) to tests/functional/u/useless/useless_parent_delegation.py. No expected useless-parent-delegation diagnostic annotation was added for this constructor. This is a regression assertion available at the historical repair commit; historical test execution is unknown. Contemporary qualification is separate validation provenance."
}
```
