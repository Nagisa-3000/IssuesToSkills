# Regression assertions at the historical commit

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:regression",
  "source_id": "PyCQA/pyflakes:671",
  "available_at": "2022-02-13T16:32:09Z",
  "kind": "historical_regression_assertions",
  "observation": "The pyflakes/test/test_type_annotations.py diff added test_TypeAlias_annotations with @skipIf(version_info < (3, 6), 'new in Python 3.6'). Using typing_extensions.TypeAlias and imported foo.Bar, self.flakes asserted no diagnostics for module-level and class-level aliases with Bar and 'Bar' values. It also asserted no diagnostics for bar: TypeAlias without a value, and m.UnusedImport when an otherwise unused imported Bar accompanied that no-value declaration. These six assertions were available at the merged commit; historical execution is unknown from the supplied evidence."
}
```
