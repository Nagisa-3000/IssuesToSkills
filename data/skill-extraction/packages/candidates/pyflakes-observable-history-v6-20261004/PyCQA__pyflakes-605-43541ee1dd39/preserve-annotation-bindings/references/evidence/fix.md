# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:605:fix",
  "source_id": "PyCQA/pyflakes:605:repair:43541ee1dd39",
  "available_at": "2021-01-05T16:04:39Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, the unconditional self.scope[value.name] = value was replaced with if value.name not in self.scope or not isinstance(value, Annotation): followed by that assignment. The added comment says not to treat annotations as assignments if there is an existing value in scope. The shown preceding propagation value.used = self.scope[value.name].used remained. This is merged implementation evidence; it does not itself record test execution."
}
```
