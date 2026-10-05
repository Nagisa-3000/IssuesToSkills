# Committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6594:regression",
  "source_id": "pylint-dev/pylint:6594:repair:f6479fd320e7",
  "available_at": "2022-05-13T18:48:10Z",
  "kind": "historical_regression_assertions",
  "observation": "The diff changed tests/functional/g/generated_members.py from the print_function future import to annotations and added `print(Klass.X)  # [no-member]`, `var: \"Klass.X\"`, and `var2: Klass.X`. The expected-output file retained `no-member:13:6:13:18::Instance of 'Klass' has no 'spam' member:INFERENCE` and added `no-member:26:6:26:13::Class 'Klass' has no 'X' member:INFERENCE` for runtime access, with no annotation diagnostic. These are assertions available at the historical commit; original historical execution is unknown. Later independent qualification is separate validation-only provenance."
}
```
