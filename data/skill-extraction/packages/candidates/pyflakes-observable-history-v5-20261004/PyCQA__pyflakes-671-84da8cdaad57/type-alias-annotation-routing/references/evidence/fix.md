# Merged routing implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:671:fix",
  "source_id": "PyCQA/pyflakes:671:repair:84da8cdaad57",
  "available_at": "2022-02-13T16:32:09Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, Checker.ANNASSIGN retained `self.handleNode(node.target, node)` and `self.handleAnnotation(node.annotation, node)`. Inside the existing `if node.value:` guard, the merged change called `self.handleAnnotation(node.value, node)` when `_is_typing(node.annotation, 'TypeAlias', self.scopeStack)` was true and otherwise retained `self.handleNode(node.value, node)`. The same diff corrected the `_is_name_or_attr` type comment from `ast.Ast` to `ast.AST`. The implementation evidence establishes the TypeAlias-specific routing mechanism; it contains no historical test-run result."
}
```
