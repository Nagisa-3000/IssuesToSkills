# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8735:regression",
  "source_id": "pylint-dev/pylint:8735:repair:33d3f22b767e",
  "available_at": "2023-06-06T18:57:38Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed regression appended 'nonlocal APPLE  # [nonlocal-without-binding]' and 'APPLE = 42' at module level in tests/functional/n/nonlocal_without_binding.py. The paired expected-output file added 'nonlocal-without-binding:74:0:74:14::nonlocal name APPLE found without binding:HIGH'. Existing assertions were retained. These are historical committed assertions, not proof of historical test execution; contemporaneous CI/test execution is unknown."
}
```
