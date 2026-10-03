# Analyze the initializer before installing the target binding

Move the target visit from before annotation processing to after annotation and initializer processing. Keep the initializer's existing conditional branches intact. Do not substitute ordinary expression handling for an initializer branch that the analyzer treats as an annotation.

The historical implementation is narrowly evidenced by a single removed target visit and a single reinserted target visit. Adapt the semantic operation to the located current handler; do not blindly apply a historical line-number patch.

```arex-contract-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b:reorder",
  "intent": "Prevent the new annotated-assignment target binding from hiding an undefined initializer reference.",
  "mechanism": "Delay the target visit until after annotation and optional initializer analysis.",
  "semantic_role": "repair-binding-order",
  "owner_role": "annotated-assignment-handler",
  "operation": "Relocate target handling after the existing annotation and initializer handling without changing those branches.",
  "kind": "edit",
  "inputs": [
    {
      "name": "reviewed-handler",
      "semantic_role": "annotated-assignment-handler",
      "artifact_kind": "source-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "reviewed-premature-binding"
    }
  ],
  "outputs": [
    {
      "name": "corrected-handler",
      "semantic_role": "annotated-assignment-handler",
      "artifact_kind": "source-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "target-visit-delayed"
    }
  ],
  "preconditions": [
    {
      "key": "role:annotated-assignment-handler",
      "value": true,
      "evaluator": "symbol_exists"
    },
    {
      "key": "premature-target-binding-confirmed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "effects": [
    {
      "key": "initializer-analyzed-before-new-target-binding",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "annotation-processing-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "initializer-special-branches-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "target-still-visited-without-initializer",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "binding-order-review",
      "instruction": "Review the edited handler: annotation processing remains, initializer processing retains its existing branches, and target visitation occurs afterward even when no initializer is present. Behavioral acceptance requires the linked validate Action.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:fix"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:annotated-assignment-handler"
  ],
  "write_set": [
    "role:annotated-assignment-handler"
  ],
  "invalidates": [
    "target-and-adjacent-checks-pass",
    "observed-annotated-self-reference-diagnostics"
  ],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:728:fix"
  ],
  "resource": "references/actions/reorder.md",
  "package_id": "workflow:verified-history:88cc33218756cccdf2ac071b"
}
```
