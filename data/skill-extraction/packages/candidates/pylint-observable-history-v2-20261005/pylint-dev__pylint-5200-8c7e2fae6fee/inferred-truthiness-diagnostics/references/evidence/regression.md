# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5200:regression",
  "source_id": "pylint-dev/pylint:5200:repair:8c7e2fae6fee",
  "available_at": "2021-10-29T19:44:19Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff adds func5 in tests/functional/t/ternary.py, assigning falsy_value=False and returning condition and falsy_value or false_value with a simplify-boolean-expression annotation. tests/functional/t/ternary.txt adds the line-39 func5 expectation 'Boolean expression may be simplified to false_value'. Existing func4 assigns truth_value=42 and retains consider-using-ternary at line 33. These are committed historical assertions; historical execution or CI success is not supplied."
}
```
