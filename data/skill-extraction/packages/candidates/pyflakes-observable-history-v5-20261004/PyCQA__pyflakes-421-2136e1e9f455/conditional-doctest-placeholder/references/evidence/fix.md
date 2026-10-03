# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:421:fix",
  "source_id": "PyCQA/pyflakes:421:repair:2136e1e9f455",
  "available_at": "2019-07-09T13:37:43Z",
  "kind": "historical_merged_implementation",
  "observation": "In pyflakes/checker.py, doctest setup retained self.scopeStack[0], computed node_offset, and pushed DoctestScope. The merged diff replaced unconditional self.addBinding(None, Builtin('_')) with if '_' not in self.scopeStack[0]: followed by that same addBinding call. Example parsing remained after the conditional. The implementation guards synthetic underscore insertion against an existing module-scope underscore rather than changing getParent. The source record identifies this as a verified resolution; this diff alone does not document historical test execution."
}
```
