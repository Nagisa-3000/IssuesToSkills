# Added undefined-name assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:728:regression",
  "source_id": "PyCQA/pyflakes:728:repair:4dcd92e45efe",
  "available_at": "2022-09-08T22:10:17Z",
  "kind": "historical_regression_assertions",
  "observation": "Historical pyflakes/test/test_type_annotations.py added TestTypeAnnotations.test_variable_annotation_references_self_name_undefined. It called self.flakes with a multiline source containing `x: int = x` and expected `m.UndefinedName`. This is a regression assertion available at the repair commit. The supplied historical record does not include its execution result; historical execution status is unknown."
}
```
