# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:510:regression",
  "source_id": "PyCQA/pyflakes:510:repair:76416437ef22",
  "available_at": "2020-03-17T20:53:38Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff adds five tests in pyflakes/test/test_type_annotations.py using self.flakes without expected diagnostics: Optional['Queue[str]']; Callable[['Queue[str]'], None]; cast('Optional[int]', 42); cast(str, 'Optional[int]') with only cast imported; and renamed direct imports cast as tsac and Optional as Maybe with tsac('Maybe[int]', 42). The second-argument string test explicitly protects ordinary string values that resemble type annotations. These assertions were available at the historical commit. Their historical execution status is unknown from the supplied core evidence; the later changed-test-only qualification is recorded separately in provenance."
}
```
