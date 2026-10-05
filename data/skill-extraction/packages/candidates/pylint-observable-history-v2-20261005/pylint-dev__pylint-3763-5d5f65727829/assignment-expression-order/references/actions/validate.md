# Validate the edited state

Render current bound public commands, then run them without golden-output update mode. Record actual diagnostics, runtime, skips, exit statuses, and code-review evidence.

Require no E0601 on supported positive examples, E0601 on genuine early reads, and `pointless-statement` on the standalone example. Run relevant adjacent checker tests and review scope restrictions.

If a legacy joined-string branch changed, check its guards and exercise applicable runtime-specific public fixtures when environments are available. Unavailable or skipped coverage is UNKNOWN, not PASS. Report failures and unknowns without claiming successful validation. Validation itself does not edit implementation or expected outputs.

```arex-contract-v4
{
  "id": "workflow:verified-history:0d5d796f6706ce7801b87899:validate",
  "intent": "Observe repaired diagnostics and preserved behavior on the edited checkout.",
  "mechanism": "Run public positive, negative, adjacent, and applicable runtime-boundary checks against the patch.",
  "semantic_role": "repair-validation",
  "owner_role": "public-test-runner",
  "operation": "Run bound public checks and review retained scope/version guards; emit a results report recording passes, failures, skips, and unknown coverage without altering implementation or expectations.",
  "kind": "validate",
  "inputs": [
    {
      "name": "patch",
      "semantic_role": "assignment-order-repair",
      "artifact_kind": "checkout-patch",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "assignment-order-validation",
      "artifact_kind": "public-evidence-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "results-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-regression-coverage-present", "value": true, "evaluator": "evidence"},
    {"key": "role:public-test-runner", "value": true, "evaluator": "file_exists"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-early-read-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "independent-expression-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "frame-and-ancestry-constraints-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "positive-and-negative-diagnostics",
      "instruction": "Execute current bound public fixtures. Verify absence of E0601 on valid conditional-test assignments, presence on genuine early reads, and preservation of the standalone pointless-statement diagnostic. Record actual outputs, runtime, skips, and exit status.",
      "evidence_refs": ["pylint-dev/pylint:3763:body", "pylint-dev/pylint:3763:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-and-version-boundaries",
      "instruction": "Execute relevant adjacent public checker tests and review frame/ancestor constraints. For changed legacy joined-string handling, verify narrow guards and execute applicable runtime-specific fixtures when available. Mark unavailable or skipped required coverage UNKNOWN.",
      "evidence_refs": ["pylint-dev/pylint:3763:fix", "pylint-dev/pylint:3763:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:0d5d796f6706ce7801b87899:repair"],
  "read_set": ["role:variable-order-checker", "role:runtime-version-policy", "role:assignment-expression-regressions", "role:public-test-runner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:3763:repair:5d5f65727829"],
  "evidence_refs": ["pylint-dev/pylint:3763:fix", "pylint-dev/pylint:3763:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:0d5d796f6706ce7801b87899"
}
```
