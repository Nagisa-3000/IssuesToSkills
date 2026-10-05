# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4668:fix",
  "source_id": "pylint-dev/pylint:4668:repair:f6c813824183",
  "available_at": "2021-07-18T13:11:15Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/classes.py initialized acceptable_obj_names to [\"self\"] for each private AssignAttr. If assign_attr.scope() was an astroid.FunctionDef named __new__, it extended the list with return_node.value.name for Return nodes whose values were astroid.Name. In same-attribute-name matching it replaced the self-only assignment/read branch with assign_attr.expr.name in acceptable_obj_names and attribute.expr.name == \"self\", retaining the preceding cls/self branch. The ChangeLog described the false-positive fix and stated Closes #4668. Historical CI/test execution is not supplied."
}
```
