# Reported reproduction

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8613:body",
  "source_id": "pylint-dev/pylint:8613:repair:f223c6de3a39",
  "available_at": "2023-04-24T12:57:46Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter defined class X with __index__(self) returning 1 and ran pylint x.py. Reported output was x.py:2:4: W3201: Bad or misspelled dunder method name __index__. (bad-dunder-name). Expected behavior was no lint. The report linked Python operator.__index__ documentation and listed Pylint 2.17.2, astroid 2.15.4, and Python 3.10.11. This is reported output; independent historical CI execution is unknown."
}
```
