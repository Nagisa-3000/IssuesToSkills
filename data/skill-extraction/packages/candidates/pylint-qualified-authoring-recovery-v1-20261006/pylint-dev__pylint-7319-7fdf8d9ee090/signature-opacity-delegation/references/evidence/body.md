# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:7319:body",
  "source_id": "pylint-dev/pylint:7319:repair:7fdf8d9ee090",
  "available_at": "2022-08-18T09:00:00Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter defined CustomError(Exception) with __init__(self, message=\"default\") calling super().__init__(message). Running `pylint a.py` reportedly emitted W0235, useless-super-delegation, at a.py:3:4. The expected behavior was no warning because the override introduced a default value. Reported versions were Pylint 2.14.5, astroid 2.11.7, and Python 3.9.13 on macOS 12.4. This is reported reproduction output, not independently observed historical CI."
}
```
