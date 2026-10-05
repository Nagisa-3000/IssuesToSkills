# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8563:fix",
  "source_id": "pylint-dev/pylint:8563:repair:4a485e28f0a5",
  "available_at": "2023-04-16T17:34:35Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged implementation in pylint/checkers/refactoring/refactoring_checker.py retained the len(node.args) == 1 and nodes.ListComp gate and the as_string()[1:-1] body extraction. It added a node.keywords branch that parenthesized inside_comp and appended comma-space followed by comma-space-joined kw.as_string() renderings. The comment changed to exactly one positional argument. The news fragment described improved consider-using-generator output for min calls with default and closed issue 8563. The resolution repaired output rather than suppressing the diagnostic. Historical CI execution is unknown."
}
```
