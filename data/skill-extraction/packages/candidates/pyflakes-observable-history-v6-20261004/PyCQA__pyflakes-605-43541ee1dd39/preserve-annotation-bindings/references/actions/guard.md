# Guard annotation-only replacement

Apply the narrow guard at the current shared binding insertion owner. Insert the incoming binding if the name is absent, or if the incoming binding is not annotation-only. Do not replace all updates with `setdefault`: that would also suppress ordinary replacement.

Preserve surrounding use-state handling. The historical implementation is recorded in the [fix evidence](../evidence/fix.md); its names are not mandatory current bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
  "intent": "Retain an existing binding when the incoming binding is annotation-only.",
  "mechanism": "Condition scope replacement on name absence or non-annotation incoming binding.",
  "semantic_role": "annotation-replacement-guard",
  "owner_role": "scope-binding-insertion-owner",
  "operation": "Edit the current scope update to skip replacing an existing entry for an incoming annotation-only binding, while retaining ordinary replacement and absent-name insertion.",
  "kind": "edit",
  "inputs": [
    {"name": "reviewed-bindings", "semantic_role": "annotation-binding-repair-context", "artifact_kind": "binding-map", "language": "Python", "scope": "current-checkout", "phase": "review", "state": "reviewed"}
  ],
  "outputs": [
    {"name": "guarded-updater", "semantic_role": "annotation-safe-binding-updater", "artifact_kind": "source-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "edited"}
  ],
  "preconditions": [
    {"key": "owner-located", "value": true, "evaluator": "symbol_exists", "description": "role:scope-binding-insertion-owner"},
    {"key": "annotation-overwrite-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-replacement-guard-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-rebinding-preserved", "value": true, "evaluator": "evidence"},
    {"key": "absent-name-annotation-insertion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "annotation-expression-use-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-narrow-guard",
      "instruction": "Review the public diff: only annotation-only replacement of an existing name is suppressed; absent-name insertion, non-annotation replacement, and surrounding use-state handling remain.",
      "evidence_refs": ["PyCQA/pyflakes:605:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:fix"],
  "read_set": ["role:scope-binding-insertion-owner", "role:annotation-binding-classifier"],
  "write_set": ["role:scope-binding-insertion-owner"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489"
}
```

Validation is mandatory through the [validation Action](validate.md).
