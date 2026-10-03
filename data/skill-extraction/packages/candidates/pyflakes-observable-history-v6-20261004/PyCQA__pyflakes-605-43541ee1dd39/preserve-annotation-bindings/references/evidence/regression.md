# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:605:regression",
  "source_id": "PyCQA/pyflakes:605:repair:43541ee1dd39",
  "available_at": "2021-01-05T16:04:39Z",
  "kind": "historical_regression_assertions",
  "observation": "In pyflakes/test/test_type_annotations.py, TestTypeAnnotations gained test_type_annotation_clobbers_all, decorated with @skipIf(version_info < (3, 6), 'new in Python 3.6'). It calls self.flakes with imports of TYPE_CHECKING, List, and z, a not TYPE_CHECKING branch assigning __all__ = (\"z\",), and an else branch declaring __all__: List[str]. No expected diagnostics are passed. This assertion was available at the repair commit; historical execution status is unknown from the supplied evidence."
}
```
