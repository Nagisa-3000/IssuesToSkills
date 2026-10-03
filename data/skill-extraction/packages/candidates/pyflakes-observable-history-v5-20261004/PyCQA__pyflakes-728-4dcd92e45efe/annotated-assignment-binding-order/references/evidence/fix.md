# Merged target-order repair

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:728:fix",
  "source_id": "PyCQA/pyflakes:728:repair:4dcd92e45efe",
  "available_at": "2022-09-08T22:10:17Z",
  "kind": "historical_merged_implementation",
  "observation": "In historical pyflakes/checker.py, Checker.ANNASSIGN removed `self.handleNode(node.target, node)` from before `self.handleAnnotation(node.annotation, node)` and added that same target visit after the existing optional initializer processing. The shown initializer paths retained `self.handleAnnotation(node.value, node)` in one branch and `self.handleNode(node.value, node)` in the other. The merged implementation therefore analyzed annotation and initializer before the target visit. No historical test execution output is present in this diff."
}
```
