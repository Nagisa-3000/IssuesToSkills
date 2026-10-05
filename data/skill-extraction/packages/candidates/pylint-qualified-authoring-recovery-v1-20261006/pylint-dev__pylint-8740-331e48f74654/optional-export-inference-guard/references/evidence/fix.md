# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8740:fix",
  "source_id": "pylint-dev/pylint:8740:repair:331e48f74654",
  "available_at": "2023-06-06T19:19:41Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/variables.py, VariablesChecker._check_all wraps assigned = next(node.igetattr(\"__all__\")) in try, with except astroid.InferenceError: return. The existing isinstance(assigned, util.UninferableBase) early return and assigned.pytype() check against builtins.list and builtins.tuple remain afterward. The new doc/whatsnew/fragments/8740.bugfix says \"Fix a crash when ``__all__`` exists but cannot be inferred.\" and \"Closes #8740\". Historical CI/test execution is unknown."
}
```
