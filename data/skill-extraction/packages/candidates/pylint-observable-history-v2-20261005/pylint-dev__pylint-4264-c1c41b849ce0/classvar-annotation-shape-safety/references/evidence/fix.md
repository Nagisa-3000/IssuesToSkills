# Merged repair

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4264:fix",
  "source_id": "pylint-dev/pylint:4264:repair:c1c41b849ce0",
  "available_at": "2021-03-30T07:19:15Z",
  "kind": "historical_merged_implementation",
  "observation": "The repair changed pylint/checkers/utils.py:is_class_var to return False unless node.parent is astroid.AnnAssign, assign annotation = node.parent.annotation, and unwrap astroid.Subscript using annotation.value. It returns True for astroid.Name whose name is \"ClassVar\" or astroid.Attribute whose attrname is \"ClassVar\", and False otherwise. The ChangeLog records 'Fix issue with annotated class constants' and 'Closes #4264'. Historical CI execution is not supplied and remains unknown."
}
```
