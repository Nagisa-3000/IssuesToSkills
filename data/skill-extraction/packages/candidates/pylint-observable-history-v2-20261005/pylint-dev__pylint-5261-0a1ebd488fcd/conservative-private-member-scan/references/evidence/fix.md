# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5261:fix",
  "source_id": "pylint-dev/pylint:5261:repair:0a1ebd488fcd",
  "available_at": "2021-11-05T20:26:54Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged change in pylint/checkers/classes.py replaces the combined Attribute condition with an Attribute branch containing `if not isinstance(child.expr, nodes.Name): break`, followed by the original attribute-name comparison and receiver-name membership in self, cls, and node.name. The break precedes attribute-name comparison. Bare Name matching, function-argument exclusion, and loop-else unused-private-member emission remain. A method docstring and crash-fix entries in ChangeLog and doc/whatsnew/2.12.rst were added, stating Closes #5261. Historical CI execution is unknown."
}
```
