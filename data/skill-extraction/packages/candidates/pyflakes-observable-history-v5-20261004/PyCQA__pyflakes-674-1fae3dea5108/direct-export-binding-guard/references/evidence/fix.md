# Merged dispatch restriction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:fix",
  "source_id": "PyCQA/pyflakes:674:repair:1fae3dea5108",
  "available_at": "2022-02-12T14:52:33Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, the Checker branch constructing `ExportBinding(name, node._pyflakes_parent, self.scope)` retained `name == '__all__'` and `isinstance(self.scope, ModuleScope)` and added `isinstance(node._pyflakes_parent, (ast.Assign, ast.AugAssign, ast.AnnAssign))`. The supplied diff leaves the surrounding Binding and Argument branches intact. This records the merged implementation, not a historical test execution."
}
```
