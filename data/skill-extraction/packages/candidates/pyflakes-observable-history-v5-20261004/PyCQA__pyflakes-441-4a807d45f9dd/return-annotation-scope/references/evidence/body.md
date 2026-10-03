# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:441:body",
  "source_id": "PyCQA/pyflakes:441:repair:4a807d45f9dd",
  "available_at": "2019-03-19T10:38:28Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The report imports TypeVar, defines class IdClass with Y = TypeVar('Y'), and defines def id(self, x: Y) -> Y returning x. The reported invocation is pyflakes t.py and the reported output is t.py:7: undefined name 'Y'. The reporter states that MyPy accepts the sample. These are report observations, not newly executed checks."
}
```
