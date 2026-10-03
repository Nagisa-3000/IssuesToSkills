# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:447:body",
  "source_id": "PyCQA/pyflakes:447:repair:c9708a18a17f",
  "available_at": "2019-05-28T11:03:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter used Pyflakes 2.1.1 on Python 3.5.2 on Linux. In a parameter annotation Optional['Queue[int]'], queue.Queue was reported as imported but unused despite being referenced inside the nested string. Quoting the whole annotation as 'Optional[Queue[int]]' was reported as a workaround. The report included a revealed type resolving the Queue element type. These are reported observations, not an independently executed reproduction in this package."
}
```
