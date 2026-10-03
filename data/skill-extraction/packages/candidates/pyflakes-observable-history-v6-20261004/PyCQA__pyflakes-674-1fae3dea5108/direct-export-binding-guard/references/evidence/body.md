# Original report

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:body",
  "source_id": "PyCQA/pyflakes:674:repair:1fae3dea5108",
  "available_at": "2022-01-28T11:43:01Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter installed pyflakes==2.4.0, placed __all__, = (\"fizz\", \"buzz\") in foo.py and ran pyflakes foo.py. The reported traceback reached checker.py at isinstance(source.value, (ast.List, ast.Tuple)) and ended with AttributeError: 'Tuple' object has no attribute 'value'. The report attributed the failure to a source-shape assumption incompatible with tuple or more complicated targets and suggested marking the input invalid. That suggestion was not the merged behavior. This is a reported reproduction, not an independently supplied historical execution log."
}
```
