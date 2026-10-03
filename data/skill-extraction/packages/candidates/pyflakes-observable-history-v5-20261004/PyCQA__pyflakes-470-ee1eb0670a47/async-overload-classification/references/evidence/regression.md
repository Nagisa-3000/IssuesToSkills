# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:470:regression",
  "source_id": "PyCQA/pyflakes:470:repair:ee1eb0670a47",
  "available_at": "2019-09-30T22:27:58Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_type_annotations.py adds test_typingOverloadAsync with @skipIf(version_info < (3, 5), 'new in Python 3.5') and docstring 'Allow intentional redefinitions via @typing.overload (async)'. The self.flakes call receives source importing overload from typing, two @overload async def f(s) declarations with type comments (None) -> None and (int) -> int and pass bodies, and an async def f(s) implementation returning s. No expected diagnostic arguments are supplied. These are assertions available at the repair commit; historical test execution status is unknown."
}
```
