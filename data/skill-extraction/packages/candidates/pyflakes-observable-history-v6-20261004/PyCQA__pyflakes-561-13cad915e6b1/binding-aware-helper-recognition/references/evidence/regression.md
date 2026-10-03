# Regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:561:regression",
  "source_id": "PyCQA/pyflakes:561:repair:13cad915e6b1",
  "available_at": "2021-10-05T22:44:29Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied pyflakes/test/test_type_annotations.py diff adds test_aliased_import, documented as detecting when typing is imported as another name. Its self.flakes snippet imports typing as t, declares two @t.overload versions of f with type comments (None) -> None and (int) -> int, then defines f(s) returning s. No expected diagnostics are passed. This is a regression assertion available at the historical repair revision; historical execution status is unknown from the supplied diff."
}
```
