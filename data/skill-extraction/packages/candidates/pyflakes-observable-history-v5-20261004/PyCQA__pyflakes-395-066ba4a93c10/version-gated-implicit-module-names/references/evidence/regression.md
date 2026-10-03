# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:395:regression",
  "source_id": "PyCQA/pyflakes:395:repair:066ba4a93c10",
  "available_at": "2019-01-01T13:10:34Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_undefined_names.py added test_moduleAnnotations with `@skipIf(version_info < (3, 6), 'new feature in 3.6')`. The docstring states that module-scope __annotations__ should not emit an undefined-name warning when the version is greater than or equal to 3.6. The assertion is `self.flakes('__annotations__')`, a bare module-level reference. These assertions were available at the historical commit; the supplied evidence contains no historical execution log, so historical execution status is unknown."
}
```
