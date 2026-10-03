# Inspect binding and annotation context

Read the current binding constructor, annotated-assignment visitor, load resolution, annotation context manager, and relevant tests. This operation does not change checkout contents.

Distinguish no-value declarations from assignments with values. Determine whether quoted annotations and future annotations are already modeled separately from eager annotations. Record current public reproductions before deciding whether an edit is needed.

```arex-contract-v4
{
  "id": "workflow:verified-history:be71c3f9e9544046d28904cd:inspect",
  "intent": "Establish current applicability and semantic owner bindings.",
  "mechanism": "Read binding classification and lookup gates, then probe the public annotation-context matrix.",
  "semantic_role": "annotation-resolution-inspection",
  "owner_role": "annotation_binding_owner",
  "operation": "Locate current semantic owners, inspect the declaration/load/context paths and regression ownership, and record evidence without modifying code.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "resolution_review",
      "semantic_role": "annotation-resolution-review",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "resolution-owners-located", "value": true, "evaluator": "evidence"},
    {"key": "resolution-mechanism-compatible", "value": true, "evaluator": "evidence", "description": "Current public review supports distinct annotation-only bindings and postponed lookup as the relevant mechanism."}
  ],
  "preserves": [
    {"key": "ordinary-value-resolution-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unused-variable-accounting-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-context-matrix",
      "instruction": "Review current owners and probe no-value T declarations in bare, quoted and future annotations. Record observed diagnostics and ordinary-load behavior; do not edit during this operation.",
      "evidence_refs": ["PyCQA/pyflakes:486:body", "PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:annotation_binding_owner", "role:annotation_regression_owner"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:486:repair:5fc37cbda5bf"],
  "evidence_refs": ["PyCQA/pyflakes:486:body", "PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:be71c3f9e9544046d28904cd"
}
```

A missing owner or UNKNOWN mechanism yields an incomplete review, not the expected successful effects above. Locate and probe further or stop.
