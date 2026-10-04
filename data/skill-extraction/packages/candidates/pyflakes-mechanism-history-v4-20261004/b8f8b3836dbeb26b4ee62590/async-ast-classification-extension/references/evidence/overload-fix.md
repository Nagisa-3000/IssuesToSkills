# Merged overload classification

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:470:fix",
  "source_id": "PyCQA/pyflakes:470:repair:ee1eb0670a47",
  "available_at": "2019-09-30T22:27:58Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py defines FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef) under PY35_PLUS and FUNCTION_TYPES = (ast.FunctionDef,) otherwise. In is_typing_overload it replaces isinstance(value.source, ast.FunctionDef) with isinstance(value.source, FUNCTION_TYPES), retaining any(is_typing_overload_decorator(dec) for dec in value.source.decorator_list). It records the classification extension and compatibility guard, not historical test execution."
}
```
