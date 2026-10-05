# Diagnose default-collection omission

Locate the current classifier, its callers, and public regression owner. Read without modifying source. Compare public examples of keyword-only default capture, positional default capture, and genuine body capture.

Inspect the default collections, their absent-entry representation, and matching by AST-node identity. Record real bindings and hashed anchors. Emit a confirmed diagnosis only when public observations establish the omission and compatible representation. UNKNOWN remains probe-only; a different mechanism rejects this repair.

```arex-contract-v4
{
  "id": "workflow:verified-history:d2dc67ed68c41ff7c06c4c32:diagnose",
  "intent": "Determine whether omitted keyword-only defaults cause the warning.",
  "mechanism": "Compare warning locations and AST default membership with classifier traversal.",
  "semantic_role": "default-binding-diagnosis",
  "owner_role": "default-expression-classifier",
  "operation": "Read bound semantic owners and run current public probes without modifying source files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosis",
      "semantic_role": "default-binding-diagnosis",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "compatible-omission-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "positional-default-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-closure-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "exact-node-matching-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-omission",
      "instruction": "Record current classifier and regression bindings, hashed anchors, keyword-only versus positional warning observations, separate AST collections, absent-default representation, and exact-node matching. Confirm the omitted collection and distinguish body capture before emitting confirmed diagnosis. Verify no source changes.",
      "evidence_refs": ["pylint-dev/pylint:5012:body", "pylint-dev/pylint:5012:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:default-expression-classifier", "role:loop-closure-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5012:repair:fb750d39f82d"],
  "evidence_refs": ["pylint-dev/pylint:5012:body", "pylint-dev/pylint:5012:fix"],
  "resource": "references/actions/diagnose.md",
  "package_id": "workflow:verified-history:d2dc67ed68c41ff7c06c4c32"
}
```
