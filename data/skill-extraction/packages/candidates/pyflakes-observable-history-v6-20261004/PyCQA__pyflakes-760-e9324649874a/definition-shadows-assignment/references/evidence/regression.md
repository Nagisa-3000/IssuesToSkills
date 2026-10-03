# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:760:regression",
  "source_id": "PyCQA/pyflakes:760:repair:e9324649874a",
  "available_at": "2023-01-12T16:26:28Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_other.py adds test_redefined_function_shadows_variable. It calls self.flakes on `x = 1` followed by `def x(): pass`, expecting m.RedefinedWhileUnused. This is a module-level regression assertion available at the historical repair commit. The supplied core does not include a historical test-run command or result, so historical execution status is unknown."
}
```
