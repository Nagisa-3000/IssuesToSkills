# Historical assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8120:regression",
  "source_id": "pylint-dev/pylint:8120:repair:660405e62182",
  "available_at": "2023-01-28T09:29:29Z",
  "kind": "historical_regression_assertions",
  "observation": "The functional fixture added async test_a and test_b assigning data to a list of dictionaries and a dictionary, respectively. Class AsyncFunctions added async funtion1 and funtion2 assigning potato to 1 and {}, respectively. These additions have no redefined-variable-type expectation; their comment explicitly states the message should not be emitted. Existing diff context retains an expected warning for var4 changing from 2. to 'baz'. These are assertions available at the historical commit; historical execution is unknown."
}
```
