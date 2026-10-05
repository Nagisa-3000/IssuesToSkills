# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7461:regression",
  "source_id": "pylint-dev/pylint:7461:repair:fb30fe09d74d",
  "available_at": "2022-09-16T07:24:19Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed functional fixture adds MyClass2, initializes self.attribute = {}, and in my_method loops 'for key in self.attribute', assigns 'tmp = self.attribute.copy()', then 'tmp[key] = None'. The method says 'This should not raise, as a copy was made' and contains no expected mutation diagnostic. The supplied surrounding context retains the instance-list deletion expectation '# [modified-iterating-list]'. These are committed assertions; historical execution and CI outcomes are unknown."
}
```
