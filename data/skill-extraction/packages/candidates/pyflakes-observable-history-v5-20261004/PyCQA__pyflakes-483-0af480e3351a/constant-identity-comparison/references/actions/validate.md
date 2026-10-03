# Validate target and adjacent behavior

Bind and execute a current public test command for the located regression owner. Supplement with public reproductions when assertions do not cover required boundaries. Record exit status, diagnostic output, and coverage limits.

The historical additions assert `IsLiteral` for empty and nested constant tuples and no diagnostic for the variable-containing tuple example. Historical execution is unknown. Current execution must independently establish results.

```arex-contract-v4
{
  "id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f:validate",
  "intent": "Observe whether the repair achieves the target and preserves adjacent behavior.",
  "mechanism": "Execute current public regression tests and boundary reproductions after editing.",
  "semantic_role": "constant-identity-validation",
  "owner_role": "identity_regression_tests",
  "operation": "Run bound public checks and record results, failures, and unknown coverage.",
  "kind": "validate",
  "inputs": [
    {
      "name": "diagnostic_patch",
      "semantic_role": "identity-diagnostic-change",
      "artifact_kind": "checkout-diff",
      "language": "Python",
      "scope": "identity-literal-diagnostic",
      "phase": "post-repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation_results",
      "semantic_role": "identity-diagnostic-validation",
      "artifact_kind": "test-result-record",
      "language": "Python",
      "scope": "identity-literal-diagnostic",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:identity_regression_tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "A result record exists; its actual checks determine success or failure."}
  ],
  "preserves": [
    {"key": "checkout-code-unchanged-by-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-identity-regressions",
      "instruction": "Execute bound public regression checks. Observe diagnostics for empty and nested constant tuples; no identity-literal diagnostic for variable-containing tuples or singleton-only identity operands; preserved scalar diagnostics, operand symmetry, is not, chained pairs, and normal child traversal. Record untested runtime branches and wider coverage as unknown, not passed.",
      "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:e84da27a5b8d26a58fc90e6f:repair"],
  "read_set": ["role:constant_classifier", "role:identity_comparison_checker", "role:identity_diagnostic", "role:identity_regression_tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:483:repair:0af480e3351a"],
  "evidence_refs": ["PyCQA/pyflakes:483:fix", "PyCQA/pyflakes:483:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:e84da27a5b8d26a58fc90e6f"
}
```
