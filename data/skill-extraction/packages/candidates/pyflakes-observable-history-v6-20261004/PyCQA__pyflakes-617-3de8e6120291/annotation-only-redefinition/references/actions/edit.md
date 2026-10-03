# Make annotation-only bindings non-redefining

The supported implementation specializes the annotation binding's redefinition predicate to return false. It does not disable redefinition checks globally. Bind this operation only when the current owner represents annotation-only statements rather than all annotated assignments.

```arex-contract-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:edit",
  "intent": "Prevent an annotation-only binding from redefining a prior name.",
  "mechanism": "Override the annotation-only redefinition predicate with a false result.",
  "semantic_role": "annotation-redefinition-repair",
  "owner_role": "annotation-binding-owner",
  "operation": "Specialize the current annotation-only binding's redefinition predicate so it cannot redefine another binding; leave ordinary definition predicates unchanged.",
  "kind": "edit",
  "inputs": [
    {"name": "owners", "semantic_role": "confirmed-annotation-redefinition-context", "artifact_kind": "code-binding-record", "language": "python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "implementation", "semantic_role": "annotation-only-redefinition-implementation", "artifact_kind": "source-code", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "candidate", "optional": false}
  ],
  "preconditions": [
    {"key": "annotation-owner-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:annotation-binding-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "annotation-owner-is-value-free", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-only-nonredefining", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-definition-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "inspect-predicate-change",
      "instruction": "Review the current diff: the annotation-only predicate returns false, while ordinary definition classification and value-bearing assignment handling remain unchanged. Runtime confirmation belongs to the retained validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:617:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:annotation-binding-owner", "role:redefinition-predicate-owner"],
  "write_set": ["role:annotation-binding-owner"],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "evidence_refs": ["PyCQA/pyflakes:617:fix"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7"
}
```

The effect is a candidate semantic result until independently reviewed and tested. Retain [validation](validate.md) after this modification.
