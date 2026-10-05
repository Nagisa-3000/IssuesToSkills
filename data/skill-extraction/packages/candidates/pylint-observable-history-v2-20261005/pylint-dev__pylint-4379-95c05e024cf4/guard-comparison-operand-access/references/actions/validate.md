# Validate the guarded checker

Run the current public min/max functional tests and relevant neighboring refactoring cases. Inspect crash status and exact expected suggestions. Check both new cases independently if a combined run would stop at the first crash. Existing supported name/constant examples must still produce their prior expected diagnostics.

Commands must be bound to the current public checkout. Empty contract command arrays are intentionally unbound, not executed commands. An unavailable harness or unexecuted command leaves validation UNKNOWN, not PASS.

```arex-contract-v4
{
  "id": "workflow:verified-history:ba0f15907d742a3c30dae2cf:validate",
  "intent": "Observe crash removal and preservation after both edits.",
  "mechanism": "Execute the public regression harness and inspect diagnostics for unsupported and supported operand cases.",
  "semantic_role": "public-behavior-validation",
  "owner_role": "min-max-functional-regressions",
  "operation": "Render and run current bound public commands; record results against current code anchors, checking both unsupported shapes and existing supported/neighboring cases. Do not rewrite source or expected outputs during validation.",
  "kind": "validate",
  "inputs": [],
  "outputs": [
    {"name": "validation-record", "semantic_role": "public-check-results", "artifact_kind": "test-result-record", "language": "python", "scope": "min-max-functional-regressions", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "operand-kind-guard-present", "value": true, "evaluator": "evidence"},
    {"key": "unsupported-shape-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-name-constant-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "neighboring-refactoring-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-unsupported-operands",
      "instruction": "Run both public reproduction shapes through the checker. Verify no UnaryOp/List attribute-access exception, continued traversal, and no min/max suggestion for either added case.",
      "evidence_refs": ["pylint-dev/pylint:4379:body", "pylint-dev/pylint:4379:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-supported-and-adjacent",
      "instruction": "Run the bound public min/max functional harness and relevant neighboring refactoring tests. Compare exact expected diagnostics for existing Name/Const positive and negative examples; record failures and unavailable checks explicitly.",
      "evidence_refs": ["pylint-dev/pylint:4379:fix", "pylint-dev/pylint:4379:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:ba0f15907d742a3c30dae2cf:guard",
    "workflow:verified-history:ba0f15907d742a3c30dae2cf:regressions"
  ],
  "source_ids": ["pylint-dev/pylint:4379:repair:95c05e024cf4"],
  "evidence_refs": ["pylint-dev/pylint:4379:body", "pylint-dev/pylint:4379:fix", "pylint-dev/pylint:4379:regression"],
  "read_set": ["role:comparison-operand-extractor", "role:min-max-functional-regressions"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:ba0f15907d742a3c30dae2cf"
}
```
