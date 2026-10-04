# Committed overload assertion

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:470:regression",
  "source_id": "PyCQA/pyflakes:470:repair:ee1eb0670a47",
  "available_at": "2019-09-30T22:27:58Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_type_annotations.py adds test_typingOverloadAsync, skipped below Python 3.5, with docstring 'Allow intentional redefinitions via @typing.overload (async)'. self.flakes receives code importing overload from typing, two decorated async def f(s) declarations with type comments (None) -> None and (int) -> int and pass bodies, then an undecorated async implementation returning s. No expected diagnostics are supplied. Historical execution is unknown from the supplied record."
}
```
