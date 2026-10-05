# Merged implementation

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5200:fix",
  "source_id": "pylint-dev/pylint:5200:repair:8c7e2fae6fee",
  "available_at": "2021-10-29T19:44:19Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pylint/checkers/refactoring/refactoring_checker.py retains utils.safe_infer(truth_value), changes the unavailable-inference guard from membership in (None, astroid.Uninferable) to inferred_truth_value is None or inferred_truth_value == astroid.Uninferable, retains truth_boolean_value=True in that branch, and replaces truth_value.bool_value() with inferred_truth_value.bool_value(). The existing truth_boolean_value is False branch selects simplify-boolean-expression. ChangeLog and doc/whatsnew/2.12.rst describe a fix when the condition can be inferred as False and close #5200. Historical test execution is unknown."
}
```
