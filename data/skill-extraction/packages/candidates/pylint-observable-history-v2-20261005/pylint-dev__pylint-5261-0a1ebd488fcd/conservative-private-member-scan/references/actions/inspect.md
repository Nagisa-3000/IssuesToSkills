# Inspect the receiver assumption

Read current public code and fixtures without editing source. Observe the failing receiver type and candidate-search structure, bind semantic owners, and record baseline diagnostics. Mere symbol existence does not prove applicability.

Outputs and effects below are expected contracts, not recorded execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:4244f18e715c9b86c7cef8e0:inspect",
  "intent": "Establish applicability and bind current semantic owners.",
  "mechanism": "Inspect compound-receiver AST shape, unchecked name-only access, and candidate-search control flow.",
  "semantic_role": "receiver-assumption-probe",
  "owner_role": "private-usage-scan",
  "operation": "Read the public report, current checker, and fixtures; record pinned base, hashed anchors, receiver shape, owner bindings, baseline diagnostics, and whether conservative suppression is acceptable. Do not modify source.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "inspection", "semantic_role": "private-scan-binding-evidence", "artifact_kind": "review-record", "language": "python", "scope": "private-member-analysis", "phase": "inspection", "state": "receiver-assumption-established", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "receiver-assumption-established", "value": true, "evaluator": "evidence"},
    {"key": "role:private-usage-scan", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:private-usage-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "preserves": [
    {"key": "simple-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "argument-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-emission-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-receiver-shape",
      "instruction": "Review or publicly probe the current AST and scan. Confirm a non-Name compound receiver, unchecked receiver.name access, and candidate for/else semantics in which break skips warning emission. Record owner bindings, baseline diagnostic evidence, and conservative-suppression requirements. Confirm source hashes are unchanged by inspection.",
      "evidence_refs": ["pylint-dev/pylint:5261:body", "pylint-dev/pylint:5261:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5261:repair:0a1ebd488fcd"],
  "evidence_refs": ["pylint-dev/pylint:5261:title", "pylint-dev/pylint:5261:body", "pylint-dev/pylint:5261:fix"],
  "read_set": ["role:private-usage-scan", "role:private-usage-regressions"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:4244f18e715c9b86c7cef8e0"
}
```

Resolve role predicates through actual current bindings. Missing mechanism evidence authorizes further probes, not an edit. An incompatible node model rejects this realization.
