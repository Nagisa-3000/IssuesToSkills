# Confirm the position path

Locate the current type-comment processing owner, annotation diagnostic consumer, and annotation test owner. Read the current public code and inspect a malformed standalone type comment after an assignment. Compare comment coordinates with associated-node coordinates and trace the actual error-position argument.

The probe does not modify source. It emits the confirmed-path output only when the mismatch and position-only compatibility are established with current evidence. UNKNOWN or FAIL withholds that output. This applicability gate is derived from historical evidence, not a claim of historical probe execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e:probe",
  "intent": "Determine whether the historical position-carrier repair applies.",
  "mechanism": "Trace comment coordinates and the diagnostic-position interface in current public code.",
  "semantic_role": "location-path-confirmation",
  "owner_role": "type-comment-processing-owner",
  "operation": "Locate current semantic owners, read the diagnostic path, and compare comment and associated-node positions without modifying source; confirm that only position attributes are needed.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "confirmed-path",
      "semantic_role": "diagnostic-location-path",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "type-comment-diagnostics",
      "phase": "pre-edit",
      "state": "compatible-mismatch-confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "position-carrier-compatibility-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "semantic-comment-association-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-position-path",
      "instruction": "Inspect public current code and a malformed type comment following an assignment. Record comment and associated-node coordinates, the object used for syntax-error positioning, and consumer attribute requirements. Confirm that semantic association can stay unchanged and that the probe changed no source files. Withhold compatibility confirmation if any fact is unknown.",
      "evidence_refs": ["PyCQA/pyflakes:419:body", "PyCQA/pyflakes:419:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:419:repair:ba64624f38a5"],
  "evidence_refs": ["PyCQA/pyflakes:419:title", "PyCQA/pyflakes:419:body", "PyCQA/pyflakes:419:fix"],
  "read_set": [
    "role:type-comment-processing-owner",
    "role:annotation-diagnostic-consumer",
    "role:type-annotation-regression-tests"
  ],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:a9e64c06fdea4cfd948ba20e"
}
```
