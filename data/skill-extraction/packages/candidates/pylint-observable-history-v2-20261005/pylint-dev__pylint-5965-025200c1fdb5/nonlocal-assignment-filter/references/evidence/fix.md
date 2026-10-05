# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5965:fix",
  "source_id": "pylint-dev/pylint:5965:repair:025200c1fdb5",
  "available_at": "2022-03-25T09:45:57Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/variables.py adds, before ExceptHandler assignment filtering, an any() check over node.frame(future=True).get_children() for isinstance(child, nodes.Nonlocal) and node.name in child.names. If true it returns found_nodes, preserving the candidate result already computed by earlier logic. The ChangeLog describes fixing a 2.13.0 regression emitting used-before-assignment for nonlocal usage in a try block and cites #5965 under the 2.13.1 heading with release date TBA. Historical CI/test-execution status is unknown."
}
```
