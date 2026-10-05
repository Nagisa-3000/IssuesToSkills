# Validate the public matrix

Execute both fallthrough positives and both explicit-`None` negatives. Run retained conditional, nested-function, and raise coverage. Review or test any behavior-neutral internal adjustments against the previous `None` result.

Collection alone or an all-skipped target suite is not success. Record failures and skips. Additional checkout-required public checks remain necessary; focused validation does not establish whole-project correctness.

```arex-contract-v4
{
  "id": "workflow:verified-history:3d852bae39e6f31c4d255bd3:validate",
  "intent": "Observe repaired diagnostics and preserved adjacent behavior.",
  "mechanism": "Execute public positive/negative assertions and retained control-flow expectations.",
  "semantic_role": "return-completeness-validation",
  "owner_role": "return-consistency-regression-suite",
  "operation": "Run bound current public tests without tracked-code edits and record results, skips, failures, and runtime-preservation checks.",
  "kind": "validate",
  "inputs": [
    {"name": "edited-analysis", "semantic_role": "return-analysis-checkout", "artifact_kind": "checkout-binding", "language": "python", "scope": "return-consistency", "phase": "validation", "state": "edited", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "return-consistency-validation", "artifact_kind": "public-test-observations", "language": "python", "scope": "return-consistency", "phase": "validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "exception-aggregation-repaired", "value": true, "evaluator": "evidence"},
    {"key": "regression-matrix-present", "value": true, "evaluator": "evidence"},
    {"key": "role:return-consistency-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-observations-fresh", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "explicit-none-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-control-flow-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-runtime-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "execute-regression-matrix",
      "instruction": "Execute the public current suite. Require both handler-fallthrough positives to warn, both explicit-None negatives not to warn, and retained conditional, nested-function, and raise expectations to remain unchanged. Record actual execution, failures, and skips.",
      "evidence_refs": ["pylint-dev/pylint:3468:regression", "pylint-dev/pylint:3468:fix"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-runtime-neutrality",
      "instruction": "For internal explicit-None edits verify the prior implicit result and new explicit result are both None using public review or focused probes. If no such edits occurred, record that fact from the diff.",
      "evidence_refs": ["pylint-dev/pylint:3468:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:3d852bae39e6f31c4d255bd3:repair"],
  "source_ids": ["pylint-dev/pylint:3468:repair:fb332490c2e5"],
  "evidence_refs": ["pylint-dev/pylint:3468:regression", "pylint-dev/pylint:3468:fix"],
  "read_set": ["role:return-completeness-analyzer", "role:return-consistency-regression-suite", "role:checker-internal-fallthrough-callers"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:3d852bae39e6f31c4d255bd3"
}
```

Bind and render both current Oracles before use. These definitions have not executed; later source qualification cannot substitute for current validation.
