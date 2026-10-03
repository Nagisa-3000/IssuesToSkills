# Add or confirm the regression

Use current public test conventions to require an undefined-name diagnostic for isolated `x: int = x`. Ensure there is no preceding binding for `x`. An equivalent existing assertion may satisfy the operation without duplication; do not require the historical test API or name.

The output is a checkout ready for validation, not evidence that any test has passed.

```arex-contract-v4
{
  "id": "annotation-binding-order.regression",
  "intent": "Make the annotated self-reference diagnostic a durable regression requirement.",
  "mechanism": "Assert undefined name for an isolated annotated initializer referencing its unbound target.",
  "semantic_role": "regression-coverage",
  "owner_role": "annotation-diagnostic-tests",
  "operation": "Add or confirm an equivalent public undefined-name assertion.",
  "kind": "edit",
  "inputs": [
    {"name": "edited-handler", "semantic_role": "binding-order-checkout", "artifact_kind": "checkout", "language": "python", "scope": "annotation-analysis-and-tests", "phase": "repair", "state": "handler-edited", "optional": false}
  ],
  "outputs": [
    {"name": "regression-checkout", "semantic_role": "binding-order-checkout", "artifact_kind": "checkout", "language": "python", "scope": "annotation-analysis-and-tests", "phase": "repair", "state": "handler-and-regression-ready", "optional": false}
  ],
  "preconditions": [
    {"key": "role:annotation-diagnostic-tests", "value": true, "evaluator": "symbol_exists"},
    {"key": "target-registration-order", "value": "after-annotation-and-initializer", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "regression-assertion", "value": "present", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-annotation-test-coverage", "value": "retained", "evaluator": "evidence"},
    {"key": "target-registration-order", "value": "after-annotation-and-initializer", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression",
      "instruction": "Inspect the current fixture and expectation. Require x: int = x with no preceding target binding and an assertion for the analyzer's undefined-name diagnostic, not merely parsing success.",
      "evidence_refs": ["PyCQA/pyflakes:728:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:728"],
  "evidence_refs": ["PyCQA/pyflakes:728:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "annotation-binding-order",
  "read_set": ["role:annotation-diagnostic-tests", "role:annotated-assignment-analysis"],
  "write_set": ["role:annotation-diagnostic-tests"],
  "invalidates": ["current-annotation-suite-results"]
}
```
