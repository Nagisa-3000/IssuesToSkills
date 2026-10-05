# Validate continuation and adjacent behavior

Bind the oracle to the current public harness and render its argv. Run the regression, an enabled-diagnostic control, and adjacent numeric/symbolic disable checks. Review exception propagation and successful registration, adding public targeted probes if the current suite does not cover them.

When a causal base control is available, expect the new regression to expose the missing suppression on the base and pass after repair. Record observations rather than declaring success from contract compatibility. These instructions do not claim the historical author executed these controls.

```arex-contract-v4
{
  "id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:validate",
  "intent": "Observe repaired suppression and preserved adjacent behavior after all retained edits.",
  "mechanism": "Run public mixed-ID regression and adjacent checks; review the narrow exception boundary.",
  "semantic_role": "repair-validation",
  "owner_role": "configuration-regression",
  "operation": "Execute bound public checks and inspect current code without modifying tracked files; record results and refresh validation freshness.",
  "kind": "validate",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "missing-advisory-id-tolerated", "value": true, "evaluator": "evidence"},
    {"key": "mixed-id-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "known-numeric-registration-preserved", "value": true, "evaluator": "evidence"},
    {"key": "symbolic-disable-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-errors-not-suppressed", "value": true, "evaluator": "evidence"},
    {"key": "existing-test-expectations-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "public-regression-and-neighbors",
      "instruction": "Run the current mixed-ID configuration test and neighboring disable tests. Observe that the later valid disable suppresses its diagnostic, the enabled control emits it, known numeric IDs still register advisory tuples, symbolic disables still work, and non-KeyError exceptions remain uncaught by the new boundary. Record argv, exit status, diagnostic output, and anchored review evidence.",
      "evidence_refs": ["pylint-dev/pylint:4265:fix", "pylint-dev/pylint:4265:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:guard",
    "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:regression"
  ],
  "read_set": ["role:disable-bookkeeping", "role:message-registry", "role:configuration-regression"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4265:repair:c92e3ab78778"],
  "evidence_refs": ["pylint-dev/pylint:4265:fix", "pylint-dev/pylint:4265:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b"
}
```
