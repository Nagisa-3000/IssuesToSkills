# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:fix",
  "source_id": "PyCQA/pyflakes:671",
  "available_at": "2022-02-13T16:32:09Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged pyflakes/checker.py diff retained handleNode(node.target, node) and handleAnnotation(node.annotation, node) in ANNASSIGN. Within if node.value, _is_typing(node.annotation, 'TypeAlias', self.scopeStack) selected handleAnnotation(node.value, node); the else branch retained handleNode(node.value, node). The diff also corrected the _is_name_or_attr type comment from ast.Ast to ast.AST. No execution result accompanies this implementation evidence."
}
```
