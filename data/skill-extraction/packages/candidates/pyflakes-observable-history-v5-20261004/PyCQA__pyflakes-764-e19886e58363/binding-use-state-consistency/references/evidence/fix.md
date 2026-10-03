# Merged producer representation repair

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:764:fix",
  "source_id": "PyCQA/pyflakes:764:repair:e19886e58363",
  "available_at": "2023-01-31T18:45:58Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py changed `scope[name].used = True` to `scope[name].used = (self.scope, node)` inside `if isinstance(binding, Annotation) and not self._in_postponed_annotation:`. The following `continue` remained unchanged. This is the supplied implementation fact for the verified repair; the diff itself does not report historical test execution."
}
```
