# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:regression",
  "source_id": "PyCQA/pyflakes:674:repair:1fae3dea5108",
  "available_at": "2022-02-12T14:52:33Z",
  "kind": "historical_regression_assertions",
  "observation": "In pyflakes/test/test_imports.py, TestSpecialAll gained `test_ignored_when_not_directly_assigned`, calling `self.flakes` on `import bar` followed by `(__all__,) = (\"foo\",)` with expected diagnostic `m.UnusedImport`. Nearby supplied context includes a direct `__all__ = [\"bar\"]` assertion and a warning-suppression test description for an imported name listed in __all__. These are assertions available at the historical commit; no historical execution transcript is supplied."
}
```
