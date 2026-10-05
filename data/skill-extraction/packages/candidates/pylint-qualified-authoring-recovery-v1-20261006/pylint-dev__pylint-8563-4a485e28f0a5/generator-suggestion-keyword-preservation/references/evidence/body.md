# Original report

```arex-evidence-v4
{
  "id": "pylint-dev/pylint:8563:body",
  "source_id": "pylint-dev/pylint:8563:repair:4a485e28f0a5",
  "available_at": "2023-04-10T17:03:58Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used pylint 2.17.2, astroid 2.15.2, and Python 3.10.10. For min([i for i in range(len(line)) if line[i] not in whitespaces], default=0), R1728 suggested min(i for i in range(len(line)) if line[i] not in whitespaces), omitting default=0. The reporter requested no error. The reported command was pylint src/hidden_type/util.py; it is historical context, not a current command binding. The report is not evidence that the later committed regression was executed."
}
```
