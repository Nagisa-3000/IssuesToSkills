# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7461:fix",
  "source_id": "pylint-dev/pylint:7461:repair:fb30fe09d74d",
  "available_at": "2022-09-16T07:24:19Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff changes iter_obj annotations in the list, dictionary, and set condition helpers from nodes.NodeNG to nodes.Name | nodes.Attribute. After existing dictionary guards and the safe_infer comparison, it selects iter_obj.attrname when isinstance(iter_obj, nodes.Attribute), otherwise iter_obj.name, and returns 'node.targets[0].value.name == iter_obj_name'. The release fragment says 'Fix a crash in the modified-iterating-dict checker involving instance attributes' and 'Closes #7461'. Historical CI and test execution are unknown."
}
```
