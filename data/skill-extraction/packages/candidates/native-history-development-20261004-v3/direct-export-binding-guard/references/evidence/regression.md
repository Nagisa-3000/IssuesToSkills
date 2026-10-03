# Regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:regression",
  "source_id": "PyCQA/pyflakes:674",
  "available_at": "2022-02-12T14:52:33Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff added TestSpecialAll.test_ignored_when_not_directly_assigned in pyflakes/test/test_imports.py. It called self.flakes with import bar and (__all__,) = (\"foo\",), expecting m.UnusedImport. This is an assertion of ordinary unused-import behavior for indirect __all__ binding available at the historical commit. No historical execution transcript is supplied; historical execution status is unknown."
}
```
