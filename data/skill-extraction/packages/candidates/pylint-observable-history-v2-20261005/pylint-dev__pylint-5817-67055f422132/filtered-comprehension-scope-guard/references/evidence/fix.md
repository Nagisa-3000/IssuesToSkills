# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5817:fix",
  "source_id": "pylint-dev/pylint:5817:repair:67055f422132",
  "available_at": "2022-02-17T15:27:29Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/variables.py the exception-handler assignment filtering condition changed from 'if found_nodes:' to 'if found_nodes and (not isinstance(parent_node, nodes.Comprehension) or node not in parent_node.ifs):'. The added comment exempts a test in a filtered comprehension, illustrated by '[e for e in range(3) if e]' followed by an exception binding of e. ChangeLog and doc/whatsnew/2.13.rst describe the false-positive fix and say 'Closes #5817'. The supplied diff establishes implementation and closure text; historical CI execution is unknown."
}
```
