# Committed regression assertion

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8613:regression",
  "source_id": "pylint-dev/pylint:8613:repair:f223c6de3a39",
  "available_at": "2023-04-24T18:26:19Z",
  "kind": "historical_regression_assertions",
  "observation": "The committed diff added __index__(self), returning 1, to class Apples in tests/functional/ext/bad_dunder/bad_dunder_name.py without an expected bad-dunder-name annotation on the method. This is a no-warning regression assertion available at the repair commit, not a historical pass claim. Historical execution and CI results are unknown; later independent qualification is validation-only."
}
```
