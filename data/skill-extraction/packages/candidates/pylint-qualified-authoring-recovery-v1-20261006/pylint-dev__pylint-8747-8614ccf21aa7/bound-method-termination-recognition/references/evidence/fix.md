# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8747:fix",
  "source_id": "pylint-dev/pylint:8747:repair:8614ccf21aa7",
  "available_at": "2023-06-11T23:37:19Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged implementation changes _is_function_def_never_returning's input declaration to nodes.FunctionDef | astroid.BoundMethod, updates its argument documentation, and changes its guard to isinstance(node, (nodes.FunctionDef, astroid.BoundMethod)) and node.returns. The existing annotation-recognition logic follows the guard, including the shown nodes.Attribute branch matching attrname == NoReturn. The release-note fragment states that method calls annotated NoReturn had been ignored by inconsistent-return-statements and says Closes #8747. Historical CI/test execution is unknown."
}
```
