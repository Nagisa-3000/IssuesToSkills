# Reported reproducer and crash

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:764:body",
  "source_id": "PyCQA/pyflakes:764:repair:e19886e58363",
  "available_at": "2023-01-31T18:26:17Z",
  "kind": "issue_body_as_of_cutoff",
  "observation": "The reporter supplied `test: int`, followed by `test.__dict__`, then a function assigning `test = 1`. Version 3.0.1 reportedly crashed in handleNodeStore at `if used and used[0] is self.scope and name not in self.scope.globals:` with `TypeError: 'bool' object is not subscriptable`. The reporter said version 2.5.0 instead reported undefined name 'test' at the outer load and local variable 'test' assigned to but never used in the function. Removing any of the annotation, attribute load, or function assignment reportedly avoided the exception. These are original report observations; no new execution is asserted."
}
```
