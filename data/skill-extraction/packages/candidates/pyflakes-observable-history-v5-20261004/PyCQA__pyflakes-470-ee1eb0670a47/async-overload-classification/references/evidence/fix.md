# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:470:fix",
  "source_id": "PyCQA/pyflakes:470:repair:ee1eb0670a47",
  "available_at": "2019-09-30T22:27:58Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py adds FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef) in the PY35_PLUS branch and FUNCTION_TYPES = (ast.FunctionDef,) otherwise, alongside compatibility-dependent loop type tuples. In is_typing_overload(value, scope_stack), isinstance(value.source, ast.FunctionDef) changes to isinstance(value.source, FUNCTION_TYPES). The existing any(...) scan using is_typing_overload_decorator over value.source.decorator_list remains unchanged. This supplies implementation evidence for the repair, not a historical test execution transcript."
}
```
