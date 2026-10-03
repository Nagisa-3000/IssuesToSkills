# Partition type and metadata traversal

Bind to current semantic owners, not historical paths.

For recognized `Annotated` subscripts, visit the target normally and identify the supported tuple representation. The historical implementation accepts direct `ast.Tuple` and `ast.Index` wrapping `ast.Tuple`.

If no multi-argument tuple exists, preserve normal slice traversal. Otherwise visit the first argument in its existing context and all remaining arguments within a scoped ordinary-expression state that restores the prior annotation state. Preserve context-node traversal and existing `Literal` behavior.

Respect current recognition conventions. Do not add unsupported alias resolution or adopt terminal-name matching when it conflicts with current semantics.

Add focused regression assertions for metadata strings, missing forward types, and nesting. Metadata names must still receive ordinary expression analysis. Expected effects below require subsequent validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
  "intent": "Correct the boundary between the Annotated type argument and metadata.",
  "mechanism": "Position-sensitive traversal with scoped ordinary-expression state for metadata.",
  "semantic_role": "boundary-repair",
  "owner_role": "python-annotation-subscript-analysis",
  "operation": "Edit Annotated traversal and add focused regression assertions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "boundary-context",
      "semantic_role": "annotation-boundary-context",
      "artifact_kind": "code-and-probe-record",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "inspected",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "boundary-context",
      "semantic_role": "annotation-boundary-context",
      "artifact_kind": "code-and-probe-record",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "edited",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "role:python-annotation-subscript-analysis", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:python-annotation-state-controller", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:python-annotation-regression-suite", "value": true, "evaluator": "file_exists"},
    {"key": "metadata-forward-parsing-defect-observed", "value": true, "evaluator": "evidence"},
    {"key": "scoped-state-transition-compatible", "value": true, "evaluator": "evidence"},
    {"key": "annotated-recognition-compatible", "value": true, "evaluator": "evidence"},
    {"key": "supported-slice-shapes-observed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "metadata-string-forward-parsing", "value": false, "evaluator": "evidence"},
    {"key": "boundary-regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "first-argument-type-analysis", "value": "preserved", "evaluator": "evidence"},
    {"key": "metadata-expression-analysis", "value": "preserved", "evaluator": "evidence"},
    {"key": "surrounding-annotation-state", "value": "preserved", "evaluator": "evidence"},
    {"key": "literal-handling", "value": "preserved", "evaluator": "evidence"},
    {"key": "target-context-and-fallback-traversal", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-partition",
      "instruction": "Review the diff for first-argument traversal in the prior context, ordinary traversal of every metadata argument, state restoration, supported slice shapes, fallback and target/context traversal, preserved Literal handling, and focused regression assertions. This review does not replace validation.",
      "evidence_refs": ["PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "evidence_refs": ["PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6",
  "read_set": [
    "role:python-annotation-subscript-analysis",
    "role:python-annotation-state-controller",
    "role:python-annotation-regression-suite"
  ],
  "write_set": [
    "role:python-annotation-subscript-analysis",
    "role:python-annotation-regression-suite"
  ],
  "invalidates": [
    "pre-edit-code-anchors",
    "pre-edit-reproduction-result",
    "pre-edit-regression-results"
  ],
  "exclusions": [
    {"key": "requested-global-metadata-diagnostic-suppression", "value": true, "evaluator": "evidence"}
  ]
}
```
