# Historical implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:419:fix",
  "source_id": "PyCQA/pyflakes:419:repair:ba64624f38a5",
  "available_at": "2019-02-01T16:41:28Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py added class DummyNode(object), documented as 'Used in place of an `ast.AST` to set error message positions', whose constructor assigns lineno and col_offset. The deferred functools.partial call to handleStringAnnotation changed its diagnostic node argument from node to DummyNode(lineno, col_offset), retaining part, the explicit lineno and col_offset arguments, and messages.CommentAnnotationSyntaxError. The authoritative source marks the repair as a verified resolution; this diff is not a historical test execution log."
}
```
