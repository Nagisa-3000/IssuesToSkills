# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6557:fix",
  "source_id": "pylint-dev/pylint:6557:repair:5fcccc13f1f7",
  "available_at": "2022-05-11T14:20:18Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/refactoring/refactoring_checker.py, inside `elif isinstance(value, nodes.Subscript)`, the merged change added `or not isinstance(value.value, nodes.Name)` after `not isinstance(node.target, nodes.AssignName)` and before `or node.target.name != value.value.name`. The subsequent dictionary-expression comparison remained. ChangeLog and doc/whatsnew/2.13.rst described fixing an unnecessary-dict-index-lookup crash when subscripting an attribute and stated Closes #6557. The artifact records implementation and closure text; historical CI/test execution is unknown."
}
```
