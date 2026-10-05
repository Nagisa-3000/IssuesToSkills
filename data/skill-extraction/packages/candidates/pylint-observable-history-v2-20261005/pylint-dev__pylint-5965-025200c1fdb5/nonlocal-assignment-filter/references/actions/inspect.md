# Inspect frame declarations and filtering

Read current public code and reproduction without changing the checkout. Identify whether the specific name has a `Nonlocal` declaration in the frame used by the name-resolution operation. Inspect earlier candidate resolution and the later exception-handler assignment filter. Produce anchored observations, not merely guessed owner names.

Historical reference: the inserted guard is immediately before the comment about filtering assignments in `ExceptHandlers`.

```arex-contract-v4
{
  "id": "workflow:verified-history:88758c6085df4be35e45f76d:inspect",
  "intent": "Establish whether the current false positive has the supported scope/filtering mechanism.",
  "mechanism": "Compare the queried name with explicit nonlocal declarations in its frame and locate the exception-handler filtering boundary.",
  "semantic_role": "scope-filter-diagnosis",
  "owner_role": "assignment-filter",
  "kind": "probe",
  "operation": "Read the reproduction, frame API and assignment-filter code; record hashed anchors and name-specific scope observations without modifying files.",
  "inputs": [],
  "outputs": [
    {"name": "diagnosis", "semantic_role": "scope-filter-diagnosis", "artifact_kind": "anchored-review", "language": "python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "mechanism-confirmed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-reproduction-available", "value": true, "evaluator": "evidence"},
    {"key": "assignment-filter-owner-located", "value": true, "evaluator": "symbol_exists", "description": "role:assignment-filter"}
  ],
  "effects": [
    {"key": "scope-filter-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unrelated-nonlocal-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-control-flow-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-frame-and-filter",
      "instruction": "Review current anchored code and the public reproduction. Confirm the queried name, enclosing initialization, same-frame explicit nonlocal declaration and exception-handler assignment filter; report UNKNOWN if any link is missing. Confirm this probe made no file changes.",
      "evidence_refs": ["pylint-dev/pylint:5965:body", "pylint-dev/pylint:5965:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5965:repair:025200c1fdb5"],
  "evidence_refs": ["pylint-dev/pylint:5965:body", "pylint-dev/pylint:5965:fix"],
  "read_set": ["role:assignment-filter", "role:scope-frame", "role:assignment-regression-suite"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:88758c6085df4be35e45f76d"
}
```
