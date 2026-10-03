# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:401:regression",
  "source_id": "PyCQA/pyflakes:401:repair:1f58890b3ea7",
  "available_at": "2019-01-17T19:38:16Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in pyflakes/test/test_type_annotations.py added test_annotated_async_def with @skipIf(version_info < (3, 5), 'new in Python 3.5'). It calls self.flakes on class c: pass followed by async def func(c: c) -> None: pass, without expected diagnostic arguments. This regression assertion was available at the historical repair commit. No historical execution log was supplied; historical execution status is unknown."
}
```
