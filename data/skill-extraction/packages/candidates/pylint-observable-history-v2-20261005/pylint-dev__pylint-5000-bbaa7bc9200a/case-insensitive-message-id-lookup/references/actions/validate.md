# Validate both edits and adjacent behavior

Run current bound public commands without source or fixture edits. Committed expected results do not prove execution.

Historical assertions cover lowercase enable directives, uppercase recommendations, and an invalid ID. The report supplies the lowercase disable reproduction. Direct resolver and already-symbolic checks are current safety probes, not additional historically executed tests.

```arex-contract-v4
{
  "id": "workflow:verified-history:3af38f4091bb3d8442540d61:validate",
  "intent": "Observe corrected recommendations and preserved adjacent behavior after both edits.",
  "mechanism": "Execute targeted public regressions and case-variant controls.",
  "semantic_role": "repair-validation",
  "owner_role": "symbolic-recommendation-regression-suite",
  "operation": "Execute the current bound public suite and reproductions. Compare case variants, enable/disable replacements, unknown IDs, original spelling, and already-symbolic directives. Record commands, outcomes, and scope without source or fixture edits.",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "numeric-symbol-lookup-case-insensitive", "value": true, "evaluator": "evidence"},
    {"key": "lowercase-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "uppercase-recommendations-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unknown-id-error-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "original-id-spelling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-public-regression",
      "instruction": "Run the bound public recommendation suite. Require separate lowercase recommendations, preserved uppercase recommendations, correct enable replacements, and unchanged invalid-ID diagnostics. Record actual results and selected-test scope.",
      "evidence_refs": ["pylint-dev/pylint:5000:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "run-case-controls",
      "instruction": "Execute public probes for uppercase/lowercase resolver equivalence, the lowercase disable reproduction, original input spelling, unchanged unknown-ID errors, and already-symbolic directives receiving no numeric-ID recommendation. Record actual outcomes rather than assuming success.",
      "evidence_refs": ["pylint-dev/pylint:5000:body", "pylint-dev/pylint:5000:fix", "pylint-dev/pylint:5000:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5000:repair:bbaa7bc9200a"],
  "evidence_refs": ["pylint-dev/pylint:5000:body", "pylint-dev/pylint:5000:fix", "pylint-dev/pylint:5000:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:3af38f4091bb3d8442540d61",
  "kind": "validate",
  "validation_for": [
    "workflow:verified-history:3af38f4091bb3d8442540d61:normalize",
    "workflow:verified-history:3af38f4091bb3d8442540d61:regression"
  ],
  "read_set": ["role:numeric-id-symbol-resolver", "role:message-control-entrypoint", "role:symbolic-recommendation-regression-suite"],
  "write_set": []
}
```

`public-validation-observed` becomes fresh only after execution; repair acceptance additionally requires passing results. Failed validation is an observed failure, not permission to claim the Workflow goal.
