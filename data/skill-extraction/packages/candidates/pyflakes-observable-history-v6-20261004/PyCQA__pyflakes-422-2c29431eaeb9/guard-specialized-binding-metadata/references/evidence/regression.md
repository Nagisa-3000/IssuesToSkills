# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:422:regression",
  "source_id": "PyCQA/pyflakes:422:repair:2c29431eaeb9",
  "available_at": "2019-01-31T14:09:20Z",
  "kind": "historical_regression_assertions",
  "observation": "Historical pyflakes/test/test_type_annotations.py added test_not_a_typing_overload, described as a regression for @typing.overload detection in 2.1.0. The snippet assigns x = lambda f: f, defines t under @x, assigns y = lambda f: f, and redefines t twice under stacked @x and @y. self.flakes expects m.RedefinedWhileUnused twice. These are assertions available at the repair commit; the supplied entry contains no historical execution transcript."
}
```
