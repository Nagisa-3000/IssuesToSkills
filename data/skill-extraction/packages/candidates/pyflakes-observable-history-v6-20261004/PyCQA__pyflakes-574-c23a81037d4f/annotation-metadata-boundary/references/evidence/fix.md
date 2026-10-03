# Historical merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:574:fix",
  "source_id": "PyCQA/pyflakes:574:repair:c23a81037d4f",
  "available_at": "2020-09-28T20:44:22Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py added `_is_name_or_attr`, matching ast.Name.id or ast.Attribute.attr. SUBSCRIPT retained Literal handling through that helper and added an Annotated branch. The branch visited node.value, accepted a direct ast.Tuple slice or ast.Index wrapping ast.Tuple, traversed node.slice normally for non-tuples or fewer than two elements, visited the first tuple element in the inherited context, visited remaining elements inside `with self._enter_annotation(AnnotationState.NONE):`, and visited node.ctx. The generic typing-member branch remained after these special cases. This evidence is an implementation diff, not a historical test-run log."
}
```
