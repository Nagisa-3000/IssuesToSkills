# Merged repair implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:395:fix",
  "source_id": "PyCQA/pyflakes:395:repair:066ba4a93c10",
  "available_at": "2019-01-01T13:10:34Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged checker diff defines PY35_PLUS = sys.version_info >= (3, 5) and PY36_PLUS = sys.version_info >= (3, 6), replacing PY34 = sys.version_info < (3, 5). The positive PY35_PLUS branch includes ast.AsyncFor in FOR_TYPES and LOOP_TYPES; the older-version branch retains only synchronous loop types. Existing _MAGIC_GLOBALS entries are '__file__', '__builtins__', and 'WindowsError'. Under if PY36_PLUS, the diff appends '__annotations__'. The authoritative source marks this repair resolved. The supplied diff contains no historical test execution result."
}
```
