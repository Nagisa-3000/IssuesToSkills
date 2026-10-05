# Validate both edits

Bind current public commands and render them before execution. Run the narrow reproduction and the public private-member functional checks, including retained positive unused-member cases. Review the unchanged ordinary `self`/`cls` branches.

If practical, use an isolated public control checkout to test new assertions against the pinned unmodified implementation. Do not overwrite working edits; unrelated environment failures are not causal evidence.

Capture actual diagnostics, exit statuses, and implementation/fixture hashes. Validation changes observations, not source or fixture contents. Historical assertions authorize intended checks, not a historical execution claim.

```arex-contract-v4
{
  "id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:validate",
  "intent": "Verify the narrow constructor repair and retained adjacent private-member behavior.",
  "mechanism": "Execute public diagnostic checks after implementation and fixture edits, with evidence-backed review of retained matching rules.",
  "semantic_role": "validate-returned-instance-repair",
  "owner_role": "public-test-runner",
  "operation": "Execute bound current public checks, capture diagnostics and statuses, check both named returns and non-name safety, and refresh observations against final code and fixture anchors.",
  "kind": "validate",
  "inputs": [
    {"name": "checker-edit", "semantic_role": "returned-instance-checker-edit", "artifact_kind": "source-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "edited"},
    {"name": "regression-edit", "semantic_role": "returned-instance-regression-edit", "artifact_kind": "test-change", "language": "Python", "scope": "current-checkout", "phase": "regression", "state": "edited"}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "returned-instance-validation", "artifact_kind": "test-result", "language": "Python", "scope": "current-checkout", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "returned-local-consumption-recognized", "value": true, "evaluator": "evidence"},
    {"key": "constructor-return-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "role:public-test-runner", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "non-name-return-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-private-member-public-checks",
      "instruction": "Run current bound reproduction and functional checks. Require no target warnings for consumed assignments on either returned local, no non-Name return crash, retained warnings for genuinely unused members, and retained ordinary self/cls matching. Record unavailable checks or failures explicitly.",
      "evidence_refs": ["pylint-dev/pylint:4668:body", "pylint-dev/pylint:4668:fix", "pylint-dev/pylint:4668:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4668:repair:f6c813824183"],
  "evidence_refs": ["pylint-dev/pylint:4668:body", "pylint-dev/pylint:4668:fix", "pylint-dev/pylint:4668:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2",
  "read_set": ["role:private-member-checker", "role:private-member-regressions", "role:public-test-runner"],
  "write_set": [],
  "validation_for": [
    "workflow:verified-history:c87ac9d043b1a02e14aba0d2:repair",
    "workflow:verified-history:c87ac9d043b1a02e14aba0d2:regressions"
  ]
}
```

A validation result can be FAIL or UNKNOWN. The declared effect describes successful completion, not automatic success. Broader current tests do not enlarge historical qualification retroactively.
