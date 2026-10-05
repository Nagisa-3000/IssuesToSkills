# Probe local classification

Read current code and run a bound public reproduction without modifying source or test files. Locate semantic owners and record code hashes. Confirm the annotation recognizer and alias category already exist.

```arex-contract-v4
{
  "id": "workflow:verified-history:b980c9ec644c821d41e50e10:probe",
  "intent": "Confirm a scope-specific explicit-alias naming defect and compatible owners.",
  "mechanism": "Compare local and top-level explicit-alias diagnostics and inspect eligible local assignment dispatch.",
  "semantic_role": "classify-defect",
  "owner_role": "local-name-classifier",
  "operation": "Read the guarded branch and existing recognizer; execute a bound public reproduction without source edits and record owner bindings and semantic findings.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "classification-findings",
      "semantic_role": "local-alias-classification-findings",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "function-local-naming",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "local-classification-defect-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "compatible-alias-recognizer-located", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [],
  "oracle": [
    {
      "id": "confirm-scope-gap",
      "instruction": "Compare bad top-level and local explicit aliases under the same naming policy. Confirm the local diagnostic gap and inspect alias recognition, variable routing, membership, argument exclusion, and import-redefinition guards. Record concrete bindings and verify source hashes are unchanged.",
      "evidence_refs": ["pylint-dev/pylint:8536:body", "pylint-dev/pylint:8536:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8536:repair:b63c8a1c148e"],
  "evidence_refs": ["pylint-dev/pylint:8536:body", "pylint-dev/pylint:8536:fix"],
  "read_set": ["role:local-name-classifier", "role:typealias-recognizer"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:b980c9ec644c821d41e50e10"
}
```

These effects and the confirmed output are conditional on actual observations. Unknown compatibility permits further probing only; a disproved defect does not produce confirmed findings.
