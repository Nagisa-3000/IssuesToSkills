# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:510:regression",
  "source_id": "PyCQA/pyflakes:510:repair:76416437ef22",
  "available_at": "2020-03-17T20:53:38Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_type_annotations.py adds five self.flakes assertions without expected diagnostics: Optional['Queue[str]'] using imported Queue; Callable[['Queue[str]'], None] using imported Queue; cast('Optional[int]', 42); cast(str, 'Optional[int]') with only cast imported, guarding against interpreting the second argument as a type annotation; and renamed imports cast as tsac and Optional as Maybe with tsac('Maybe[int]', 42). These assertions were available at the historical commit. Their historical execution status is unknown from the supplied diff; package eval definitions have not been executed."
}
```
