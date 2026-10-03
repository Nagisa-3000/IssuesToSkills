# Reported reproduction and failure

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:674:body",
  "source_id": "PyCQA/pyflakes:674:repair:1fae3dea5108",
  "available_at": "2022-01-28T11:43:01Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter installed pyflakes==2.4.0, put `__all__, = (\"fizz\", \"buzz\",)` in foo.py, and ran `pyflakes foo.py`. The reported traceback reached pyflakes/checker.py at `if isinstance(source.value, (ast.List, ast.Tuple)):` and raised `AttributeError: 'Tuple' object has no attribute 'value'`. The reporter attributed this to an unsupported target shape and suggested marking it invalid. This is a reported failure, not an independently executed reproduction in this bundle."
}
```
