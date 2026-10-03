# Repair supported overload recognition

At the bound recognizer, replace immediate-scope name lookup with innermost-first scope-stack lookup. Return at the first matching binding: accept the supported import-from identity for `typing.overload`, otherwise reject.

Inspect all decorators rather than requiring exactly one. At the reporting owner, pass the scope stack while continuing to inspect the existing binding. Preserve the function-source guard and existing attribute branch.

These are expected effects, not observed execution results. Retain the [validation Action](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:repair",
  "intent": "Correct overload recognition for enclosing imports and multiple decorators.",
  "mechanism": "Innermost-first binding resolution and any-decorator recognition.",
  "semantic_role": "recognizer-repair",
  "owner_role": "overload-recognition",
  "operation": "Edit the recognizer and its unused-redefinition call site.",
  "kind": "edit",
  "inputs": [
    {"name": "assessment", "semantic_role": "overload-repair-assessment", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "inspection", "state": "assessed", "optional": false}
  ],
  "outputs": [
    {"name": "repair", "semantic_role": "overload-recognition-change", "artifact_kind": "source-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "modified", "optional": false}
  ],
  "preconditions": [
    {"key": "role:overload-recognition", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:unused-redefinition-reporting", "value": true, "evaluator": "symbol_exists"},
    {"key": "historical-mechanism-applicable", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "supported-overloads-recognized", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nearest-binding-shadowing", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-redefinition-reporting", "value": "preserved", "evaluator": "evidence"},
    {"key": "existing-attribute-recognition", "value": "preserved", "evaluator": "evidence"},
    {"key": "function-source-guard", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-recognition-change",
      "instruction": "Review that lookup stops at the nearest binding, uses supported import identity, scans every decorator, and receives the scope stack when inspecting the existing binding.",
      "evidence_refs": ["PyCQA/pyflakes:434:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs": ["PyCQA/pyflakes:434:fix"],
  "read_set": ["role:overload-recognition", "role:unused-redefinition-reporting"],
  "write_set": ["role:overload-recognition", "role:unused-redefinition-reporting"],
  "invalidates": ["current-diagnostic-observations", "public-validation-passed"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0"
}
```
