# Inspect the binding boundary

Locate the current dispatcher, export consumer, and tests. Compare direct and tuple-target immediate parents. Inspect whether the consumer assumes assignment values, whether dispatch can violate that assumption, and whether ordinary binding remains available.

Record the pinned revision, hashed public code anchors, parent observations, and resolved owner bindings. Do not modify source or tests. Reject a different mechanism rather than forcing this repair.

```arex-contract-v4
{
  "id": "direct-export-binding-guard.inspect",
  "intent": "Establish the current export-binding parent-shape mismatch and semantic owners.",
  "mechanism": "Inspect dispatch and consumer assumptions and compare direct versus destructuring AST parent shapes.",
  "semantic_role": "establish-binding-boundary",
  "owner_role": "name-store-binding-dispatcher",
  "operation": "read-and-probe",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "binding-boundary",
      "semantic_role": "verified-export-dispatch-context",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "mechanism-and-owners-observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-binding-boundary-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-parent-mismatch",
      "instruction": "Record current direct and tuple-target immediate parent types, dispatch conditions, consumer value assumptions, ordinary fallback, owner bindings, revision and hashed anchors. Determine whether the historical mismatch is present; reject an incompatible mechanism.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674"],
  "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "direct-export-binding-guard",
  "read_set": [
    "role:name-store-binding-dispatcher",
    "role:export-binding-handler",
    "role:export-binding-regression-tests"
  ],
  "write_set": []
}
```
