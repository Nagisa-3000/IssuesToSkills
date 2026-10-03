# Validate public behavior and adjacent diagnostics

Bind commands to current public owners before execution. Exercise `print *= -1` and `print += 1`, then run the added regression and relevant existing ordinary-load, assignment, and incompatible-print tests. Review every caller of the changed interface.

No historical execution command is supplied. Empty command arrays require current Oracle bindings; they are not executable authorization.

```arex-contract-v4
{
  "id": "workflow:verified-history:73c1883f7ed05d43025127fa:validate",
  "intent": "Observe crash removal and preservation of adjacent behavior after the explicit-parent edit.",
  "mechanism": "Use public reproductions, repository regression tests, and caller-completeness review.",
  "semantic_role": "parent-context-validation",
  "owner_role": "regression-test-owner",
  "operation": "Execute current bound public checks and review affected callers, recording outcomes, actual scope, and code anchors without source edits.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "explicit-parent-context-candidate",
      "artifact_kind": "source-and-test-change",
      "language": "python",
      "scope": "bound-load-analysis-and-regression-tests",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "parent-context-validation",
      "artifact_kind": "public-check-record",
      "language": "python",
      "scope": "bound-load-analysis-and-regression-tests",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "explicit-parent-context-installed", "value": true, "evaluator": "evidence"},
    {"key": "augmented-load-regression-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-load-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "builtin-print-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "augmented-value-target-order-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "augmented-load-no-crash",
      "instruction": "Run the current public analyzer on print *= -1 and print += 1. Check that neither causes the missing-parent AttributeError or an internal analyzer failure; record actual outcomes.",
      "evidence_refs": ["PyCQA/pyflakes:744:body", "PyCQA/pyflakes:744:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-regression-checks",
      "instruction": "Run the added regression and relevant existing public ordinary-load, print-assignment, and incompatible-print tests. Review every affected caller and value/target traversal order. Record failures and actual test scope rather than inferring whole-project success.",
      "evidence_refs": ["PyCQA/pyflakes:744:fix", "PyCQA/pyflakes:744:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:73c1883f7ed05d43025127fa:repair"],
  "read_set": [
    "role:load-analysis-owner",
    "role:early-load-dispatch-owner",
    "role:ordinary-load-dispatch-owner",
    "role:regression-test-owner"
  ],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:744:repair:e0d7a6be8959"],
  "evidence_refs": ["PyCQA/pyflakes:744:body", "PyCQA/pyflakes:744:fix", "PyCQA/pyflakes:744:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:73c1883f7ed05d43025127fa"
}
```

An observed validation output may contain failures. Required semantic checks must be PASS before acceptance; FAIL or UNKNOWN is not converted into success by creating a record. Any subsequent source edit requires fresh validation. Independent hidden acceptance is outside these public instructions.
