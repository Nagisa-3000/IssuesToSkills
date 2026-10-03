# Probe the annotation-only binding path

Read current public code and run a public reproduction without editing the checkout. Locate semantic owners rather than copying historical paths. Confirm that the statement has no value and that the diagnostic comes from redefinition classification, not an unrelated undefined-name check.

```arex-contract-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:probe",
  "intent": "Confirm the reported false-positive mechanism and bind current owners.",
  "mechanism": "Trace an import followed by annotation-only syntax and subsequent use through binding classification.",
  "semantic_role": "annotation-redefinition-diagnosis",
  "owner_role": "annotation-binding-owner",
  "operation": "Read the current annotation binding and redefinition predicate, locate annotation tests, and observe a public minimal reproduction; do not modify files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "owners", "semantic_role": "confirmed-annotation-redefinition-context", "artifact_kind": "code-binding-record", "language": "python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "annotation-owner-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-definition-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-mechanism",
      "instruction": "Observe the public import/annotation/use diagnostic and inspect whether annotation-only bindings inherit ordinary redefinition behavior. Record current owners and runner; confirm the probe makes no source edits.",
      "evidence_refs": ["PyCQA/pyflakes:617:body", "PyCQA/pyflakes:617:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:annotation-binding-owner", "role:redefinition-predicate-owner", "role:annotation-test-owner"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "evidence_refs": ["PyCQA/pyflakes:617:body", "PyCQA/pyflakes:617:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7"
}
```

Expected output is a confirmed owner record, not a claim that this package has probed the current checkout. Stop if the public reproduction or semantic equivalence cannot be established.
