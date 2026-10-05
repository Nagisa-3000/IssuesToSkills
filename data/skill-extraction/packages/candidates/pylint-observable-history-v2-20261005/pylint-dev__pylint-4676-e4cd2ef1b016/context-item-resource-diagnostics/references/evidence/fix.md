# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4676:fix",
  "source_id": "pylint-dev/pylint:4676:repair:e4cd2ef1b016",
  "available_at": "2021-07-06T19:46:15Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff added `_is_part_of_with_items(node: astroid.Call) -> bool`. It sets `frame = node.frame()`, walks parents while `current != frame`, and at the first astroid.With compares `node.lineno` with the inclusive interval from `current.items[0][0].lineno` through `current.items[-1][0].tolineno`. It returns False if no With is encountered before the frame. The resource-call condition changed from `not isinstance(node.parent, astroid.With)` to `not _is_part_of_with_items(node)`. ChangeLog records the ternary-with R1732 false-positive fix and `Closes #4676`; the 2.9 release notes also record the fix. Historical CI/test execution status is unknown."
}
```
