# Register the valid method

Add only the confirmed valid name. Preserve existing entries and diagnostic enforcement. Historically this was `__index__`; other current names require fresh validity and mechanism evidence.

```arex-contract-v4
{
  "id": "workflow:verified-history:6811635fea96a3e3f778e2f1:register",
  "intent": "Correct valid-method rejection through narrow registry membership.",
  "mechanism": "Add the missing valid name to the explicit accepted special-method collection.",
  "semantic_role": "repair-name-acceptance",
  "owner_role": "special-method-acceptance-registry",
  "operation": "Edit the bound consumed registry to include the confirmed valid name once, retaining existing entries and diagnostic logic.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "registry-omission-diagnosis", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed", "optional": false}
  ],
  "outputs": [],
  "preconditions": [
    {"key": "role:special-method-acceptance-registry", "value": true, "evaluator": "symbol_exists", "description": "Resolve the consumed registry symbol in the current checkout."},
    {"key": "registry-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "method-validity-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "registration-edit-present", "value": true, "evaluator": "evidence"},
    {"key": "valid-method-accepted", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "invalid-name-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "inspect-narrow-registration",
      "instruction": "Inspect the diff for one added valid name in the consumed registry, retained existing entries, and unchanged diagnostic enforcement. Behavioral acceptance requires the retained validation Action.",
      "evidence_refs": ["pylint-dev/pylint:8613:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:special-method-acceptance-registry"],
  "write_set": ["role:special-method-acceptance-registry"],
  "source_ids": ["pylint-dev/pylint:8613:repair:f223c6de3a39"],
  "evidence_refs": ["pylint-dev/pylint:8613:fix"],
  "resource": "references/actions/register.md",
  "package_id": "workflow:verified-history:6811635fea96a3e3f778e2f1"
}
```

Effects specify requirements, not observed success. Retain [validation](validate.md) after this edit. Existence predicates use a role key and boolean value.
