# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:422:fix",
  "source_id": "PyCQA/pyflakes:422:repair:2c29431eaeb9",
  "available_at": "2019-01-31T14:09:20Z",
  "kind": "historical_merged_implementation",
  "observation": "In historical pyflakes/checker.py, is_typing_overload's ast.Name branch already checked node.id in scope and compared scope[node.id].fullName to 'typing.overload'. The merged repair inserted isinstance(scope[node.id], ImportationFrom) and between membership and fullName comparison. The visible diff leaves the adjacent ast.Attribute branch unchanged. This entry establishes the merged implementation, not a historical test execution."
}
```
