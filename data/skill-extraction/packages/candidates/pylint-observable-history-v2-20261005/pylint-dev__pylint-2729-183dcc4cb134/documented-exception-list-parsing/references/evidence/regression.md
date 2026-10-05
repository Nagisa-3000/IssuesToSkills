# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:2729:regression",
  "source_id": "pylint-dev/pylint:2729:repair:183dcc4cb134",
  "available_at": "2019-10-17T07:10:45Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff adds test_find_multiple_sphinx_raises and test_find_multiple_google_raises. Each fixture documents RuntimeError singly and NameError, OSError, ValueError together, includes corresponding raises, extracts the marked NameError raise node, and asserts no messages when visit_raise is called on that node. These assertions directly check NameError in both styles, not independent visits to every fixture raise. Historical execution status is unknown; later qualification is separate validation provenance."
}
```
