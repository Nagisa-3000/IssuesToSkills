# Add the no-warning assertion

Use the current public fixture convention, retaining existing expected diagnostics. Historically `Apples.__index__` returned `1`.

```arex-contract-v4
{
  "id": "workflow:verified-history:6811635fea96a3e3f778e2f1:regression",
  "intent": "Retain valid-method acceptance as a regression requirement.",
  "mechanism": "Add a minimal valid method definition without expecting the erroneous name diagnostic.",
  "semantic_role": "retain-valid-method-assertion",
  "owner_role": "special-method-diagnostic-regression-suite",
  "operation": "Add the reproduction to the bound fixture using its no-warning convention. Preserve existing invalid-name and unrelated expectations; adjust line-sensitive metadata only for moved source locations.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "registry-omission-diagnosis", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [],
  "preconditions": [
    {"key": "role:special-method-diagnostic-regression-suite", "value": true, "evaluator": "file_exists", "description": "Resolve the public fixture in the current checkout."},
    {"key": "registry-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "regression-harness-understood", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "invalid-name-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "inspect-regression-assertion",
      "instruction": "Inspect the added valid method and its no-warning expectation. Confirm existing expectations remain semantically unchanged. For __index__, use a minimal integer-returning method.",
      "evidence_refs": ["pylint-dev/pylint:8613:regression", "pylint-dev/pylint:8613:body"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:special-method-diagnostic-regression-suite"],
  "write_set": ["role:special-method-diagnostic-regression-suite"],
  "source_ids": ["pylint-dev/pylint:8613:repair:f223c6de3a39"],
  "evidence_refs": ["pylint-dev/pylint:8613:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:6811635fea96a3e3f778e2f1"
}
```

An assertion is not an execution result. Retain [validation](validate.md) after this edit.
