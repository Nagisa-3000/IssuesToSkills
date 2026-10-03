# Guard specialized dispatch

Require an immediate assignment-statement parent in addition to the existing module-scope and `__all__` checks. The evidenced Python realization accepts `ast.Assign`, `ast.AugAssign`, and `ast.AnnAssign`.

Do not replace this with an enclosing-statement check or rewrite AST targets. Preserve earlier classifier branches and ordinary fallback. The contract describes intended effects, not observed execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
  "intent": "Exclude indirect target containers from specialized export assignment analysis.",
  "mechanism": "Conjoin an immediate-parent assignment-type check with specialized dispatch conditions.",
  "semantic_role": "specialized-dispatch-guard",
  "owner_role": "export-binding-dispatch",
  "operation": "Edit the classifier so specialized module __all__ binding requires an immediate Assign, AugAssign or AnnAssign parent, retaining existing name, scope, earlier branches and fallback behavior.",
  "kind": "edit",
  "inputs": [
    {"name": "located-boundary", "semantic_role": "export-repair-candidate", "artifact_kind": "checkout-with-observations", "language": "python", "scope": "module-export-analysis", "phase": "current-repair", "state": "located"}
  ],
  "outputs": [
    {"name": "guarded-candidate", "semantic_role": "export-repair-candidate", "artifact_kind": "checkout-with-observations", "language": "python", "scope": "module-export-analysis", "phase": "current-repair", "state": "guarded"}
  ],
  "preconditions": [
    {"key": "binding-boundary-observed", "value": true, "evaluator": "evidence"},
    {"key": "current-parent-contract-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:export-binding-dispatch", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "special-export-dispatch-direct-parent-only", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-export-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-direct-parent-gate",
      "instruction": "Review the diff for the immediate-parent gate, retained name and scope conditions, and unchanged surrounding classification. Require explicit public validation; diff review alone does not establish repair success.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"],
  "read_set": ["role:export-binding-dispatch", "role:export-binding-constructor"],
  "write_set": ["role:export-binding-dispatch"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d"
}
```
