# Repair recognition and add regression assertions

For a bare decorator name, search available scopes from inner to outer. Stop at the first binding and require the imported-symbol representation to identify `typing.overload`; do not bypass a shadowing binding. Recognize any matching decorator rather than requiring a singleton list.

Retain the existing function-node restriction and qualified-decorator branch. Wire the scope stack into the diagnostic helper call. Add assertions for class-contained overload declarations and declarations with additional decorators. Apply only missing changes supported by current inspection.

```arex-contract-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:repair",
  "intent": "Correct overload recognition without broadly suppressing unused-redefinition diagnostics.",
  "mechanism": "First-binding import identity resolution across scopes plus existential decorator matching.",
  "semantic_role": "recognition-repair",
  "owner_role": "overload-recognition-and-redefinition-gate",
  "operation": "Edit the bound recognizer and diagnostic call site to use available scope-stack lookup and any-match decorator scanning; add both public regression shapes in the bound annotation suite.",
  "kind": "edit",
  "inputs": [
    {"name": "recognition-context", "semantic_role": "bound-recognition-context", "artifact_kind": "inspection-record", "language": "Python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "applicability-established", "optional": false}
  ],
  "outputs": [
    {"name": "recognition-change", "semantic_role": "recognition-change-under-test", "artifact_kind": "code-and-test-diff", "language": "Python", "scope": "current-public-checkout", "phase": "post-edit", "state": "awaiting-validation", "optional": false}
  ],
  "preconditions": [
    {"key": "recognition-applicability-established", "value": true, "evaluator": "evidence"},
    {"key": "role:overload-recognition-and-redefinition-gate", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:scope-stack-and-import-bindings", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:type-annotation-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "recognition-repair-present", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "first-binding-shadowing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-qualified-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "function-node-restriction-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-recognition-diff",
      "instruction": "Review the diff for first-binding termination, typing.overload import identity, full decorator-list scanning, scope-stack call-site wiring, retained node and qualified-recognition boundaries, unchanged ordinary diagnostic gating, and both regression shapes. Test execution is a separate validation obligation.",
      "evidence_refs": ["PyCQA/pyflakes:434:fix", "PyCQA/pyflakes:434:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:overload-recognition-and-redefinition-gate", "role:scope-stack-and-import-bindings", "role:type-annotation-regression-suite"],
  "write_set": ["role:overload-recognition-and-redefinition-gate", "role:type-annotation-regression-suite"],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs": ["PyCQA/pyflakes:434:fix", "PyCQA/pyflakes:434:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0"
}
```

Effects are intended reviewable changes, not observed test success. Every prior test result must be reconsidered after the edit. Broader import resolution or AST support requires separate evidence.
