# Added regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:617:regression",
  "source_id": "PyCQA/pyflakes:617:repair:3de8e6120291",
  "available_at": "2021-03-24T16:30:05Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff in pyflakes/test/test_type_annotations.py adds test_annotating_an_import guarded by @skipIf(version_info < (3, 6), 'new in Python 3.6'). It calls self.flakes on three statements: from a import b, c; b: c; print(b), with no expected diagnostic arguments. This is a historical no-diagnostics regression assertion. Historical execution status is not supplied; this package does not claim it ran that test."
}
```
