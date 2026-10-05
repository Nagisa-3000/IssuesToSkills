# Inspect diagnostic ownership

Read source and run a bound public reproduction without modifying implementation or fixtures. Establish whether the executor classification, premature assigned-call emission, or both are present. Resolve semantic owners rather than borrowing historical paths.

```arex-contract-v4
{
  "id": "workflow:verified-history:d5bff35cdcd2562bddc778f8:inspect",
  "intent": "Establish current applicability and concrete semantic bindings.",
  "mechanism": "Inspect callable inference, classification, call emission, assignment visitors, with visitors, and scope lifecycle; compare public reproductions.",
  "semantic_role": "diagnostic-lifecycle-inspection",
  "owner_role": "resource-diagnostic-owner",
  "operation": "Read current source and public tests, record hashed anchors and a bound public reproduction, and identify which historical mechanisms are applicable. Do not edit source or fixtures.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "lifecycle-review",
      "semantic_role": "resource-diagnostic-lifecycle-review",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-lifecycle-review-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unmanaged-resource-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-context-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-refactoring-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-lifecycle",
      "instruction": "Record public reproduction diagnostics and source anchors identifying constructor classification and delayed-use handling. Confirm the operation made no implementation or fixture edits; report uncertainty explicitly.",
      "evidence_refs": ["pylint-dev/pylint:4689:body", "pylint-dev/pylint:4689:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:resource-diagnostic-owner", "role:resource-regression-owner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4689:repair:dd54e55265c5"],
  "evidence_refs": ["pylint-dev/pylint:4689:title", "pylint-dev/pylint:4689:body", "pylint-dev/pylint:4689:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:d5bff35cdcd2562bddc778f8"
}
```

An owner name is not proof of compatibility. If inference resolves a different callable or the current diagnostic has a different policy, return insufficient or not applicable rather than edit.
