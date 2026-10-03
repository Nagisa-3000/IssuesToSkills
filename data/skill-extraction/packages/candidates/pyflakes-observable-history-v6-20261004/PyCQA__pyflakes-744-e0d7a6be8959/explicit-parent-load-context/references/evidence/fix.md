# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:744:fix",
  "source_id": "PyCQA/pyflakes:744:repair:e0d7a6be8959",
  "available_at": "2022-11-24T16:51:46Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py changed handleNodeLoad(self, node) to handleNodeLoad(self, node, parent). It removed parent = self.getParent(node) from the branch for name == 'print' with a Builtin binding, retaining the ast.BinOp and ast.RShift condition that reports InvalidPrintSyntax. NAME load dispatch changed to self.handleNodeLoad(node, self.getParent(node)). AUGASSIGN changed to self.handleNodeLoad(node.target, node), followed by unchanged self.handleNode(node.value, node) and self.handleNode(node.target, node). The authoritative SourceRecord marks this repair as a verified resolution. No historical test execution transcript accompanies the diff."
}
```
