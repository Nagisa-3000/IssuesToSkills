# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:633:fix",
  "source_id": "PyCQA/pyflakes:633:repair:e02336c3d47c",
  "available_at": "2022-05-30T16:20:13Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged diff in pyflakes/checker.py introduced NamedExprAssignment as an Assignment subclass. Stored names with parent_stmt of ast.NamedExpr were classified as NamedExprAssignment under PY38_PLUS. In addBinding, the existing annotation guard remained; insertion initialized cur_scope_pos = -1 and decremented it while the value was a NamedExprAssignment and the selected scopeStack entry was a GeneratorScope, then stored the binding at that selected scope. Thus ordinary bindings retained current-scope insertion, while assignment-expression bindings skipped consecutive generator scopes. The diff's comment attributes the destination to the scope in which the outermost generator is defined, per PEP 572. This records merged implementation, not a historical test-run result."
}
```
