# Merged guard

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4379:fix",
  "source_id": "pylint-dev/pylint:4379:repair:95c05e024cf4",
  "available_at": "2021-04-19T19:36:37Z",
  "kind": "historical_merged_implementation",
  "observation": "In pylint/checkers/refactoring/refactoring_checker.py, the existing isinstance(right_statement, astroid.Name) branch keeps reading right_statement.name. The former else reading right_statement.value becomes elif isinstance(right_statement, astroid.Const); a new else returns. The subsequent comparison of right_statement_value with body_value remains. The supplied diff establishes implementation content, not historical test execution."
}
```
