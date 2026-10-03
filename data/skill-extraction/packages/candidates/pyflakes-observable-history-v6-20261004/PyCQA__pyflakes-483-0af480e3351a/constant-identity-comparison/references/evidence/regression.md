# Historical regression assertions

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:483:regression",
  "source_id": "PyCQA/pyflakes:483:repair:0af480e3351a",
  "available_at": "2020-02-17T19:43:55Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff in pyflakes/test/test_is_literal.py added test_is_tuple_constant, expecting IsLiteral for x = 5 followed by if x is (): pass; test_is_tuple_constant_containing_constants, expecting IsLiteral for if x is (1, '2', True, (1.5, ())): pass; and test_is_tuple_containing_variables_ok, expecting no diagnostic for if x is (x,): pass. The last test comment noted that the expression was a bit nonsensical but did not trigger a SyntaxWarning. Supplied surrounding test context included an IsLiteral assertion for if 4 < x is 'foo': pass. These are assertions available at the historical commit, not evidence of a historical test execution."
}
```
