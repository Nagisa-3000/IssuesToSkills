# Inspect the binding boundary

Read current code and public tests; do not edit source or tests. Trace direct and unpacked stored names to their immediate parents, and inspect the specialized consumer's assignment-value expectation. Record anchors, owner bindings, and semantic observations. Historical symptoms are hypotheses until reproduced or corroborated in the current checkout.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:inspect",
  "intent": "Determine whether the current defect matches the supported export-dispatch boundary.",
  "mechanism": "Inspect immediate AST parent relationships and the specialized assignment-value consumer.",
  "semantic_role": "binding-boundary-inspection",
  "owner_role": "export-binding-dispatch",
  "operation": "Read dispatch, parent-link construction, consumer and public tests without changing source or tests; bind owners and record compatible parent and harness contracts.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "located-boundary", "semantic_role": "export-repair-candidate", "artifact_kind": "checkout-with-observations", "language": "python", "scope": "module-export-analysis", "phase": "current-repair", "state": "located"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "binding-boundary-observed", "value": true, "evaluator": "evidence"},
    {"key": "current-parent-contract-compatible", "value": true, "evaluator": "evidence", "description": "Emit only after current review establishes immediate-parent semantics and the supported mismatch."},
    {"key": "current-diagnostic-harness-compatible", "value": true, "evaluator": "evidence", "description": "Emit only after locating public diagnostic assertions suitable for the regression."}
  ],
  "preserves": [
    {"key": "direct-export-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-parent-contract",
      "instruction": "Inspect or publicly probe immediate parent types for direct and tuple-target assignments. Confirm the specialized consumer expects an assignment value, locate ordinary fallback and public diagnostic tests, and record anchors without editing source or tests. Incompatible or unknown findings must not emit compatibility effects.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
  "read_set": ["role:export-binding-dispatch", "role:export-binding-constructor", "role:export-binding-tests"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d"
}
```
