# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:728:fix",
  "source_id": "PyCQA/pyflakes:728",
  "available_at": "2022-09-08T22:10:17Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, Checker.ANNASSIGN removed `self.handleNode(node.target, node)` from before `self.handleAnnotation(node.annotation, node)` and inserted the target call after optional value handling. Existing value paths retained `self.handleAnnotation(node.value, node)` or `self.handleNode(node.value, node)`. The complete specialized branch condition was not supplied. This is the merged repair implementation, not a historical execution log."
}
```
