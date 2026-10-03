# Original reproduction and consumer failure

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:764:body",
  "source_id": "PyCQA/pyflakes:764:repair:e19886e58363",
  "available_at": "2023-01-31T18:26:17Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied `test: int`, followed by `test.__dict__`, and a function containing `test = 1`. Version 3.0.1 reportedly crashed in handleNodeStore at `if used and used[0] is self.scope and name not in self.scope.globals:` with TypeError: 'bool' object is not subscriptable. Version 2.5.0 reportedly emitted undefined name 'test' and local variable 'test' is assigned to but never used. The reporter stated that removing the annotation, attribute read, or function assignment avoided the exception. These are reported observations; no independent historical run transcript was supplied."
}
```
