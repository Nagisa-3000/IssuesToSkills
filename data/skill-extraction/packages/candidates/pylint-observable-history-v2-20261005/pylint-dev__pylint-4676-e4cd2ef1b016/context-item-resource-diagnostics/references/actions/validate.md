# Validate header and body boundaries

Bind executable current public commands before running this operation. Execute after repair and again after further edits. Record command argv, exit status, diagnostic locations, test output, and semantic checks. An intentional warning may make a diagnostic command exit nonzero; compare expected diagnostics rather than relying only on exit status.

Run the original multiple-item reproduction and targeted assertions with the retained body-call control. Include available adjacent resource tests. Broader testing, if performed, is a separate observed result and must not be inferred from historical qualification.

```arex-contract-v4
{
  "id": "workflow:verified-history:ec6290f765c15f3fdc7283d4:validate",
  "intent": "Observe corrected context-item diagnostics and preservation of unmanaged-resource warnings.",
  "mechanism": "Execute public reproductions and functional assertions contrasting context-item expressions with independent body calls.",
  "semantic_role": "context-membership-validation",
  "owner_role": "resource-diagnostic-test-owner",
  "operation": "Run bound current public probes and tests without editing tracked files; record results and reject candidates with header false positives, missing body warnings, or changed adjacent expectations.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate-checkout",
      "semantic_role": "context-membership-repair-candidate",
      "artifact_kind": "checkout",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "context-membership-validation-results",
      "artifact_kind": "test-report",
      "language": "python",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:resource-diagnostic-test-owner", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unmanaged-body-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-resource-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-reproduction",
      "instruction": "Run the current public multiple-item conditional open/nullcontext reproduction and both-open ternary variants. Confirm no resource-management warning on their context-item resource calls.",
      "evidence_refs": ["pylint-dev/pylint:4676:body", "pylint-dev/pylint:4676:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-boundary-regressions",
      "instruction": "Run current targeted assertions and adjacent resource tests. Confirm correct direct single-line and multiline context-item behavior, a warning for a separate open in the with body, and unchanged existing expected diagnostics.",
      "evidence_refs": ["pylint-dev/pylint:4676:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4676:repair:e4cd2ef1b016"],
  "evidence_refs": ["pylint-dev/pylint:4676:body", "pylint-dev/pylint:4676:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:ec6290f765c15f3fdc7283d4",
  "read_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"],
  "write_set": [],
  "validation_for": ["workflow:verified-history:ec6290f765c15f3fdc7283d4:repair"]
}
```

A validation record may contain failures. Acceptance requires passing behavior and preservation checks, not merely completion of the operation. This Action does not provide independent hidden acceptance.
