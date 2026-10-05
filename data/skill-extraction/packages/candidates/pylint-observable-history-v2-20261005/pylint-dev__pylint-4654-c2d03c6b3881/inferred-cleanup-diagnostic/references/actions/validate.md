# Validate target and adjacent diagnostics

Run current bound public commands, not copied historical commands. Check the target no-warning fixture and existing controls for unmanaged allocation and ordinary `with` use.

Inspect or publicly probe the new helper's non-call-parent, failed-inference, and unrecognized-callable boundaries. These are current checks derived from the implementation, not claims of additional committed historical tests.

If feasible, use an isolated current checkout to show that the added regression distinguishes the pre-edit diagnostic from the candidate. Do not execute firmware-file access as application code: this is a static-analysis oracle. Record unavailable checks as UNKNOWN and stop if required validation cannot be completed.

```arex-contract-v4
{
  "id": "workflow:verified-history:556cefd05a1df4981665346d:validate",
  "intent": "Observe corrected target output and preserved adjacent warning behavior.",
  "mechanism": "Execute public resource-diagnostic regressions and review or probe unsupported inference boundaries.",
  "semantic_role": "validate-cleanup-exemption",
  "owner_role": "resource-diagnostic-test-owner",
  "operation": "Run bound current public target and adjacent tests; check fallback boundaries; record actual argv, exit status, observations, and limitations without modifying source.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "cleanup-diagnostic-candidate",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "cleanup-diagnostic-validation",
      "artifact_kind": "test-and-review-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "recognized-direct-registration-exempt", "value": true, "evaluator": "evidence"},
    {"key": "no-warning-regression-added", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "target-and-adjacent-controls",
      "instruction": "Run current public diagnostic tests. Require no resource warning for direct managed recognized registration, retained unmanaged-allocation warnings, and retained ordinary-with exemptions. Review or publicly probe non-call parents, failed inference, and unrecognized callable identities to confirm no new exemption. Record executed checks separately from review and unavailable checks.",
      "evidence_refs": ["pylint-dev/pylint:4654:fix", "pylint-dev/pylint:4654:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4654:repair:c2d03c6b3881"],
  "evidence_refs": ["pylint-dev/pylint:4654:fix", "pylint-dev/pylint:4654:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:556cefd05a1df4981665346d",
  "read_set": ["role:resource-diagnostic-owner", "role:resource-diagnostic-test-owner"],
  "validation_for": ["workflow:verified-history:556cefd05a1df4981665346d:repair"]
}
```
