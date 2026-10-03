# Merged traversal change

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:575:fix",
  "source_id": "PyCQA/pyflakes:575:repair:e3f26593eac9",
  "available_at": "2021-03-14T16:02:46Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged call-visitor diff introduced omit, annotated, and not_annotated collections. TypedDict literal-dictionary values and keyword values enter annotation traversal. NamedTuple recognized two-element list/tuple field pairs contribute second elements as types, while labels are non-annotation traversal; keyword values are annotated. TypeVar arguments after the first and bound values are annotated. For partitioned calls, selected ordinary children are traversed under AnnotationState.NONE and selected type nodes under _enter_annotation(). The cast first argument now enters annotation context whenever present, removing the previous ast.Str restriction and explicit STRING state; its branch still reaches ordinary handleChildren when omit is empty. Dispatch remains guarded by _is_typing. The supplied merged implementation establishes the repair change, not a historical execution log."
}
```
