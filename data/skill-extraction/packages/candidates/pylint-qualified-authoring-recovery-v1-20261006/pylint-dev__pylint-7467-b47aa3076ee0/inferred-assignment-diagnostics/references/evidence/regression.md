# Historical committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7467:regression",
  "source_id": "pylint-dev/pylint:7467:repair:b47aa3076ee0",
  "available_at": "2022-09-16T14:00:37Z",
  "kind": "historical_regression_assertions",
  "observation": "The supplied diff in tests/functional/i/invalid/invalid_class_object.txt changes five expected invalid-class-object message texts. Line 20 expects Invalid assignment to '__class__'. Should be a class definition but got a 'Instance'; lines 21, 50, 58, and 62 use the same template with 'Const'. Symbols, source spans, object labels, and INFERENCE confidence are unchanged. The latter three object labels are Pylint7429Good.class_defining_function_bad, Pylint7429Good.class_defining_function_bad_inverted, and Pylint7429Good.class_defining_function_complex_bad. These are committed assertions available at the historical revision; historical execution is unknown."
}
```
