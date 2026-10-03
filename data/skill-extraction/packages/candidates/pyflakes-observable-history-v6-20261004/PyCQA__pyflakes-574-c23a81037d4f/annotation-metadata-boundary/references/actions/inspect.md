# Inspect current applicability

Read the current Python AST subscript visitor, annotation-state manager, and annotation-test owner. Resolve real bindings and code anchors. Inspect the public reproduction, name/attribute recognition conventions, and supported tuple/index slice shapes.

This operation makes no source edits. Its output is an expected review artifact to be produced by current inspection, not an observation already obtained.

```arex-contract-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:inspect",
  "intent": "Establish whether the supported metadata-context defect exists.",
  "mechanism": "Inspect annotation traversal and publicly probe metadata misclassification.",
  "semantic_role": "applicability-inspection",
  "owner_role": "annotation-subscript-visitor",
  "operation": "Read current traversal and state code, bind semantic owners, and record public reproduction diagnostics and AST slice layouts without modifying source files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspection",
      "semantic_role": "annotation-boundary-inspection",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "applicability-assessed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "type-reference-checking-preserved", "value": true, "evaluator": "evidence"},
    {"key": "enclosing-annotation-state-preserved", "value": true, "evaluator": "evidence"},
    {"key": "literal-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-expression-checking-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-boundary",
      "instruction": "Inspect public owner code and probe Annotated[int, '>1']; record whether metadata enters forward parsing, current owner bindings and supported AST layouts. Record PASS, FAIL or UNKNOWN without source edits.",
      "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:annotation-subscript-visitor",
    "role:annotation-state-manager",
    "role:annotation-regression-tests"
  ],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6"
}
```

An assessed result can be insufficient or inapplicable. `applicability-assessed` does not assert that editing is authorized.
