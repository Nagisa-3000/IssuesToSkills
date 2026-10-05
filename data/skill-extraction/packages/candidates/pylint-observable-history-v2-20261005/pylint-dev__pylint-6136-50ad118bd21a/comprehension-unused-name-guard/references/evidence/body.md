# Original public report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:6136:body",
  "source_id": "pylint-dev/pylint:6136:repair:50ad118bd21a",
  "available_at": "2022-04-02T13:09:45Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied a function assigning `project_id = []` and then using `assert (project_id > 0 for project_id in project_id)`. The reported command `pylint z.py` emitted `z.py:2:4: W0612: Unused variable 'project_id' (unused-variable)`. Expected behavior was no message. The report attributed the regression to #6073 and said it was found by diffing primer package messages. This is reported historical output, not an executed Skill case."
}
```
