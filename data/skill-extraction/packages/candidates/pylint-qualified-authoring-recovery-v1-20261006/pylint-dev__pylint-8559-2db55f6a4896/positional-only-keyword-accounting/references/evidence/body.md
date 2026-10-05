# Reported reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8559:body",
  "source_id": "pylint-dev/pylint:8559:repair:2db55f6a4896",
  "available_at": "2023-04-10T01:43:50Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report defines required_positional_with_var_kwargs(a, /, **_kwargs), returning a, and calls required_positional_with_var_kwargs(a=43). With missing-function-docstring and missing-module-docstring disabled, reported command `pylint a.py` produces nothing; expected behavior is no-value-for-parameter. Reported versions are Pylint 3.0.0b1, astroid 2.16.0dev0, and Python 3.8.10. This is reported output, not newly executed Skill validation."
}
```
