# Original public reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:728:body",
  "source_id": "PyCQA/pyflakes:728:repair:4dcd92e45efe",
  "available_at": "2022-09-08T20:06:47Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The original report showed `pyflakes /dev/stdin <<< 'x = x'` emitting `/dev/stdin:1:5: undefined name 'x'`, while `pyflakes /dev/stdin <<< 'x: int = x'` emitted no diagnostic. These are reporter-supplied console observations. The evidence does not establish behavior in other scopes or a current execution result."
}
```
