# Historical merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:760:fix",
  "source_id": "PyCQA/pyflakes:760:repair:e9324649874a",
  "available_at": "2023-01-12T16:26:28Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py added Definition.redefines(self, other), returning super().redefines(other) or (isinstance(other, Assignment) and self.name == other.name). Definition is documented as a binding defining a function or class. The repair preserves the inherited predicate and extends recognition to same-name Assignment bindings on the definition side. The supplied diff contains no execution log."
}
```
