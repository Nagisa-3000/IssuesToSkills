# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5989:fix",
  "source_id": "pylint-dev/pylint:5989:repair:5c8384e811e3",
  "available_at": "2022-03-27T12:31:53Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/classes/class_checker.py added 'if not closest_func.is_bound(): return False' after the closest-function absence guard and before checking closest_func.args.args in _is_mandatory_method_param. Its documentation added 'Static methods return False.' A separate branch replaced self._is_type_self_call(attribute.expr) with isinstance(attribute.expr, nodes.Call). The ChangeLog stated that the repair fixed a false-negative regression in 2.13.0 where protected-access was not raised on functions and included 'Fixes #5989'. This records the merged implementation and closure text; historical CI/test execution remains unknown."
}
```
