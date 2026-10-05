# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6089:fix",
  "source_id": "pylint-dev/pylint:6089:repair:e444a22e2ef0",
  "available_at": "2022-04-03T14:26:48Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/variables.py removes caching of _is_used_before_assignment_enabled and removes the early return of (VariableVisitConsumerAction.RETURN, found_nodes) when neither undefined-variable nor used-before-assignment is enabled. The return followed _check_late_binding_closure(node) and preceded utils.assign_parent(found_nodes[0]), statement(future=True), and frame(future=True) processing. The nearby undefined-variable and undefined-loop-variable enablement caches remain. ChangeLog and doc/whatsnew/2.13.rst describe fixing false unused-import when both diagnostics are disabled and state Closes #6089. Historical CI/test execution is unknown."
}
```
