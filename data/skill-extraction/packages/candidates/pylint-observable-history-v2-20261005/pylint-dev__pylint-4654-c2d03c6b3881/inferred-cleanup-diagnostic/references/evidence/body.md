# Public reproduction and version observations

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:4654:body",
  "source_id": "pylint-dev/pylint:4654:repair:c2d03c6b3881",
  "available_at": "2021-07-01T17:09:52Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report passed five open(...) calls directly to stack.enter_context(...) inside with contextlib.ExitStack() as stack and showed five R1732 consider-using-with warnings, one for each allocation. Expected behavior was no such warnings. The reporter listed Pylint 3.0.0-a4 and 2.9.3 with astroid 2.6.2 as affected, and Pylint 2.8.3 with astroid 2.5.6 as unaffected, on Python 3.8.9. These are reporter observations, not version comparisons executed by the authored Skill."
}
```
