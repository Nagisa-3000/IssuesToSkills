# Import, annotate, use assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:617:regression",
  "source_id": "PyCQA/pyflakes:617:repair:3de8e6120291",
  "available_at": "2021-03-24T16:30:05Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in pyflakes/test/test_type_annotations.py added test_annotating_an_import with `@skipIf(version_info < (3, 6), 'new in Python 3.6')`. It called self.flakes on `from a import b, c`, `b: c`, and `print(b)` without an expected diagnostic argument. This asserts no diagnostics for that sequence. Historical execution status is unknown from this entry; the later changed-test qualification is separately recorded in provenance."
}
```
