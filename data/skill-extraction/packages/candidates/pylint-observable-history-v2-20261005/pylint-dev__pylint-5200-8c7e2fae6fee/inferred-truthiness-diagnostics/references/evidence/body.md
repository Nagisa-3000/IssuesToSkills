# Reported reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5200:body",
  "source_id": "pylint-dev/pylint:5200:repair:8c7e2fae6fee",
  "available_at": "2021-10-22T13:24:41Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report assigns a=True, b=False, c=True. It shows (a and b) or c yielding True and the suggested b if a else c yielding False. The reported command pylint test.py emitted R1706 consider-using-ternary at line 6, suggesting b if a else c. The environment lists Pylint 2.11.1, astroid 2.8.0, Python 3.9.7, and Fedora 34. This is reported reproduction evidence, not independently recorded historical CI execution."
}
```
