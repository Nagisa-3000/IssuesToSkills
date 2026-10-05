# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5817:regression",
  "source_id": "pylint-dev/pylint:5817:repair:67055f422132",
  "available_at": "2022-02-17T15:27:29Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff for tests/functional/u/used/used_before_assignment_issue626.py adds main5: try: print([e for e in range(3) if e]); except ValueError as e: print(e). No used-before-assignment annotation is added to this case. The preceding context retains print(e) with a [used-before-assignment] annotation outside the handler. These are committed target and adjacent-behavior assertions; historical execution of them is unknown."
}
```
