# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:fix",
  "source_id": "PyCQA/pyflakes:674:repair:1fae3dea5108",
  "available_at": "2022-02-12T14:52:33Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, the specialized branch previously conditioned only on name == '__all__' and isinstance(self.scope, ModuleScope) gained isinstance(node._pyflakes_parent, (ast.Assign, ast.AugAssign, ast.AnnAssign)). It still constructs ExportBinding(name, node._pyflakes_parent, self.scope). The supplied diff retains surrounding binding branches. This is the merged implementation, not a historical test-run result."
}
```
