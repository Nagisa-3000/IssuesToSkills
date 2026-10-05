# Validate final code and assertions

Run bound public checks on the final edited state. The original issue's `pylint a.py` is historical evidence only. Resolve the current runner and construct current commands from public checkout information.

Inspect actual diagnostics and confidence, not only process exit status. An analyzer may legitimately exit nonzero for missing-parameter or unexpected-keyword messages. Repository-test failure, analyzer traceback, or missing expected diagnostics is a validation failure.

```arex-contract-v4
{
  "id": "workflow:verified-history:d00504c6d18cf355ce8404aa:validate",
  "intent": "Observe the repaired edge cases and preserved adjacent behavior on the current final state.",
  "mechanism": "Run a public minimal reproduction and the bound functional suite, comparing emitted diagnostics and confidence with the public regression matrix.",
  "semantic_role": "validate-repair-and-regressions",
  "owner_role": "public-test-runner",
  "operation": "Render and execute current public Oracle commands, capture results against final code anchors, and refresh the validation observation. Do not modify source or expectations.",
  "kind": "validate",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "current-owner-bindings-established", "value": true, "evaluator": "evidence"},
    {"key": "missing-argument-handled-locally", "value": true, "evaluator": "evidence"},
    {"key": "argument-form-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-signature-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-copy-check-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-exceptions-not-swallowed", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "omitted-argument-mre",
      "instruction": "Run the bound public no-argument reproduction. Verify no checker traceback or analyzer crash and verify the ordinary missing-parameter diagnostic remains.",
      "evidence_refs": ["pylint-dev/pylint:8774:body", "pylint-dev/pylint:8774:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "argument-forms-and-adjacent-tests",
      "instruction": "Run the bound public functional cases and adjacent checks. Verify direct positional and keyword warnings, inferred unpacked-keyword confidence, absence of specialized warnings for unrelated values and wrong keywords, preserved ordinary diagnostics, alias behavior and inference-error handling. Review the final diff for narrow exception handling.",
      "evidence_refs": ["pylint-dev/pylint:8774:fix", "pylint-dev/pylint:8774:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:d00504c6d18cf355ce8404aa:repair",
    "workflow:verified-history:d00504c6d18cf355ce8404aa:regressions"
  ],
  "source_ids": ["pylint-dev/pylint:8774:repair:92485a35e516"],
  "evidence_refs": ["pylint-dev/pylint:8774:body", "pylint-dev/pylint:8774:fix", "pylint-dev/pylint:8774:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d00504c6d18cf355ce8404aa",
  "read_set": ["role:call-value-checker", "role:call-checker-regression-suite", "role:public-test-runner"],
  "write_set": []
}
```

Empty command arrays are deliberate unbound definitions. They are not executable authorization. Current TaskContext bindings supply actual argv arrays and evidence.

If results fail or remain UNKNOWN, report the gap and do not label the repair successful. Any subsequent edit makes `public-validation-observed` stale and requires fresh validation.
