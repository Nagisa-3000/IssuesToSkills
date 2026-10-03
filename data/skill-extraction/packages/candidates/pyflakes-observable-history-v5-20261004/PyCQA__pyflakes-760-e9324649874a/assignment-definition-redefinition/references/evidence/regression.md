# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:760:regression",
  "source_id": "PyCQA/pyflakes:760:repair:e9324649874a",
  "available_at": "2023-01-12T16:26:28Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_other.py added test_redefined_function_shadows_variable. It passes the source x = 1 followed by def x(): pass to self.flakes with expected m.RedefinedWhileUnused. This is a module-level assignment-to-function regression assertion available at the historical commit. Historical execution is unknown from the supplied entry; it supplies no test-run log and no dedicated class-body regression assertion."
}
```
