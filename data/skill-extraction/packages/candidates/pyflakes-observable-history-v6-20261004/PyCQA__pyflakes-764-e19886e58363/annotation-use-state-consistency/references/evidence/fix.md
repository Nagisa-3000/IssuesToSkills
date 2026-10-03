# Historical merged assignment change

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:764:fix",
  "source_id": "PyCQA/pyflakes:764:repair:e19886e58363",
  "available_at": "2023-01-31T18:45:58Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, under `if isinstance(binding, Annotation) and not self._in_postponed_annotation:`, the merged implementation replaced `scope[name].used = True` with `scope[name].used = (self.scope, node)`. The following `continue` and branch guard remained unchanged. The supplied diff establishes the scope-and-node representation change, not a historical test-run result."
}
```
