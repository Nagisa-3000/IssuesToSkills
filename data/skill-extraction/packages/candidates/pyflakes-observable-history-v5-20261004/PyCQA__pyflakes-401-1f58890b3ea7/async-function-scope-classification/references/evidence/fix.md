# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:401:fix",
  "source_id": "PyCQA/pyflakes:401:repair:1f58890b3ea7",
  "available_at": "2019-01-17T19:38:16Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py added `if PY35_PLUS:` followed by `_ast_node_scope[ast.AsyncFunctionDef] = FunctionScope,` to Checker's scope classification. The trailing comma makes the assigned value tuple-shaped. This registers asynchronous function definitions using FunctionScope under the Python 3.5+ gate. It is the supplied verified repair implementation; no historical test execution log is included."
}
```
