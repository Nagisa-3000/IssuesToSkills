# Merged implementation

```arex-evidence-v4
{
  "id": "PyCQA/pyflakes:633:fix",
  "source_id": "PyCQA/pyflakes:633:repair:e02336c3d47c",
  "available_at": "2022-05-30T16:20:13Z",
  "kind": "historical_merged_implementation",
  "observation": "The merged pyflakes/checker.py diff adds NamedExprAssignment as an Assignment subclass. Target classification selects it when PY38_PLUS and parent_stmt is ast.NamedExpr. Binding insertion initializes cur_scope_pos = -1, decrements it while the value is NamedExprAssignment and scopeStack[cur_scope_pos] is GeneratorScope, then writes into that selected scope. The comment attributes this to PEP 572 and the scope in which the outermost generator is defined. The existing annotation guard remains. The authoritative source marks this repair as verified resolution; this implementation entry itself supplies no test execution transcript."
}
```
