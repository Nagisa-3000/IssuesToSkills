# Historical implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5569:fix",
  "source_id": "pylint-dev/pylint:5569:repair:642268f63624",
  "available_at": "2022-01-11T15:50:30Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff inserts `if self._is_type_self_call(attribute.expr): continue` after attribute-name matching and before the name-based condition. It annotates _is_type_self_call with nodes.NodeNG and bool. _is_mandatory_method_param uses _first_attrs[-1] when available; otherwise it obtains the closest nodes.FunctionDef ancestor, returns False if absent or without positional arguments, and compares a nodes.Name to the first positional argument's name. The comment says the function may already have been unregistered. ChangeLog and 2.13 release notes describe the unused-private-member crash fix for type(self) in bound methods and state Closes #5569. The supplied diff does not expose all existing recognizer conditions. Historical CI/test execution is unknown."
}
```
