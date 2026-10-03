# Merged insertion guard

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:421:fix",
  "source_id": "PyCQA/pyflakes:421:repair:2136e1e9f455",
  "available_at": "2019-07-09T13:37:43Z",
  "kind": "historical_merged_implementation",
  "observation": "The supplied merged diff in pyflakes/checker.py retains self.scopeStack = [self.scopeStack[0]], computes node_offset, and pushes DoctestScope. It replaces unconditional self.addBinding(None, Builtin('_')) with that insertion nested under if '_' not in self.scopeStack[0]:. Parsing each doctest example remains after this guard. The implementation therefore skips the synthetic binding when the module scope already contains underscore and retains insertion otherwise. The diff contains no historical execution log."
}
```
