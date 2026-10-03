# Inspect applicability and current owners

Locate the classifier, comparison handler, diagnostic text, and regression tests in the pinned public checkout. Inspect supported Python AST versions and chain traversal. Probe empty tuples, nested all-constant tuples, variable-containing tuples, singleton constants, and existing scalar literals.

Record actual observations separately from desired behavior. Bind the Oracle to current public commands. The empty argv below is a binding placeholder, not an executable historical command.

```arex-contract-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:inspect",
  "intent": "Establish current applicability, AST representations, and semantic owner bindings.",
  "mechanism": "Read classification and comparison traversal and probe public literal examples.",
  "semantic_role": "classification-gap-inspection",
  "owner_role": "identity_comparison_checker",
  "operation": "Locate current owners, inspect supported AST shapes, and record public diagnostic behavior.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "classification_review",
      "semantic_role": "identity-classification-review",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "identity-literal-diagnostic",
      "phase": "pre-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-checkout-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "classification-gap-assessed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-code-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-gap",
      "instruction": "Record current owner bindings, hashed anchors, and supported AST shapes. Observe diagnostic behavior for empty tuples, nested constant tuples, variable-containing tuples, singleton constants, and scalar literals; distinguish observations from expected behavior.",
      "evidence_refs": ["PyCQA/pyflakes:483:body", "PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:constant_classifier", "role:identity_comparison_checker", "role:identity_diagnostic", "role:identity_regression_tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "evidence_refs": ["PyCQA/pyflakes:483:body", "PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f"
}
```
