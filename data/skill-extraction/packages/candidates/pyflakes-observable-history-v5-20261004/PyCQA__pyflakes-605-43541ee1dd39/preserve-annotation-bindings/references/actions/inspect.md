# Inspect annotation-only replacement

Locate current semantic owners for scope insertion, annotation classification, export bindings, and annotation tests. Trace the public reproduction and determine whether an incoming annotation-only binding overwrites the existing export binding.

Review declarations with assigned values separately. Record scope selection and usage propagation before proposing an edit. Historical paths do not substitute for current bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:inspect",
  "intent": "Determine applicability and bind current semantic owners.",
  "mechanism": "Read insertion and classification code and trace the public export/annotation reproduction.",
  "semantic_role": "binding-overwrite-diagnosis",
  "owner_role": "scope-binding-insertion",
  "operation": "Locate owners and record whether annotation-only insertion replaces an existing specialized binding.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosis",
      "semantic_role": "annotation-binding-repair-context",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "owners-bound-and-overwrite-confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-owner-bindings-established", "value": true, "evaluator": "evidence"},
    {"key": "annotation-only-overwrite-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "annotation-classification-compatible", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-overwrite",
      "instruction": "Trace the current public reproduction, identify current owners, and record whether an annotation-only incoming binding replaces the export binding. Distinguish declarations with assigned values and confirm that the insertion guard can preserve them.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489",
  "read_set": ["role:scope-binding-insertion", "role:annotation-binding-classifier", "role:export-binding", "role:annotation-test-suite"],
  "write_set": [],
  "exclusions": [
    {"key": "incoming-binding-is-real-assignment", "value": true, "evaluator": "evidence"}
  ]
}
```

The output and effects describe a successful applicability probe, not an observation already made by this package. A negative or incomplete diagnosis blocks edits; preserve its actual FAIL or UNKNOWN outcome.
