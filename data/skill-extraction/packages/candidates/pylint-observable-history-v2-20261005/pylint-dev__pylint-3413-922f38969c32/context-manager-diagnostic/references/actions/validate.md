# Validate public outcomes

Bind commands to current public fixtures and client checks. Do not reuse contemporary qualification commands as historical execution guidance.

Run positive and negative diagnostic examples, message-control checks, and adjacent refactoring/non-iterator fixtures. Compare complete diagnostics and locations, not just process exit codes. Inspect interpreter-specific inference separately.

Review converted clients for preserved ownership and output consumption. Ensure suppressions name a registered message. Preserve adjacent assertions even when justified edits change source locations.

```arex-contract-v4
{
  "id": "workflow:verified-history:a2197ca95e3d5f6edcfac42f:validate",
  "intent": "Observe diagnostic correctness and preserved integration behavior after edits.",
  "mechanism": "Execute current public target and adjacent fixtures and check lifetime-sensitive consumers and suppression against complete observable outcomes.",
  "semantic_role": "diagnostic-validation",
  "owner_role": "python-functional-fixtures",
  "operation": "Run rendered current public Oracle commands without editing source. Record actual diagnostics, expected locations, suppression results, inference exclusions, client lifetime observations, and PASS/FAIL/UNKNOWN outcomes.",
  "kind": "validate",
  "inputs": [
    {
      "name": "integrated-change",
      "semantic_role": "context-manager-diagnostic-change",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "public-diagnostic-validation",
      "artifact_kind": "test-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-validation",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "context-manager-diagnostic-integrated", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "resource-lifetime-semantics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "target-and-adjacent-tests",
      "instruction": "Execute bound public fixtures for allocation, acquisition/start, direct-with negatives, builtin-open inference, suppression, and adjacent diagnostics. Compare complete actual and required diagnostics and record interpreter limitations.",
      "evidence_refs": ["pylint-dev/pylint:3413:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "client-lifetime-review",
      "instruction": "Review and publicly check converted and suppressed consumers for unchanged ownership, output consumption, and resource lifetime; reject premature closure of escaping handles.",
      "evidence_refs": ["pylint-dev/pylint:3413:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:a2197ca95e3d5f6edcfac42f:implement"],
  "read_set": ["role:python-refactoring-checker", "role:python-functional-fixtures", "role:diagnostic-consumers-and-docs"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:3413:repair:922f38969c32"],
  "evidence_refs": ["pylint-dev/pylint:3413:fix", "pylint-dev/pylint:3413:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a2197ca95e3d5f6edcfac42f"
}
```

A complete observation record is not a success claim. All required current Oracle checks and preserved-behavior assurances must be PASS for public acceptance. Failures and unknowns remain visible.
