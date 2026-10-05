# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4277:fix",
  "source_id": "pylint-dev/pylint:4277:repair:44a3aa25fd9b",
  "available_at": "2021-04-01T12:02:36Z",
  "kind": "historical_merged_implementation",
  "observation": "NameChecker's annotation-based class-constant alternative changes from utils.is_class_var(node) to utils.is_assign_name_annotated_with(node, \"Final\"), retaining the Enum ancestor condition. The helper is renamed and parameterized by typing_name; it requires an AnnAssign parent, unwraps a Subscript to its value, and compares Name.name or Attribute.attrname to the requested name. The ChangeLog describes correcting ClassVar constant misclassification and recognizing Final, closing #4277. The diff does not establish historical CI execution."
}
```
