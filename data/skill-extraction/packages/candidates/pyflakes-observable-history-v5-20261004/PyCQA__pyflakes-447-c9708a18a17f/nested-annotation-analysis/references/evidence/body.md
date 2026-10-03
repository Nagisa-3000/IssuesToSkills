# Original public reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:447:body",
  "source_id": "PyCQA/pyflakes:447:repair:c9708a18a17f",
  "available_at": "2019-05-28T11:03:15Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter imported Queue from queue and Optional from typing, then used Queue only in the parameter annotation Optional['Queue[int]']. The report showed an unused-import warning for Queue and stated that quoting the entire annotation as 'Optional[Queue[int]]' worked around it. The reported environment was pyflakes 2.1.1 on Python 3.5.2 on Linux. This is the supplied public report; no independent reproduction run transcript is included."
}
```
