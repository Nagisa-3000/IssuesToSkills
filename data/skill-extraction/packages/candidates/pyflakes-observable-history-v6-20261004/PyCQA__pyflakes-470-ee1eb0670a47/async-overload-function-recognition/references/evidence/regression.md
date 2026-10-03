# Historical regression assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:470:regression",
  "source_id": "PyCQA/pyflakes:470:repair:ee1eb0670a47",
  "available_at": "2019-09-30T22:27:58Z",
  "kind": "historical_regression_assertions",
  "observation": "The merged diff in pyflakes/test/test_type_annotations.py adds test_typingOverloadAsync with @skipIf(version_info < (3, 5), 'new in Python 3.5'). Its docstring is 'Allow intentional redefinitions via @typing.overload (async)'. It calls self.flakes on code importing overload from typing, two decorated async def f(s) declarations with type comments (None) -> None and (int) -> int and pass bodies, then an undecorated async def f(s) returning s. No expected diagnostics are supplied. This is a historical no-diagnostic assertion available at the commit; historical execution is unknown from the supplied record."
}
```
