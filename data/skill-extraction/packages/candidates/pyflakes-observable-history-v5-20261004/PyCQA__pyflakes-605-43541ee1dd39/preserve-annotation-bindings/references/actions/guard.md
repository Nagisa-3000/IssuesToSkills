# Guard annotation-only insertion

At the bound scope insertion owner, skip replacement only when the name already exists and the incoming binding is annotation-only. Retain insertion for absent names and replacement for ordinary bindings.

Do not use unconditional `setdefault`. Preserve scope selection and surrounding usage metadata propagation.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
  "intent": "Prevent annotation-only declarations from destroying existing binding semantics.",
  "mechanism": "Condition insertion on name absence or a non-annotation incoming binding.",
  "semantic_role": "annotation-binding-preservation",
  "owner_role": "scope-binding-insertion",
  "operation": "Edit the insertion guard while retaining ordinary rebinding and usage propagation.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "annotation-binding-repair-context",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "owners-bound-and-overwrite-confirmed"
    }
  ],
  "outputs": [
    {
      "name": "guard-edit",
      "semantic_role": "annotation-insertion-repair",
      "artifact_kind": "source-edit",
      "language": "python",
      "scope": "current-checkout",
      "phase": "implementation",
      "state": "edited-unvalidated"
    }
  ],
  "preconditions": [
    {"key": "role:scope-binding-insertion", "value": true, "evaluator": "symbol_exists"},
    {"key": "annotation-only-overwrite-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "annotation-classification-compatible", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-preserves-existing-binding", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-bindings-still-replace", "value": true, "evaluator": "evidence"},
    {"key": "absent-name-annotations-still-insert", "value": true, "evaluator": "evidence"},
    {"key": "existing-usage-propagation-retained", "value": true, "evaluator": "evidence"},
    {"key": "scope-selection-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-insertion-guard",
      "instruction": "Review the edited insertion truth table: existing-name annotation retains the entry; absent-name annotation inserts; non-annotation binding replaces. Confirm scope choice and surrounding usage propagation are unchanged.",
      "evidence_refs": ["PyCQA/pyflakes:605:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489",
  "read_set": ["role:scope-binding-insertion", "role:annotation-binding-classifier"],
  "write_set": ["role:scope-binding-insertion"],
  "invalidates": ["annotation-only-overwrite-confirmed", "current-public-validation-passes"]
}
```

The effect is intended, not an executed result. Re-observe it through current review and the explicit [validation Action](validate.md).
