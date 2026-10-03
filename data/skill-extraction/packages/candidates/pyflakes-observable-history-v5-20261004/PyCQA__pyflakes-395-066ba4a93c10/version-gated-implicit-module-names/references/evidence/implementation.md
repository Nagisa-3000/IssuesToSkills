# Historical merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:395:fix",
  "source_id": "PyCQA/pyflakes:395:repair:066ba4a93c10",
  "available_at": "2019-01-01T13:10:34Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py replaced `PY34 = sys.version_info < (3, 5)` with `PY35_PLUS = sys.version_info >= (3, 5)` and added `PY36_PLUS = sys.version_info >= (3, 6)`. It reordered the loop-type branches: under PY35_PLUS, FOR_TYPES remained (ast.For, ast.AsyncFor) and LOOP_TYPES remained (ast.While, ast.For, ast.AsyncFor); otherwise the tuples remained (ast.For,) and (ast.While, ast.For). The existing _MAGIC_GLOBALS list ['__file__', '__builtins__', 'WindowsError'] was retained. A PEP 526 comment and `if PY36_PLUS: _MAGIC_GLOBALS.append('__annotations__')` were added. This is the merged repair mechanism; no historical test execution result is supplied."
}
```
