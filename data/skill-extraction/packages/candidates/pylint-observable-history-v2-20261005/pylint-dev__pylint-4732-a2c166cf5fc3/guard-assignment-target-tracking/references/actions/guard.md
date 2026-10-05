# Guard tracking and add regressions

Require a supported target type before deferred stack lookup and target-name extraction. In the supplied Python realization, supported types were `astroid.AssignName` and `astroid.AssignAttr`.

Retain inference and recognized-resource-call filtering. Skip only unsupported deferred tracking; do not disable immediate diagnostics, catch all attribute errors, or fabricate a container resource name.

Add list-item and dictionary-item assignments of a recognized context-manager-producing call to the current public regression fixture. Both must assert immediate diagnostics. See [historical assertions](../evidence/regression.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:4b0b98b3c492f42522a4c12d:guard",
  "intent": "Exclude unsupported targets from deferred tracking while retaining immediate diagnostics.",
  "mechanism": "Extend the existing skip condition with a supported-target type check before stack access and field extraction.",
  "semantic_role": "tracking-boundary-repair",
  "owner_role": "context-manager-assignment-tracker",
  "operation": "Edit the current tracking owner to accept only supported name and attribute targets; update current functional fixtures and diagnostic assertions for list-item and dictionary-item resource calls.",
  "kind": "edit",
  "inputs": [
    {
      "name": "assessment",
      "semantic_role": "assignment-tracking-assessment",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout-resource-checker",
      "phase": "pre-edit",
      "state": "assessed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "guarded-assignment-tracking-candidate",
      "artifact_kind": "checkout-diff",
      "language": "python",
      "scope": "current-checkout-resource-checker",
      "phase": "post-edit",
      "state": "modified",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "tracking-boundary-assessed", "value": true, "evaluator": "evidence"},
    {"key": "unsupported-target-reaches-name-extraction", "value": true, "evaluator": "evidence"},
    {"key": "separate-immediate-diagnostic-path-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:context-manager-assignment-tracker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:resource-checker-functional-assertions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "unsupported-targets-excluded", "value": true, "evaluator": "evidence"},
    {"key": "subscript-regression-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-target-tracking-preserved", "value": true, "evaluator": "evidence"},
    {"key": "immediate-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-checker-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-guard-and-assertions",
      "instruction": "Review the current diff for a supported-target guard before stack lookup and field extraction, retained inference and call filters, and diagnostic assertions for both subscript targets. Retain the validation Action for runtime checks.",
      "evidence_refs": ["pylint-dev/pylint:4732:fix", "pylint-dev/pylint:4732:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:context-manager-assignment-tracker", "role:immediate-resource-diagnostic", "role:resource-checker-functional-assertions"],
  "write_set": ["role:context-manager-assignment-tracker", "role:resource-checker-functional-assertions"],
  "invalidates": ["public-validation-observed", "pre-edit-code-anchors-current"],
  "exclusions": [
    {"key": "container-lifetime-tracking-required", "value": true, "evaluator": "evidence"},
    {"key": "separate-immediate-diagnostic-path-confirmed", "value": false, "evaluator": "evidence"}
  ],
  "source_ids": ["pylint-dev/pylint:4732:repair:a2c166cf5fc3"],
  "evidence_refs": ["pylint-dev/pylint:4732:fix", "pylint-dev/pylint:4732:regression"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:4b0b98b3c492f42522a4c12d"
}
```

Effects are required candidate properties, not observed success. Invalidated observations are distinct from preserved behavior. Retain [validation](validate.md) after every execution of this modifying Action.
