# Reported reproduction

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:body",
  "source_id": "PyCQA/pyflakes:674",
  "available_at": "2022-01-28T11:43:01Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter specified pyflakes==2.4.0, a foo.py containing __all__, = (\"fizz\", \"buzz\",), and the historical command pyflakes foo.py. The reported trace accessed source.value in checker.py and ended with AttributeError: 'Tuple' object has no attribute 'value'. The reporter attributed this to source-shape assumptions and proposed marking the code invalid. That proposal is not the merged resolution. This is a historical report, not a newly executed reproduction."
}
```
