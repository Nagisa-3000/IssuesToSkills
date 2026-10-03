# Validate repair and preservation

Execute current-bound public reproductions and tests. Record argv, revision, actual diagnostics, exit status, selected test scope, counts, and failures. Review preserved analysis paths and use applicable public tests or probes for annotation-only and previously bound-name behavior.

When publicly available, an original-base control can demonstrate that the regression distinguishes defective behavior from the repaired handler. That control is a current validation option, not an invented historical test run.

This Action validates both modifications. Missing checks remain UNKNOWN; observed failures remain FAIL. Neither may become a fully validated repair claim.

```arex-contract-v4
{
  "id": "annotation-binding-order.validate",
  "intent": "Verify restored undefined-name reporting and preserved adjacent annotation analysis.",
  "mechanism": "Execute public reproductions and annotation tests with a preservation review.",
  "semantic_role": "repair-validation",
  "owner_role": "annotation-diagnostic-tests",
  "operation": "Run current bound public oracles and record tri-state results with checkout identity.",
  "kind": "validate",
  "inputs": [
    {"name": "regression-checkout", "semantic_role": "binding-order-checkout", "artifact_kind": "checkout", "language": "python", "scope": "annotation-analysis-and-tests", "phase": "repair", "state": "handler-and-regression-ready", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "binding-order-validation", "artifact_kind": "test-report", "language": "python", "scope": "annotation-analysis-and-tests", "phase": "verification", "state": "checks-recorded", "optional": false}
  ],
  "preconditions": [
    {"key": "regression-assertion", "value": "present", "evaluator": "evidence"},
    {"key": "current-oracle-bindings", "value": "recorded", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "current-validation-results", "value": "recorded", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-self-reference-diagnostic", "value": "undefined-name", "evaluator": "evidence"},
    {"key": "annotation-and-specialized-value-analysis", "value": "retained", "evaluator": "evidence"},
    {"key": "optional-initializer-support", "value": "retained", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "annotated-self-reference",
      "instruction": "Execute isolated x: int = x and x = x probes in the current checkout. Require an undefined-name diagnostic for initializer x in each. Capture actual diagnostics rather than relying on exit status alone.",
      "evidence_refs": ["PyCQA/pyflakes:728:body", "PyCQA/pyflakes:728:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-regression-suite",
      "instruction": "Execute the isolated regression and relevant current public annotation suite. Record selected tests and results. Review annotation calls, optional-value handling, and specialized dispatch; check annotation-only and previously bound-name behavior using applicable public tests or probes. Mark missing evidence UNKNOWN and state actual validation scope.",
      "evidence_refs": ["PyCQA/pyflakes:728:fix", "PyCQA/pyflakes:728:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:728"],
  "evidence_refs": ["PyCQA/pyflakes:728:body", "PyCQA/pyflakes:728:fix", "PyCQA/pyflakes:728:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "annotation-binding-order",
  "read_set": ["role:annotated-assignment-analysis", "role:annotation-diagnostic-tests"],
  "write_set": [],
  "validation_for": ["annotation-binding-order.reorder", "annotation-binding-order.regression"]
}
```
