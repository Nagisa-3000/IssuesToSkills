# Inspect the discriminator

Locate semantic owners in current code. Inspect the assignment-parent guard, annotation normalization, identifier access and naming consumer. Parse public direct and qualified examples to confirm actual node fields. Read regression conventions. Do not change tracked code. Produce a confirmed context only if the mechanism matches; otherwise record the mismatch and stop.

```arex-contract-v4
{
  "id": "workflow:verified-history:8196d401013577b7b429876a:inspect",
  "intent": "Confirm whether current ClassVar recognition matches the historical shape defect.",
  "mechanism": "Inspect public code and AST shapes to distinguish Name from Attribute annotation bases.",
  "semantic_role": "annotation-shape-diagnosis",
  "owner_role": "annotation-classifier",
  "operation": "Locate classifier, consumer and regression owners; record hashed anchors, node fields and unsafe recognition assumptions without changing tracked code.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "inspection", "semantic_role": "annotation-repair-context", "artifact_kind": "review-record", "language": "python", "scope": "classvar-naming", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "matching-shape-mechanism", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "direct-classvar-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-naming-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-shape-mechanism",
      "instruction": "Record current owner bindings and AST observations showing Name for direct bases and Attribute for qualified bases. Identify unsafe identifier access or equivalent qualified-form misclassification, confirm the naming consumer, and verify inspection did not change tracked code. Do not emit a confirmed context on mismatch.",
      "evidence_refs": ["pylint-dev/pylint:4264:body", "pylint-dev/pylint:4264:fix", "pylint-dev/pylint:4264:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4264:repair:c1c41b849ce0"],
  "evidence_refs": ["pylint-dev/pylint:4264:body", "pylint-dev/pylint:4264:fix", "pylint-dev/pylint:4264:regression"],
  "read_set": ["role:annotation-classifier", "role:class-constant-naming-consumer", "role:annotation-naming-regressions"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:8196d401013577b7b429876a"
}
```
