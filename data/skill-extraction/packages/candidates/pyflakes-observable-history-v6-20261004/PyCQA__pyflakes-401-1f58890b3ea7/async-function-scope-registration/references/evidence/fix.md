# Merged registration

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:401:fix",
  "source_id": "PyCQA/pyflakes:401:repair:1f58890b3ea7",
  "available_at": "2019-01-17T19:38:16Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py added, after the _ast_node_scope dictionary, \"if PY35_PLUS:\" and beneath it \"_ast_node_scope[ast.AsyncFunctionDef] = FunctionScope,\". The trailing comma is part of the assignment. This registers asynchronous function definitions using FunctionScope under the Python 3.5-plus gate. The supplied diff does not modify getParent or introduce a Module.parent fallback."
}
```
