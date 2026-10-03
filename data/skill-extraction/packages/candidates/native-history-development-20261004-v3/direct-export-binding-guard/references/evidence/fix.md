# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:fix",
  "source_id": "PyCQA/pyflakes:674",
  "available_at": "2022-02-12T14:52:33Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py changed the ExportBinding dispatch condition from name == '__all__' and isinstance(self.scope, ModuleScope) to those same checks plus isinstance(node._pyflakes_parent, (ast.Assign, ast.AugAssign, ast.AnnAssign)). The call remained ExportBinding(name, node._pyflakes_parent, self.scope). Surrounding earlier binding and later argument branches remained in place. This is merged implementation evidence, not a historical execution log."
}
```
