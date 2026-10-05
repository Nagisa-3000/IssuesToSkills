# Validate corrected and retained diagnostics

Bind and render current public commands before execution. Record actual results. Review branch preservation independently of test exit status.

```arex-contract-v4
{
  "id": "workflow:verified-history:65539eb7c9013462474b0b56:validate",
  "intent": "Verify false-positive removal and preservation of adjacent diagnostics after edits.",
  "mechanism": "Combine a collecting-override reproduction, retained nonvariadic assertions, and narrow-diff review.",
  "semantic_role": "validate-default-count-compatibility",
  "owner_role": "override-signature-regression-suite",
  "operation": "Execute bound current public checks. Confirm no signature-differs at the collecting override, retained expected nonvariadic default-loss diagnostics, and unchanged preceding argument-mismatch logic. Record commands, outputs, tri-state statuses, and current anchors. Do not edit tracked source.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "guarded-default-count-candidate",
      "artifact_kind": "source-and-regression-change",
      "language": "python",
      "scope": "override-signature-checking",
      "phase": "repair",
      "state": "edited-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "default-count-validation-observation",
      "artifact_kind": "public-test-and-review-record",
      "language": "python",
      "scope": "override-signature-checking",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "default-count-guard-added", "value": true, "evaluator": "evidence"},
    {"key": "collecting-override-regression-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "collecting-override-false-positive-removed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nonvariadic-default-loss-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "preceding-argument-mismatch-branch-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-collecting-override",
      "instruction": "Run the bound public reproduction and inspect diagnostics. Confirm no signature-differs at the collecting override without demanding absence of unrelated messages.",
      "evidence_refs": ["pylint-dev/pylint:3737:body", "pylint-dev/pylint:3737:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-retained-controls",
      "instruction": "Run the bound public signature regression suite. Confirm nonvariadic default-loss expectations still match and review that preceding argument-mismatch logic is unchanged. Record failures, skips, and unavailable checks separately from passes.",
      "evidence_refs": ["pylint-dev/pylint:3737:fix", "pylint-dev/pylint:3737:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:65539eb7c9013462474b0b56:repair"],
  "read_set": ["role:override-signature-checker", "role:override-signature-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:3737:repair:3ed4b9c0cc18"],
  "evidence_refs": ["pylint-dev/pylint:3737:body", "pylint-dev/pylint:3737:fix", "pylint-dev/pylint:3737:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:65539eb7c9013462474b0b56"
}
```

Successful effects require passing observable checks. FAIL or UNKNOWN blocks a repair-success claim. Subsequent edits require fresh validation.
