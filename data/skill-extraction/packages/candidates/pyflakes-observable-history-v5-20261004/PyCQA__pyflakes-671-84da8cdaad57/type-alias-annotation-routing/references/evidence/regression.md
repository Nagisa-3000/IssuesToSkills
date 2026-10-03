# Added regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:regression",
  "source_id": "PyCQA/pyflakes:671:repair:84da8cdaad57",
  "available_at": "2022-02-13T16:32:09Z",
  "kind": "historical_regression_assertions",
  "observation": "The added `TestTypeAnnotations.test_TypeAlias_annotations` in pyflakes/test/test_type_annotations.py was skipped below Python 3.6. Using `from typing_extensions import TypeAlias` and `from foo import Bar`, it asserted no diagnostics for `bar: TypeAlias = Bar` and `bar: TypeAlias = 'Bar'`, both at module scope and inside class A. It also asserted no diagnostics for a value-less `bar: TypeAlias` with only the TypeAlias import. When an imported Bar was present but the alias still had no value, it expected `m.UnusedImport`. These are test assertions available at the historical commit; the supplied core evidence does not record their historical execution."
}
```
