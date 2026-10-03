# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:regression",
  "source_id": "PyCQA/pyflakes:671:repair:84da8cdaad57",
  "available_at": "2022-02-13T16:32:09Z",
  "kind": "historical_regression_assertions",
  "observation": "The added test_TypeAlias_annotations in pyflakes/test/test_type_annotations.py was skipped for Python < 3.6. Using TypeAlias imported from typing_extensions and Bar imported from foo, it asserted no diagnostics for bar: TypeAlias = Bar and bar: TypeAlias = 'Bar' at module scope and inside class A. It also asserted no diagnostics for a valueless bar: TypeAlias declaration without Bar imported, and m.UnusedImport when Bar was imported but the alias declaration had no value. These are assertions available at the historical repair revision; historical execution results are not supplied."
}
```
