# Correct the truthiness receiver

For a confirmed compatible Python decision path, call `bool_value()` on the successful inference result, not the original expression node.

The historical guard became `inferred_truth_value is None or inferred_truth_value == astroid.Uninferable`; unavailable inference still assigned `True`. Preserve the existing policy and use the explicit guard only when current sentinel semantics are compatible. Do not redesign uncertainty handling or rewrite user expressions.

This modification invalidates validation freshness. Retain the [validation Action](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8:edit",
  "intent": "Correct the receiver used to classify the middle operand's truthiness.",
  "mechanism": "Use the successfully inferred value as the bool_value receiver.",
  "semantic_role": "truthiness-receiver-correction",
  "owner_role": "boolean-refactoring-checker",
  "operation": "Make a narrow receiver correction in the bound Python checker and preserve unavailable-inference behavior; use the evidenced explicit None and sentinel guard only after confirming API compatibility.",
  "kind": "edit",
  "inputs": [
    {"name": "located-mechanism", "semantic_role": "diagnostic-mechanism-binding", "artifact_kind": "review-record", "language": "python", "scope": "boolean-refactoring", "phase": "inspection", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "edited-checker", "semantic_role": "diagnostic-selection-implementation", "artifact_kind": "source-code", "language": "python", "scope": "boolean-refactoring", "phase": "repair", "state": "modified", "optional": false}
  ],
  "preconditions": [
    {"key": "role:boolean-refactoring-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "mechanism-match-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "inferred-value-is-truthiness-receiver", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "truthy-name-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unavailable-inference-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-receiver-edit",
      "instruction": "Review the diff and data flow: successful inference feeds bool_value, the unavailable-inference branch retains its prior policy, and unrelated diagnostic branches are unchanged. Require the separate validation Action for behavioral acceptance.",
      "evidence_refs": ["pylint-dev/pylint:5200:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:boolean-refactoring-checker"],
  "write_set": ["role:boolean-refactoring-checker"],
  "source_ids": ["pylint-dev/pylint:5200:repair:8c7e2fae6fee"],
  "evidence_refs": ["pylint-dev/pylint:5200:fix"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8"
}
```
