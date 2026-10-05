# Merged guard

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4732:fix",
  "source_id": "pylint-dev/pylint:4732:repair:a2c166cf5fc3",
  "available_at": "2021-07-21T06:24:01Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/refactoring/refactoring_checker.py extended the existing condition skipping absent inference or calls outside CALLS_RETURNING_CONTEXT_MANAGERS with: or not isinstance(assignee, (astroid.AssignName, astroid.AssignAttr)). The condition continues before deferred stack lookup and varname extraction. The ChangeLog records a fix for crashes when a callable returning a context manager is assigned to a list or dict item and states Closes #4732. doc/whatsnew/2.9.rst records the same fix. Historical test execution is not supplied."
}
```
