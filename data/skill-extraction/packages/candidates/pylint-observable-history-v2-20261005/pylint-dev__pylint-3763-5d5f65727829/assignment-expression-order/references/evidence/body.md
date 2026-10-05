# Historical reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:3763:body",
  "source_id": "pylint-dev/pylint:3763:repair:5d5f65727829",
  "available_at": "2020-08-04T14:22:42Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter evaluates `foo if (foo := 3 - 2) > 0 else 0` on Python 3.8 and reports result 1. Running `pylint somefile.py` reportedly emits E0601: Using variable 'foo' before assignment (used-before-assignment). Reported versions are Pylint 2.5.3, astroid 2.4.2, and Python 3.8.3. These are report observations, not independently executed Skill probes."
}
```
