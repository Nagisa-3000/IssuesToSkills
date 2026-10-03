# Ordinary decorator regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:422:regression",
  "source_id": "PyCQA/pyflakes:422:repair:2c29431eaeb9",
  "available_at": "2019-01-31T14:09:20Z",
  "kind": "historical_regression_assertions",
  "observation": "Historical pyflakes/test/test_type_annotations.py added test_not_a_typing_overload with the docstring \"regression test for @typing.overload detection bug in 2.1.0\". It assigns x = lambda f: f, defines t under @x, assigns y = lambda f: f, then defines t twice more under stacked @x and @y. self.flakes receives exactly two m.RedefinedWhileUnused expectations. These are assertions available at the historical commit, not supplied evidence of a historical test run."
}
```
