# Inspect dispatch and parent lifecycle

Read current owners and all relevant call sites. Compare early augmented-assignment dispatch with ordinary traversal and identify how parent metadata is initialized. If safely available, capture the public reproduction. Make no source edits.

The confirmed output is conditional: if timing or parent semantics remain unknown, record uncertainty rather than emitting a confirmed diagnosis.

```arex-contract-v4
{
  "id": "workflow:verified-history:73c1883f7ed05d43025127fa:inspect",
  "intent": "Establish whether early load dispatch needs parent context before traversal metadata exists.",
  "mechanism": "Compare load call order, metadata initialization, and caller-owned parent semantics.",
  "semantic_role": "parent-context-diagnosis",
  "owner_role": "load-analysis-owner",
  "operation": "Read current bound owners and callers, locate parent initialization and the parent-sensitive branch, and record public anchors and observations without source edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosis",
      "semantic_role": "parent-context-diagnosis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "bound-load-analysis-and-callers",
      "phase": "pre-edit",
      "state": "confirmed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:load-analysis-owner",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The load-analysis owner resolves to a symbol in the current checkout."
    }
  ],
  "effects": [
    {"key": "parent-context-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "caller-parent-semantics-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-load-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "builtin-print-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "augmented-value-target-order-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-parent-lifecycle",
      "instruction": "Record public anchors showing early load before target parent initialization, the failing parent-sensitive branch, and the correct parent available at each caller. Confirm no source edits. Unknown facts leave applicability UNKNOWN; contrary facts reject the mechanism.",
      "evidence_refs": ["PyCQA/pyflakes:744:body", "PyCQA/pyflakes:744:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:load-analysis-owner",
    "role:early-load-dispatch-owner",
    "role:ordinary-load-dispatch-owner",
    "role:regression-test-owner"
  ],
  "write_set": [],
  "exclusions": [
    {"key": "caller-parent-semantics-confirmed", "value": false, "evaluator": "evidence"}
  ],
  "source_ids": ["PyCQA/pyflakes:744:repair:e0d7a6be8959"],
  "evidence_refs": ["PyCQA/pyflakes:744:body", "PyCQA/pyflakes:744:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:73c1883f7ed05d43025127fa"
}
```

The effects and output state are intended successful postconditions, not claims of execution. Preservation declarations are retained by any composed plan; inspection itself has no source side effects.
