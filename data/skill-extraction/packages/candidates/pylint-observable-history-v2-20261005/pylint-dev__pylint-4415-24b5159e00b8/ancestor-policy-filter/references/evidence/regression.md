# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4415:regression",
  "source_id": "pylint-dev/pylint:4415:repair:24b5159e00b8",
  "available_at": "2021-04-28T19:22:56Z",
  "kind": "historical_regression_assertions",
  "observation": "The ancestry fixture imported MutableSequence and added a minimal ItemSequence subclass implementing required methods without an expected too-many-ancestors annotation. Existing positive controls Iiii and Jjjj retained that warning. Expected output changed from Iiii at line 20 with 9/7 and Jjjj at line 23 with 10/7 to line 21 with 8/7 and line 24 with 9/7. These are assertions committed with the repair; contemporaneous test execution is not established by the supplied historical evidence."
}
```
