# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6301:regression",
  "source_id": "pylint-dev/pylint:6301:repair:1664202ba5de",
  "available_at": "2022-04-19T15:21:03Z",
  "kind": "historical_regression_assertions",
  "observation": "The tests/test_similar.py diff appended --persistent=no, --enable=astroid-error, --ignore-imports=y, and --ignore-signatures=y in the helper, enabling functionality that builds another AST. The output helper stored stripped actual output, retained expected-output containment, and added assert 'Fatal error' not in actual_output_stripped. These are committed assertions available at the repair revision. Historical execution is unknown; authored Skill functional definitions remain unexecuted."
}
```
