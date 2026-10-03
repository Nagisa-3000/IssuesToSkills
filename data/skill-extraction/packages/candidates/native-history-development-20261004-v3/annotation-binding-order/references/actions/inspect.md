# Inspect symptom and mechanism

Locate current owners and hashed code anchors. Compare isolated ordinary and annotated self-reference diagnostics, then inspect traversal and binding order. Emit a mechanism-confirmed review only when both symptom and causal mechanism match. Otherwise retain FAIL or UNKNOWN and do not authorize the edit.

This operation is read-only. Its output describes an expected current review, not an already observed result.

```arex-contract-v4
{
  "id": "annotation-binding-order.inspect",
  "intent": "Determine whether premature annotated target registration suppresses the initializer diagnostic.",
  "mechanism": "Compare isolated public probes and inspect traversal and binding order.",
  "semantic_role": "mechanism-confirmation",
  "owner_role": "annotated-assignment-analysis",
  "operation": "Bind current owners and record evidence confirming or rejecting early target registration.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "mechanism-review", "semantic_role": "binding-order-review", "artifact_kind": "review-record", "language": "python", "scope": "annotated-assignment-analysis", "phase": "diagnosis", "state": "mechanism-confirmed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-owner-bindings", "value": "recorded", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-binding-order",
      "instruction": "Compare isolated x = x and x: int = x diagnostics in the pinned current checkout. Inspect whether target registration precedes initializer analysis. Record current owner bindings and hashed anchors; emit a confirmed review only when both mismatch and mechanism are observed.",
      "evidence_refs": ["PyCQA/pyflakes:728:body", "PyCQA/pyflakes:728:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:728"],
  "evidence_refs": ["PyCQA/pyflakes:728:body", "PyCQA/pyflakes:728:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "annotation-binding-order",
  "read_set": ["role:annotated-assignment-analysis", "role:annotation-diagnostic-tests"],
  "write_set": [],
  "exclusions": [
    {"key": "early-target-registration", "value": false, "evaluator": "evidence"}
  ]
}
```
