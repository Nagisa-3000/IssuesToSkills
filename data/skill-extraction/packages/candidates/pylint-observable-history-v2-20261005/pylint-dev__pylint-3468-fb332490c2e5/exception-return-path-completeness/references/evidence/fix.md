# Historical implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3468:fix",
  "source_id": "pylint-dev/pylint:3468:repair:fb332490c2e5",
  "available_at": "2020-09-06T19:08:03Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged implementation added an astroid.TryExcept branch using all(self._is_node_return_ended(child) for child in node.get_children()) and removed astroid.ExceptHandler exclusion from generic recursion. Conditional logic moved into a helper excluding inner FunctionDef nodes; an if without orelse required a later direct sibling Return and a returning body. Raise handling moved into a helper retaining bare-raise termination, safe inference, matching-handler analysis, and unhandled-raise termination. Several internal functions gained trailing return None. Release documentation described the changed diagnostic behavior and closing issue 3468. Resolution is verified by the supplied source qualification; historical CI/test execution is unknown."
}
```
