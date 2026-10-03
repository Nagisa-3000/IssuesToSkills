# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:728:fix",
  "source_id": "PyCQA/pyflakes:728:repair:4dcd92e45efe",
  "available_at": "2022-09-08T22:10:17Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, Checker.ANNASSIGN removed `self.handleNode(node.target, node)` from the start of the handler and placed the same call after annotation and optional value processing. `self.handleAnnotation(node.annotation, node)` and the existing conditional value dispatch, including `self.handleAnnotation(node.value, node)` versus `self.handleNode(node.value, node)`, remained before target handling. The supplied diff is implementation evidence; it contains no historical execution result."
}
```
