# Validate target and adjacent behavior

Bind and render current public Oracle commands. Execute focused regressions and AST controls without modifying implementation or expected diagnostics. Record commands, code anchors, exit statuses, and warning locations. Inspect expectations as well as process exit status.

Absent-default, identity, and scope probes are authored current validation obligations derived from the implementation. They are not claims that additional historical tests existed or ran.

Only passing required observations support a success claim. Record failures and UNKNOWN honestly. Subsequent edits stale the observation and require validation again.

```arex-contract-v4
{
  "id": "workflow:verified-history:d2dc67ed68c41ff7c06c4c32:validate",
  "intent": "Observe corrected eager-default classification and retained adjacent behavior.",
  "mechanism": "Execute public capture regressions and AST-level classifier controls.",
  "semantic_role": "default-classification-validation",
  "owner_role": "loop-closure-regression-suite",
  "operation": "Run current bound public tests and probes without changing implementation or expectations; record actual outcomes.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "default-classification-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "default-classification-validation",
      "artifact_kind": "test-observation",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "default-collections-complete", "value": true, "evaluator": "evidence"},
    {"key": "focused-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "positional-default-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-closure-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "exact-node-matching-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-regressions",
      "instruction": "Run the current public loop-closure regression suite. Require no warnings for escaping keyword-only and positional eager captures, and retained expected warnings for genuine late-bound body references. Compare diagnostic locations and confirm expectations were not weakened.",
      "evidence_refs": ["pylint-dev/pylint:5012:body", "pylint-dev/pylint:5012:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-classifier-controls",
      "instruction": "Probe required keyword-only parameters without defaults, queried name descendants in both default collections, distinct same-spelling nodes, function/lambda handling, and unsupported scopes. Require safe absent-entry handling, exact-node identity recognition, and retained false fallback.",
      "evidence_refs": ["pylint-dev/pylint:5012:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:d2dc67ed68c41ff7c06c4c32:repair"],
  "read_set": ["role:default-expression-classifier", "role:loop-closure-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5012:repair:fb750d39f82d"],
  "evidence_refs": ["pylint-dev/pylint:5012:body", "pylint-dev/pylint:5012:fix", "pylint-dev/pylint:5012:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d2dc67ed68c41ff7c06c4c32"
}
```
