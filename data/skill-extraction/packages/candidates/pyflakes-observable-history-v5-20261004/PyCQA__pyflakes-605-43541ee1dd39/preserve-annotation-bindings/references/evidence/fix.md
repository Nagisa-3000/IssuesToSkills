# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:605:fix",
  "source_id": "PyCQA/pyflakes:605:repair:43541ee1dd39",
  "available_at": "2021-01-05T16:04:39Z",
  "kind": "historical_merged_implementation",
  "observation": "In historical pyflakes/checker.py, unconditional self.scope[value.name] = value was replaced by the guard if value.name not in self.scope or not isinstance(value, Annotation): followed by self.scope[value.name] = value. The added comment says not to treat annotations as assignments if an existing value is in scope. The preceding value.used propagation remains unchanged in the supplied diff. The guard still inserts annotations for absent names and still replaces entries for non-Annotation bindings."
}
```
