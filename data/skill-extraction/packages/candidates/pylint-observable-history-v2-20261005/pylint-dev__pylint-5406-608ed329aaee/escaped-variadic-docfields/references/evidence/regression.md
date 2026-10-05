# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5406:regression",
  "source_id": "pylint-dev/pylint:5406:repair:608ed329aaee",
  "available_at": "2021-12-03T15:35:29Z",
  "kind": "historical_regression_assertions",
  "observation": "The Sphinx functional fixture and expected-output diff added missing-param-doc expectations for unescaped ':param *args:' and ':param **kwargs:' cases. New raw-docstring cases with ':param \\*args:' and ':param \\**kwargs:' retained inconsistent-return-statements expectations without missing-param-doc. Existing absent-variadic-documentation cases continued to expect missing-param-doc, and unrelated expectations remained with adjusted locations. These are committed assertions, not evidence of historical CI execution. Contemporary qualification is separate from these historical assertions and from newly authored Skill evaluations."
}
```
