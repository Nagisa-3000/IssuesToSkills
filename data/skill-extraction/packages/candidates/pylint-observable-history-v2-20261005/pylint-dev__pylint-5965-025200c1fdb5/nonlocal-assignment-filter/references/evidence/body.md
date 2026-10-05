# Original reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:5965:body",
  "source_id": "pylint-dev/pylint:5965:repair:025200c1fdb5",
  "available_at": "2022-03-24T23:55:38Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report initializes myvar = 1 in outer(), declares nonlocal myvar in inner(), reads it with print(\"A\", myvar) in a try block, raises IOError, then reads and increments myvar in the handler. It reports E0601 at the first read and expects no Pylint errors. The stated command is pylint a.py; the displayed diagnostic uses test.py. Reported versions are Pylint 2.13.0, astroid 2.11.1 and Python 3.7.12 on Ubuntu 18.04. These are reporter observations, not independently observed Skill outcomes."
}
```
