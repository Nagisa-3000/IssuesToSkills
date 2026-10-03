# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:744:fix",
  "source_id": "PyCQA/pyflakes:744:repair:e0d7a6be8959",
  "available_at": "2022-11-24T16:51:46Z",
  "kind": "historical_merged_implementation",
  "observation": "The checker.py diff changes handleNodeLoad(self, node) to handleNodeLoad(self, node, parent), removes parent = self.getParent(node) from the builtin-print branch, changes NAME load dispatch to self.handleNodeLoad(node, self.getParent(node)), and changes AUGASSIGN to self.handleNodeLoad(node.target, node). AUGASSIGN still visits node.value and then node.target afterward. The builtin-print BinOp/RShift condition remains. The diff supplies implementation evidence, not a historical test-run log."
}
```
