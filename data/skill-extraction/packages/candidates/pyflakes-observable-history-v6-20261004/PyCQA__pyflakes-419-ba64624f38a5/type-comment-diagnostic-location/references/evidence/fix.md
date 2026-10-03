# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:419:fix",
  "source_id": "PyCQA/pyflakes:419:repair:ba64624f38a5",
  "available_at": "2019-02-01T16:41:28Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py introduces DummyNode(object), documented as 'Used in place of an `ast.AST` to set error message positions'. Its constructor assigns self.lineno = lineno and self.col_offset = col_offset. In the deferred functools.partial call to handleStringAnnotation, the second argument changes from node to DummyNode(lineno, col_offset). The part, explicit lineno and col_offset arguments, and messages.CommentAnnotationSyntaxError remain unchanged. This is implementation evidence; no historical test execution log is supplied."
}
```
