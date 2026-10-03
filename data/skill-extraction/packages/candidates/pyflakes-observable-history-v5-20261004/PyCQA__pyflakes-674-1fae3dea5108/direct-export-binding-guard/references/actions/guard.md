# Guard specialized export-binding dispatch

Retain the special identifier and module-scope conditions. Add an immediate-parent type restriction at the dispatch point. In the evidenced Python AST realization, supported parents are `ast.Assign`, `ast.AugAssign`, and `ast.AnnAssign`.

Do not catch the downstream attribute error as a substitute. Do not flatten an unpacking target into a synthetic direct assignment.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
  "intent": "Prevent indirect targets from entering a constructor that expects an assignment statement.",
  "mechanism": "Add a supported immediate-parent type predicate to special export dispatch.",
  "semantic_role": "special-binding-guard",
  "owner_role": "python-binding-dispatch",
  "operation": "Restrict module-level special export binding to direct supported assignment parents and leave remaining dispatch branches intact.",
  "kind": "edit",
  "inputs": [
    {"name": "boundary", "semantic_role": "export-binding-boundary", "artifact_kind": "review", "language": "python", "scope": "current-checkout", "phase": "inspection", "state": "established"}
  ],
  "outputs": [
    {"name": "guarded-implementation", "semantic_role": "export-dispatch-implementation", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "candidate", "state": "modified"}
  ],
  "preconditions": [
    {"key": "role:python-binding-dispatch", "value": true, "evaluator": "symbol_exists"},
    {"key": "constructor-requires-supported-assignment-parent", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-fallback-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "indirect-target-special-export-binding", "value": false, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-module-export-processing", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-binding-fallback", "value": "preserved", "evaluator": "evidence"},
    {"key": "special-name-and-module-scope-restrictions", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "guard-diff-review",
      "instruction": "Review the candidate diff: specialization requires a supported immediate assignment parent, existing name/scope restrictions remain, and indirect targets retain ordinary fallback.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d",
  "read_set": ["role:python-binding-dispatch", "role:python-export-binding-constructor"],
  "write_set": ["role:python-binding-dispatch"],
  "invalidates": ["export-dispatch-behavior", "export-diagnostic-suite-results"]
}
```

Effects describe the intended candidate behavior, not an observed successful execution. The validate Action must check this edit publicly.
