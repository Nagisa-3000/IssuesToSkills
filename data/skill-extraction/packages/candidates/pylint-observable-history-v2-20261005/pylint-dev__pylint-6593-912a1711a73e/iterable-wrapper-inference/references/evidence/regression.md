# Committed regression assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6593:regression",
  "source_id": "pylint-dev/pylint:6593:repair:912a1711a73e",
  "available_at": "2022-05-13T14:07:05Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff adds `use_enumerate()` to tests/functional/u/undefined/undefined_loop_variable.py. Its body is `for i, num in enumerate(range(3)): pass` followed by `print(i, num)`, with no expected undefined-loop-variable annotation for that read. This supplies the functional regression assertion at the historical commit. It does not provide a historical test-execution log; historical execution remains unknown."
}
```
