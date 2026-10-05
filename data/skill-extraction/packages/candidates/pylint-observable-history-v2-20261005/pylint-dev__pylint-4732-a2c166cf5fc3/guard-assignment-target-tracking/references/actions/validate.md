# Validate diagnostics and preservation

Bind current public commands to the located linter and test harness. Run subscript regressions and existing supported-target and adjacent coverage. Distinguish expected diagnostic exit statuses from internal exceptions.

Refresh anchors and observations against the edited candidate. Testing must not edit tracked source or expected-output files. Missing coverage remains UNKNOWN.

```arex-contract-v4
{
  "id": "workflow:verified-history:4b0b98b3c492f42522a4c12d:validate",
  "intent": "Observe crash avoidance, immediate diagnostics, and preservation of supported and adjacent behavior.",
  "mechanism": "Exercise unsupported subscript targets and existing supported-target assertions after the edit.",
  "semantic_role": "tracking-repair-validation",
  "owner_role": "resource-checker-functional-assertions",
  "operation": "Execute bound public reproductions and functional tests, inspect diagnostics, refresh candidate hashes, and record actual tri-state results.",
  "kind": "validate",
  "inputs": [
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
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "assignment-tracking-validation",
      "artifact_kind": "test-observation",
      "language": "python",
      "scope": "current-checkout-resource-checker",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "unsupported-targets-excluded", "value": true, "evaluator": "evidence"},
    {"key": "subscript-regression-assertions-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "subscript-diagnostics-observed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-target-tracking-preserved", "value": true, "evaluator": "evidence"},
    {"key": "immediate-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-checker-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-subscript-diagnostics",
      "instruction": "Lint public list-item and dictionary-item assignments of a recognized context-manager-producing call. Verify no internal exception and the immediate context-manager recommendation at both calls.",
      "evidence_refs": ["pylint-dev/pylint:4732:body", "pylint-dev/pylint:4732:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-supported-and-adjacent-behavior",
      "instruction": "Run current resource-checker assertions and adjacent public tests. Check direct-name and attribute tracking, context-manager handling, inference failure, and non-resource calls. Mark uncovered behavior UNKNOWN.",
      "evidence_refs": ["pylint-dev/pylint:4732:fix", "pylint-dev/pylint:4732:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:4b0b98b3c492f42522a4c12d:guard"],
  "read_set": ["role:context-manager-assignment-tracker", "role:immediate-resource-diagnostic", "role:resource-checker-functional-assertions"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4732:repair:a2c166cf5fc3"],
  "evidence_refs": ["pylint-dev/pylint:4732:body", "pylint-dev/pylint:4732:fix", "pylint-dev/pylint:4732:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4b0b98b3c492f42522a4c12d"
}
```

Observation outputs can contain failures. Required effects are not claims of execution success. This Action has not run during Skill authoring.
