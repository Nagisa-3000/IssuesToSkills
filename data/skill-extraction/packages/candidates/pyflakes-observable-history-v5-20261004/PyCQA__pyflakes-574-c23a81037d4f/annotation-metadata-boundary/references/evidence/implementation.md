# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:574:fix",
  "source_id": "PyCQA/pyflakes:574:repair:c23a81037d4f",
  "available_at": "2020-09-28T20:44:22Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py adds `_is_name_or_attr`, recognizing ast.Name.id or ast.Attribute.attr, and uses it for Literal while retaining the Literal state save/restore structure. Its new Annotated SUBSCRIPT branch visits node.value, recognizes a direct ast.Tuple slice for Python 3.9+ or ast.Index containing ast.Tuple for older ASTs, and visits node.slice normally when no tuple exists or fewer than two elements exist. Otherwise it visits the first element in the existing context and all later elements within `_enter_annotation(AnnotationState.NONE)`. It then visits node.ctx. These are merged repair facts; the diff supplies no historical execution results."
}
```
