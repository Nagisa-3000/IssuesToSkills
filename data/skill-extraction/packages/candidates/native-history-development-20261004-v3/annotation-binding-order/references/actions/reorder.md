# Delay target registration

In the bound current handler, relocate the existing target-handling operation after annotation and optional initializer analysis. Preserve annotation calls, the value-presence guard, specialized dispatch, and annotation-only support.

Review the full current handler; do not copy historical line numbers or invent the branch condition omitted from the historical diff. Expected effects below require current review and subsequent public validation.

```arex-contract-v4
{
  "id": "annotation-binding-order.reorder",
  "intent": "Prevent the target from resolving its own otherwise-unbound initializer reference.",
  "mechanism": "Delay target registration until annotation and optional initializer processing finish.",
  "semantic_role": "binding-order-repair",
  "owner_role": "annotated-assignment-analysis",
  "operation": "Relocate target handling while retaining existing annotation and initializer paths.",
  "kind": "edit",
  "inputs": [
    {"name": "mechanism-review", "semantic_role": "binding-order-review", "artifact_kind": "review-record", "language": "python", "scope": "annotated-assignment-analysis", "phase": "diagnosis", "state": "mechanism-confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "edited-handler", "semantic_role": "binding-order-checkout", "artifact_kind": "checkout", "language": "python", "scope": "annotation-analysis-and-tests", "phase": "repair", "state": "handler-edited", "optional": false}
  ],
  "preconditions": [
    {"key": "early-target-registration", "value": true, "evaluator": "evidence"},
    {"key": "role:annotated-assignment-analysis", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "target-registration-order", "value": "after-annotation-and-initializer", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "annotation-and-specialized-value-analysis", "value": "retained", "evaluator": "evidence"},
    {"key": "optional-initializer-support", "value": "retained", "evaluator": "evidence"},
    {"key": "ordinary-self-reference-diagnostic", "value": "undefined-name", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-reordering",
      "instruction": "Review the current diff and control flow. Confirm target registration follows annotation and optional initializer analysis, preserving annotation calls, initializer guards, specialized dispatch, and the path with no initializer.",
      "evidence_refs": ["PyCQA/pyflakes:728:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:728"],
  "evidence_refs": ["PyCQA/pyflakes:728:fix"],
  "resource": "references/actions/reorder.md",
  "package_id": "annotation-binding-order",
  "read_set": ["role:annotated-assignment-analysis"],
  "write_set": ["role:annotated-assignment-analysis"],
  "invalidates": ["current-diagnostic-results", "current-annotation-suite-results"]
}
```
