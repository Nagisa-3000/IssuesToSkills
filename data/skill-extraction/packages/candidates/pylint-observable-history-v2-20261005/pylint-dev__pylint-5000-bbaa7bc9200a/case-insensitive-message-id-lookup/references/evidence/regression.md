# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5000:regression",
  "source_id": "pylint-dev/pylint:5000:repair:bbaa7bc9200a",
  "available_at": "2021-09-14T07:56:58Z",
  "kind": "historical_regression_assertions",
  "observation": "The historical fixture tests/functional/u/use/use_symbolic_message_instead.py changes line 2 from enable=C0111 to enable=c0111,w0223 with two use-symbolic-message-instead annotations. Its companion expected-output file asserts separate line-2 recommendations retaining 'c0111' and 'w0223' and suggesting enable=missing-docstring and enable=abstract-method respectively. Other uppercase recommendations and the invalid T1234 bad-option-value assertion remain. The expected-output diff also adds HIGH confidence suffixes. These are committed assertions; original historical execution is unknown and authored Skill evaluations are unexecuted."
}
```
