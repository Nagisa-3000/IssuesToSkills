# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:441:fix",
  "source_id": "PyCQA/pyflakes:441:repair:4a807d45f9dd",
  "available_at": "2019-07-03T01:37:22Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, in Checker after self.pushScope(), the merged diff replaces self.handleChildren(node, omit='decorator_list') with self.handleChildren(node, omit=['decorator_list', 'returns']). This adds returns to the omission while retaining decorator_list. The supplied diff does not show the complete earlier annotation-processing pass or historical test-run output."
}
```
