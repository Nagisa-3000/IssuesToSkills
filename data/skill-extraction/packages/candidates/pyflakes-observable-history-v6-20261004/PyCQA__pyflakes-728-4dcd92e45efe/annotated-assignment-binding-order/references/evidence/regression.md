# Committed regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:728:regression",
  "source_id": "PyCQA/pyflakes:728:repair:4dcd92e45efe",
  "available_at": "2022-09-08T22:10:17Z",
  "kind": "historical_regression_assertions",
  "observation": "In pyflakes/test/test_type_annotations.py, TestTypeAnnotations added test_variable_annotation_references_self_name_undefined. It calls self.flakes with the source `x: int = x` and expected message class m.UndefinedName. This assertion was available at the historical commit; historical execution status is unknown from the supplied core evidence."
}
```
