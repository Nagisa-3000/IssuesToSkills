# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7528:fix",
  "source_id": "pylint-dev/pylint:7528:repair:aca8dd546e6e",
  "available_at": "2022-09-30T11:11:37Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/modified_iterating_checker.py changed the _common_cond_list_set iterable annotation from nodes.NodeNG to nodes.Name | nodes.Attribute. It introduced iter_obj_name = iter_obj.attrname if isinstance(iter_obj, nodes.Attribute) else iter_obj.name and compared node.value.func.expr.name to iter_obj_name. The infer_val == utils.safe_infer(iter_obj) guard remained. The new doc/whatsnew/fragments/7528.bugfix described fixing the modified_iterating checker crash when iterating on a set defined as a class attribute and stated Closes #7528. Historical test and CI execution are unknown."
}
```
