# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8536:fix",
  "source_id": "pylint-dev/pylint:8536:repair:b63c8a1c148e",
  "available_at": "2023-04-07T20:17:19Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/base/name_checker/checker.py, the function-local branch retained node.name in frame, node.name not in frame.argnames(), and not _redefines_import(node). It replaced unconditional self._check_name(\"variable\", node.name, node) with a conditional: isinstance(assign_type, nodes.AnnAssign) and self._assigns_typealias(assign_type.annotation) selects self._check_name(\"typealias\", node.name, node); otherwise variable naming remains. The supplied hunk did not change the following class-scope branch. The new release fragment stated that TypeAlias variables defined in functions are now checked for invalid-name errors and recorded Closes #8536. Historical test execution is not reported in this core diff."
}
```
