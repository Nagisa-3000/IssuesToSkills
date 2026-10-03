# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:483:regression",
  "source_id": "PyCQA/pyflakes:483:repair:0af480e3351a",
  "available_at": "2020-02-17T19:43:55Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff adds test_is_tuple_constant asserting IsLiteral for x = 5; if x is (): pass, and test_is_tuple_constant_containing_constants asserting IsLiteral for x = 5; if x is (1, '2', True, (1.5, ())): pass. It adds test_is_tuple_containing_variables_ok with x = 5; if x is (x,): pass and no expected diagnostic, with a comment that this does not trigger a SyntaxWarning. These assertions were available at the historical commit; supplied historical evidence does not show their execution."
}
```
