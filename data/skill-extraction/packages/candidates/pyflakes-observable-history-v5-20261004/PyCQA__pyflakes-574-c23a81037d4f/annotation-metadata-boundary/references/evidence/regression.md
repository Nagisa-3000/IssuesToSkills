# Regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:574:regression",
  "source_id": "PyCQA/pyflakes:574:repair:c23a81037d4f",
  "available_at": "2020-09-28T20:44:22Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_type_annotations.py adds four tests gated with skipIf(version_info < (3,), 'new in Python 3'). Using self.flakes, function parameters annotated Annotated['integer'] and Annotated['integer', 1] each expect m.UndefinedName; Annotated[int, '> 0'] expects no diagnostics; Union[Annotated['int', '>0'], 'integer'] expects m.UndefinedName. Each function is annotated -> None and returns None. These are assertions available at the historical commit, not supplied historical execution results."
}
```
