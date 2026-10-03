# Validate target and adjacent behavior

Run current public async and neighboring overload tests. Compare sync/async overload acceptance and ordinary unused-redefinition diagnostics. Review decorator resolution and runtime compatibility.

Bind public current commands before execution. Record commands, runtime, results, skips, and unresolved checks. No supplied evidence establishes historical test execution. Adjacent-behavior probes are current preservation requirements, not invented historical test results.

A required failure or UNKNOWN result blocks acceptance. This validation Action remains attached to the modifying Action even if other already satisfied operations are dropped.

```arex-contract-v4
{
  "id": "workflow:verified-history:a571de127bfc56dc56819c7c:validate",
  "intent": "Verify async overload acceptance and preservation of adjacent behavior.",
  "mechanism": "Execute public regressions and compare overload and ordinary redefinition diagnostics.",
  "semantic_role": "overload-repair-validation",
  "owner_role": "overload-regression-tests",
  "operation": "Run bound public checks after modification and record observed outcomes.",
  "kind": "validate",
  "inputs": [
    {
      "name": "overload-repair",
      "semantic_role": "overload-classification-change",
      "artifact_kind": "source-and-test-diff",
      "language": "python",
      "scope": "current-checkout-overload-analysis",
      "phase": "repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "overload-repair-check-results",
      "artifact_kind": "public-validation-record",
      "language": "python",
      "scope": "current-checkout-overload-analysis",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "repair-diff-available", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "post-edit-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified-by-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "async-overload-regression",
      "instruction": "Run the current public async overload regression and relevant annotation/overload tests using the current repository runner; record outcomes, skips, and runtime.",
      "evidence_refs": ["PyCQA/pyflakes:470:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "overload-adjacency",
      "instruction": "Use public examples to verify sync and async typing overload acceptance and retention of ordinary unused-redefinition diagnostics. Review unchanged typing decorator resolution and supported-runtime guards.",
      "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a571de127bfc56dc56819c7c",
  "read_set": ["role:overload-classification", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": [],
  "validation_for": ["workflow:verified-history:a571de127bfc56dc56819c7c:repair"]
}
```
