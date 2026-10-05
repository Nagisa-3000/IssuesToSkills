# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5406:regression",
  "source_id": "pylint-dev/pylint:5406:repair:3b744d180e5e",
  "available_at": "2022-04-07T08:43:11Z",
  "kind": "historical_regression_assertions",
  "observation": "Committed fixtures add bare kwargs documentation for **kwargs in Google and NumPy, escaped *args documentation in Google using a doubled source backslash, and raw Sphinx docstrings documenting *args and **kwargs as bare args and kwargs. Expected outputs add no missing/differing parameter warnings for these positive cases. Existing genuine missing variadic warnings remain, and unrelated inconsistent-return warnings remain for the new Sphinx fixtures. These are historical committed assertions, not proof of historical execution. Later changed-test-only qualification is validation-only provenance."
}
```
