# Historical merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:575:fix",
  "source_id": "PyCQA/pyflakes:575:repair:e3f26593eac9",
  "available_at": "2021-03-14T16:02:46Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py introduced omit, annotated and not_annotated collections in call traversal. Recognized TypedDict calls collected dictionary values from a dictionary second argument and keyword values as annotations. Recognized NamedTuple calls collected second elements from structurally valid tuple/list field pairs, with field names outside annotation context, and collected keyword values as annotations. TypeVar collected positional arguments after the first and bound keyword values as annotations. cast handled its first argument under _enter_annotation() whenever present, removing the string-only condition. With omit entries, non-annotation traversal occurred under AnnotationState.NONE before annotation traversal; otherwise ordinary handleChildren(node) remained. This is implementation evidence at the merged revision, not historical test execution output."
}
```
