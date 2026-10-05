# Restrict fallback receiver classification and add assertions

Use current boundness semantics, not parameter spelling. In the evidenced fallback branch, reject an unbound nearest function before interpreting its first argument as a mandatory receiver. Preserve the existing absence and no-argument checks and legitimate receiver-stack logic.

Add ordinary-function and static-method protected-property accesses with explicit expected diagnostics. Retain the fixture's earlier expectations.

The historical companion change skips call-node expressions in a related checker branch rather than only specialized self-type calls. Apply that change only if inspection establishes the same branch and compatible expression semantics; otherwise document that it is absent or already satisfied. Do not infer an additional causal explanation from the diff alone.

```arex-contract-v4
{
  "id": "workflow:verified-history:5eae2300be395ac5633f17e5:repair",
  "intent": "Remove an accidental unbound-parameter exemption and encode its diagnostic boundary.",
  "mechanism": "Gate fallback first-argument receiver classification on function boundness and add ordinary-function/static-method regression assertions.",
  "semantic_role": "repair-receiver-exemption",
  "owner_role": "receiver-classifier",
  "operation": "Edit the located receiver classifier so an unbound nearest function returns false before its first argument can be treated as an implicit receiver. Preserve no-function, no-argument, and established bound-receiver handling. Add public protected-property diagnostic assertions for a static method and an ordinary function, retaining old expectations. For an evidenced equivalent related expression branch, retain or restore the historical general call-node skip; do not transplant it into an incompatible branch.",
  "kind": "edit",
  "inputs": [
    {
      "name": "mechanism-review",
      "semantic_role": "receiver-exemption-applicability",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "repair-delta",
      "semantic_role": "receiver-exemption-repair",
      "artifact_kind": "source-and-test-diff",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "receiver-exemption-mechanism-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "unbound-first-parameter-suppression-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "boundness-api-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:receiver-classifier", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:protected-access-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:protected-access-fixtures", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "unbound-first-parameter-exemption-rejected", "value": true, "evaluator": "evidence"},
    {"key": "external-protected-access-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "legitimate-bound-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-protected-access-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "call-expression-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-boundness-delta",
      "instruction": "Review the current diff: an unbound nearest function must be rejected before first-argument receiver classification; existing receiver-stack and empty-argument checks must remain. Confirm both new public diagnostic assertions and retention of earlier expectations. Review any companion call-node change against the located branch. Treat behavior effects as expected until post-edit validation runs.",
      "evidence_refs": ["pylint-dev/pylint:5989:fix", "pylint-dev/pylint:5989:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5989:repair:5c8384e811e3"],
  "evidence_refs": ["pylint-dev/pylint:5989:fix", "pylint-dev/pylint:5989:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:5eae2300be395ac5633f17e5",
  "read_set": ["role:receiver-classifier", "role:protected-access-checker", "role:protected-access-fixtures"],
  "write_set": ["role:receiver-classifier", "role:protected-access-checker", "role:protected-access-fixtures"],
  "invalidates": ["current-public-validation-observed", "current-diagnostic-observations-fresh"]
}
```
