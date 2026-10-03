# Added interaction regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:764:regression",
  "source_id": "PyCQA/pyflakes:764:repair:e19886e58363",
  "available_at": "2023-01-31T18:45:58Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff in pyflakes/test/test_type_annotations.py added test_unused_annotation_in_outer_scope_reassigned_in_local_scope. Its self.flakes input was `x: int`, `x.__dict__`, and `def f(): x = 1`; expected message classes were m.UndefinedName and m.UnusedVariable. These assertions were available at the historical repair commit. Their historical execution status is unknown from the supplied core evidence; later changed-test-only qualification is recorded separately in provenance."
}
```
