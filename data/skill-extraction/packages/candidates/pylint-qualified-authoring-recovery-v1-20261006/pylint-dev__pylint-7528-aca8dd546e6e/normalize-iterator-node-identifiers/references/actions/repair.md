# Normalize iterable identifier selection

In the current shared list/set condition, select `.attrname` for the confirmed Attribute type and `.name` for the confirmed Name type. Use that identifier in the existing comparison. Align the annotation with the established supported shapes where appropriate.

Retain inferred-object equality and receiver-side semantics. Do not silently extend this operation to other node kinds.

```arex-contract-v4
{
  "id": "workflow:verified-history:bc4129e7b226dfae4c87ca01:repair",
  "intent": "Remove unsupported iterable-side .name access for Attribute nodes.",
  "mechanism": "Select the identifier field by the confirmed iterable node kind.",
  "semantic_role": "condition-repair",
  "owner_role": "iteration-condition-owner",
  "operation": "Introduce Attribute.attrname-or-Name.name selection and use it in the existing comparison while retaining inferred-object equality.",
  "kind": "edit",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "role:iteration-condition-owner", "value": true, "evaluator": "symbol_exists"},
    {"key": "supported-node-shapes-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "receiver-name-contract-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "iterable-identifier-selection", "value": "Attribute.attrname-or-Name.name", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "inference-equality-guard-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-iteration-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "separate-copy-not-diagnosed-as-iterated-set", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "unsupported-iterable-node-kind-reachable", "value": true, "evaluator": "evidence"},
    {"key": "receiver-name-access-unsafe", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-identifier-selection",
      "instruction": "Review the current diff for Attribute.attrname and Name.name selection, use of the selected identifier, and unchanged inferred-object equality. Reject receiver normalization, weakened inference, and exception suppression. Retain final public execution in the validate Action.",
      "evidence_refs": ["pylint-dev/pylint:7528:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:iteration-condition-owner", "role:ast-node-api-owner"],
  "write_set": ["role:iteration-condition-owner"],
  "source_ids": ["pylint-dev/pylint:7528:repair:aca8dd546e6e"],
  "evidence_refs": ["pylint-dev/pylint:7528:fix"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:bc4129e7b226dfae4c87ca01"
}
```
