# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:441:fix",
  "source_id": "PyCQA/pyflakes:441:repair:4a807d45f9dd",
  "available_at": "2019-07-03T01:37:22Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py changed the child traversal after `self.pushScope()` from `self.handleChildren(node, omit='decorator_list')` to `self.handleChildren(node, omit=['decorator_list', 'returns'])`. It retained decorator exclusion and added return-annotation exclusion. The supplied excerpt does not show the earlier annotation-processing code and does not contain a test execution log."
}
```
