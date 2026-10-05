# Historical merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3791:fix",
  "source_id": "pylint-dev/pylint:3791:repair:a054796d7008",
  "available_at": "2021-07-22T19:31:25Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged change in pylint/checkers/variables.py changes the consumed-name condition from name-in-consumed AND NOT(comprehension AND upper-function homonym) to name-in-consumed AND (utils.is_func_decorator(current_consumer.node) OR NOT(comprehension AND upper-function homonym)). The branch still resolves utils.assign_parent(current_consumer.consumed[name][0]) and calls self._check_late_binding_closure(node, defnode). Historical CI/test execution is unknown."
}
```
