# Locate and diagnose

Locate current parser symbols and public checker tests. Compare list recognition, collected names, and warning output with singleton and genuine-missing controls. Separate parsing defects from inference and configuration failures.

This operation does not edit source or tests. Produce the success port only after confirming the mismatch and real owner bindings; otherwise report FAIL or UNKNOWN without authorizing repair.

```arex-contract-v4
{
  "id": "workflow:verified-history:659f8bc8e03e7014a22a5caa:diagnose",
  "intent": "Confirm a documentation-list parsing mismatch.",
  "mechanism": "Compare recognized declarations and collected exception names with public checker diagnostics.",
  "semantic_role": "diagnose-exception-list-mismatch",
  "owner_role": "docstring-type-parser",
  "operation": "Locate current Python parser and test owners; inspect recognition and collection; probe list, singleton, and genuinely missing declarations without source or test edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosis",
      "semantic_role": "exception-list-diagnosis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "public-checkout-docstring-checker",
      "phase": "diagnosed",
      "state": "owners-bound-and-mismatch-confirmed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "list-parsing-mismatch-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "singleton-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-type-forms-preserved", "value": true, "evaluator": "evidence"},
    {"key": "google-description-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "public-list-diagnosis",
      "instruction": "Record real owner bindings, hashed anchors, parsed list output, singleton and missing-documentation controls, and warning output. Confirm the discrepancy belongs to documentation recognition or extraction, not inference or configuration. Confirm source and test diffs are unchanged.",
      "evidence_refs": ["pylint-dev/pylint:2729:body", "pylint-dev/pylint:2729:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:2729:repair:183dcc4cb134"],
  "evidence_refs": ["pylint-dev/pylint:2729:title", "pylint-dev/pylint:2729:body", "pylint-dev/pylint:2729:fix"],
  "read_set": ["role:docstring-type-parser", "role:raise-doc-tests"],
  "write_set": [],
  "resource": "references/actions/diagnose.md",
  "package_id": "workflow:verified-history:659f8bc8e03e7014a22a5caa"
}
```
