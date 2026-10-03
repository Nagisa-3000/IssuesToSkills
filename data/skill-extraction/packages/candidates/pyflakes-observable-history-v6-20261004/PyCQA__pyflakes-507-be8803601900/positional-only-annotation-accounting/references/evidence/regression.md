# Committed focused assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:507:regression",
  "source_id": "PyCQA/pyflakes:507:repair:be8803601900",
  "available_at": "2020-01-17T20:24:48Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in pyflakes/test/test_type_annotations.py adds test_positional_only_argument_annotations with @skipIf(version_info < (3, 8), 'new in Python 3.8'). It calls self.flakes on source containing from x import C and def f(c: C, /): ... without an expected diagnostic argument, asserting no diagnostics. This is a committed assertion available at the repair commit. Historical execution status is unknown because no historical test-run log is supplied."
}
```
