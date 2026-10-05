# Validate acceptance and neighboring diagnostics

Use current public Oracle bindings, with the diagnostic enabled and the harness detecting unexpected warnings. Validation does not modify tracked source.

```arex-contract-v4
{
  "id": "workflow:verified-history:6811635fea96a3e3f778e2f1:validate",
  "intent": "Observe valid-method acceptance and preserved adjacent diagnostics.",
  "mechanism": "Run a public reproduction and the functional fixture after both edits.",
  "semantic_role": "verify-name-acceptance-repair",
  "owner_role": "special-method-diagnostic-regression-suite",
  "operation": "Execute bound public reproduction and functional tests; record argv, exit codes, diagnostics, input hashes, and PASS/FAIL/UNKNOWN outcomes without editing tracked source.",
  "kind": "validate",
  "inputs": [],
  "outputs": [
    {"name": "validation-record", "semantic_role": "special-method-diagnostic-validation", "artifact_kind": "test-report", "language": "Python", "scope": "current-checkout", "phase": "validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "registration-edit-present", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "invalid-name-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "valid-method-no-warning",
      "instruction": "Run the current bound minimal reproduction with the name diagnostic enabled. Confirm no name warning is emitted for the valid method.",
      "evidence_refs": ["pylint-dev/pylint:8613:body", "pylint-dev/pylint:8613:fix"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "functional-adjacent-coverage",
      "instruction": "Run the bound public functional suite. Require the new no-warning assertion, retained invalid-name warnings, and unrelated expectations to pass without weakening assertions.",
      "evidence_refs": ["pylint-dev/pylint:8613:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:6811635fea96a3e3f778e2f1:register",
    "workflow:verified-history:6811635fea96a3e3f778e2f1:regression"
  ],
  "read_set": ["role:special-method-acceptance-registry", "role:special-method-diagnostic-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8613:repair:f223c6de3a39"],
  "evidence_refs": ["pylint-dev/pylint:8613:body", "pylint-dev/pylint:8613:fix", "pylint-dev/pylint:8613:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:6811635fea96a3e3f778e2f1"
}
```

A failed report is an observation, not repair success. Both Oracles must be PASS and preservation assurances supported. Broader current checks cannot be claimed as historical execution.
