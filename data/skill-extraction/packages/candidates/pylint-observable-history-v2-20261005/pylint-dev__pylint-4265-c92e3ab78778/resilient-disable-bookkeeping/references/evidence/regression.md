# Historical committed regression assertions

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4265:regression",
  "source_id": "pylint-dev/pylint:4265:repair:c92e3ab78778",
  "available_at": "2021-03-30T07:26:03Z",
  "kind": "historical_regression_assertions",
  "observation": "The commit added tests/functional/d/disabled_msgid_in_pylintrc.py with an issue-link docstring and try: f = open('test') followed by except Exception: pass. Its companion .rc file has [MESSAGES CONTROL] and disable=C0111,C0326,W0703 across lines. The fixture contains no annotation expecting broad-except, providing a public configured-suppression regression in the functional harness. These are committed assertions available at the historical revision; historical test execution and CI status are unknown in the supplied core evidence."
}
```
