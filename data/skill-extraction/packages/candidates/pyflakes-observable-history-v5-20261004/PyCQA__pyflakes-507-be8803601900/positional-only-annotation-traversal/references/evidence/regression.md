# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:507:regression",
  "source_id": "PyCQA/pyflakes:507:repair:be8803601900",
  "available_at": "2020-01-17T20:24:48Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff in pyflakes/test/test_type_annotations.py added `test_positional_only_argument_annotations`, decorated with `@skipIf(version_info < (3, 8), 'new in Python 3.8')`. It invoked `self.flakes` on `from x import C` followed by `def f(c: C, /): ...`, with no expected diagnostic arguments. This records the no-diagnostic regression assertion available at the historical commit. Historical execution status is not supplied."
}
```
