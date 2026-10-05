# Validate target and adjacent behavior

Bind current public commands to the reproduction and regression interfaces. Execute them after editing and record fresh results.

Compare existing inspectable-signature and genuine-delegation expectations with the baseline. Check that the added guard evaluates false for override argument names exactly `["self"]`; do not infer that every self-only wrapper must warn.

```arex-contract-v4
{
  "id": "workflow:verified-history:79391484ce4048a1c8e1217a:validate",
  "intent": "Observe target correction and preservation of adjacent delegation behavior.",
  "mechanism": "Execute public reproduction and regression checks and inspect the narrow guard boundary.",
  "semantic_role": "signature-opacity-validation",
  "owner_role": "delegation-regression-owner",
  "operation": "Run current bound public checks and record fresh target and preservation results without modifying tracked source.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate-repair",
      "semantic_role": "opaque-parent-delegation-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "delegation-diagnostic",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "opaque-parent-delegation-validation",
      "artifact_kind": "test-result",
      "language": "python",
      "scope": "delegation-diagnostic",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "opaque-signature-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "default-message-regression-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "target-false-positive-removed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "inspectable-signature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "self-only-guard-boundary-preserved", "value": true, "evaluator": "evidence"},
    {"key": "fixture-interface-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-default-message",
      "instruction": "Run the public default-message exception reproduction and observe no useless-delegation diagnostic. Confirm the default argument and forwarding behavior remain unchanged.",
      "evidence_refs": ["pylint-dev/pylint:7319:body", "pylint-dev/pylint:7319:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-adjacent-delegation",
      "instruction": "Run current public delegation regression checks. Confirm unchanged inspectable-signature and genuine-delegation expectations, and verify that the added guard excludes self-only overrides.",
      "evidence_refs": ["pylint-dev/pylint:7319:fix", "pylint-dev/pylint:7319:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:79391484ce4048a1c8e1217a:repair"],
  "source_ids": ["pylint-dev/pylint:7319:repair:7fdf8d9ee090"],
  "evidence_refs": ["pylint-dev/pylint:7319:body", "pylint-dev/pylint:7319:fix", "pylint-dev/pylint:7319:regression"],
  "read_set": ["role:delegation-diagnostic-owner", "role:delegation-regression-owner"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:79391484ce4048a1c8e1217a"
}
```

Record PASS/FAIL/UNKNOWN for every current check. UNKNOWN is not success. Failed preservation checks reject acceptance even if the target warning disappears. Expected effects become established only through actual observations.
