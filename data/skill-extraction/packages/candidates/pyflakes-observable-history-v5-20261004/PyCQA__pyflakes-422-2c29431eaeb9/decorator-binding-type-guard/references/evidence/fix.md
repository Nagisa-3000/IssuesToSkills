# Merged binding guard

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:422:fix",
  "source_id": "PyCQA/pyflakes:422:repair:2c29431eaeb9",
  "available_at": "2019-01-31T14:09:20Z",
  "kind": "historical_merged_implementation",
  "observation": "In historical pyflakes/checker.py, is_typing_overload gained `isinstance(scope[node.id], ImportationFrom)` between `node.id in scope` and `scope[node.id].fullName == 'typing.overload'` in the ast.Name branch. The supplied diff shows the following ast.Attribute alternative without a modification. This is the merged implementation change; no historical execution transcript is supplied."
}
```
