# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:764:regression",
  "source_id": "PyCQA/pyflakes:764:repair:e19886e58363",
  "available_at": "2023-01-31T18:45:58Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff added TestTypeAnnotations.test_unused_annotation_in_outer_scope_reassigned_in_local_scope in pyflakes/test/test_type_annotations.py. It called self.flakes on `x: int`, `x.__dict__`, and `def f(): x = 1`, expecting `m.UndefinedName` and `m.UnusedVariable`. This assertion was available at the historical commit. The supplied historical evidence does not include execution output, so historical test execution is unknown."
}
```
