# Committed regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:regression",
  "source_id": "PyCQA/pyflakes:674:repair:1fae3dea5108",
  "available_at": "2022-02-12T14:52:33Z",
  "kind": "historical_regression_assertions",
  "observation": "In pyflakes/test/test_imports.py, TestSpecialAll gained test_ignored_when_not_directly_assigned. It calls self.flakes on import bar followed by (__all__,) = (\"foo\",), with m.UnusedImport as the expected diagnostic. The assertion protects ordinary unused-import behavior for indirect __all__ assignment; successful evaluation would also exclude an analyzer exception. The evidence supplies a committed assertion, not a historical passing-run log. Historical execution status is unknown."
}
```
