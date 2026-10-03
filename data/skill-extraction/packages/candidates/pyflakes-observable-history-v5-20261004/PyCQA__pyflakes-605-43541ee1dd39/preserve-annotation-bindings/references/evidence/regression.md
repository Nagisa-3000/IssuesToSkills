# Regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:605:regression",
  "source_id": "PyCQA/pyflakes:605:repair:43541ee1dd39",
  "available_at": "2021-01-05T16:04:39Z",
  "kind": "historical_regression_assertions",
  "observation": "Historical pyflakes/test/test_type_annotations.py gained test_type_annotation_clobbers_all with @skipIf(version_info < (3, 6), 'new in Python 3.6'). It calls self.flakes on imports of TYPE_CHECKING, List, and z, the assigned __all__ = (\"z\",) in the not TYPE_CHECKING branch, and annotation-only __all__: List[str] in the else branch, with no expected diagnostics supplied. This is a regression assertion available at the repair commit; historical execution results are unknown because no execution log is supplied."
}
```
