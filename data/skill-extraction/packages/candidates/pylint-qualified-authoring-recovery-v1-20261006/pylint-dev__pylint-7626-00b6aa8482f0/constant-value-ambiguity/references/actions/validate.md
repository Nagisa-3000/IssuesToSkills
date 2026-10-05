# Validate suppression and preserved definite behavior

Bind public commands to the current checkout. Check both changed behavior and preserved behavior, including the default safe-inference interface. Do not regard an updated expected-output file as evidence that runtime behavior passed.

```arex-contract-v4
{
  "id": "workflow:verified-history:b8f0f43a57ace4a8864a27f3:validate",
  "intent": "Observe that the repair suppresses unsafe suggestions without removing valid definite-value diagnostics.",
  "mechanism": "Run public reproduction, inference probes, and regression tests with ambiguous and definite controls.",
  "semantic_role": "repair-validation",
  "owner_role": "python-public-regression-harness",
  "operation": "Execute bound public checks, inspect diagnostic outputs and confidence metadata, and record fresh results with current code hashes. This Action does not modify source or expected outputs.",
  "kind": "validate",
  "inputs": [
    {
      "name": "patched-boundary",
      "semantic_role": "constant-ambiguity-repair-artifact",
      "artifact_kind": "checkout-diff",
      "language": "python",
      "scope": "safe-inference-and-boolean-rewrite",
      "phase": "post-edit",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "constant-ambiguity-validation",
      "artifact_kind": "public-test-results",
      "language": "python",
      "scope": "safe-inference-and-boolean-rewrite",
      "phase": "post-validation",
      "state": "observed-results",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:python-public-regression-harness", "value": true, "evaluator": "file_exists"},
    {"key": "public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "default-inference-contract-preserved", "value": true, "evaluator": "evidence"},
    {"key": "definite-value-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-reproduction",
      "instruction": "Run the public loop-reassignment reproduction. Verify that the result remains True and no unsafe Boolean simplification is suggested. Verify unknown and uninferable operands emit neither rewrite diagnostic.",
      "evidence_refs": ["pylint-dev/pylint:7626:body", "pylint-dev/pylint:7626:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-inference-and-controls",
      "instruction": "Run current public inference and regression checks. With comparison enabled, unequal same-type constants must be ambiguous; equal constants must remain inferable. Default-disabled behavior and different-type ambiguity handling must remain intact. Definite truthy and falsy controls must retain expected diagnostics and inference confidence. Record failures and skipped checks explicitly.",
      "evidence_refs": ["pylint-dev/pylint:7626:fix", "pylint-dev/pylint:7626:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:b8f0f43a57ace4a8864a27f3:repair"],
  "source_ids": ["pylint-dev/pylint:7626:repair:00b6aa8482f0"],
  "evidence_refs": ["pylint-dev/pylint:7626:body", "pylint-dev/pylint:7626:fix", "pylint-dev/pylint:7626:regression"],
  "read_set": ["role:python-safe-inference-helper", "role:python-boolean-rewrite-consumer", "role:python-public-regression-harness"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:b8f0f43a57ace4a8864a27f3"
}
```

The effect means results were observed, not that they passed. Require PASS for both correctness and preservation oracles before accepting the repair. UNKNOWN is not success. Each current Oracle binding uses semantic check key `oracle:<action_id>:<source_oracle_id>` and records current instructions, argv, and public evidence references.
