# Committed assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8559:regression",
  "source_id": "pylint-dev/pylint:8559:repair:2db55f6a4896",
  "available_at": "2023-04-15T01:53:00Z",
  "kind": "historical_regression_assertions",
  "observation": "The added tests/functional/a/arguments_positional_only.py defines name1(param1, /, **kwargs), name2(param1, /, param2, **kwargs), name3(param1=True, /, **kwargs), and name4(param1, **kwargs). Only name1(param1=43) is annotated [no-value-for-parameter]. Controls name1(43), name2(1, param2=False), name3(), and name4(param1=43) have no expected diagnostics. The .rc sets min_pyver=3.8. The .txt assertion is `no-value-for-parameter:11:0:11:16::No value for argument 'param1' in function call:UNDEFINED`. These are committed assertions available at the historical revision; historical execution/CI status is unknown."
}
```
