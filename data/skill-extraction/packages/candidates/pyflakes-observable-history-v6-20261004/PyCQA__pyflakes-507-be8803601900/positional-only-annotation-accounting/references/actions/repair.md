# Include positional-only arguments

Edit the semantic collector, not a blindly reused historical path. Collect both names and annotations through the same downstream pipeline as ordinary and keyword-only parameters.

The historical change guarded access with `PY38_PLUS`. Determine the current supported-runtime policy before adapting that guard. Preserve existing categories and avoid unrelated refactoring. Review alone does not establish behavioral success; retain the [validation Action](validate.md).

```arex-contract-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
  "intent": "Include positional-only parameter bindings and annotation references in argument accounting.",
  "mechanism": "Append positional-only argument names and annotations before the retained ordinary and keyword-only collection.",
  "semantic_role": "collector-repair",
  "owner_role": "function-argument-collector",
  "operation": "Edit the bound collector to process positional-only AST arguments using the evidenced current runtime compatibility policy.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosed-candidate",
      "semantic_role": "argument-accounting-candidate",
      "artifact_kind": "checkout-with-evidence",
      "language": "python",
      "scope": "function-argument-accounting",
      "phase": "diagnosis",
      "state": "omission-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "implementation-candidate",
      "semantic_role": "argument-accounting-candidate",
      "artifact_kind": "checkout-with-evidence",
      "language": "python",
      "scope": "function-argument-accounting",
      "phase": "implementation",
      "state": "collector-edited-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "collector-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "positional-only-ast-support-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-runtime-policy-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "role:function-argument-collector", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "positional-only-accounting-implemented", "value": true, "evaluator": "evidence", "description": "Expected implementation effect; behavioral success requires current validation."}
  ],
  "preserves": [
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "parameter-binding-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-collector-diff",
      "instruction": "Review the current diff for collection of positional-only names and annotations, retained ordinary and keyword-only processing, and AST access compatible with the reviewed runtime policy. Require the separate validate Action for behavioral acceptance.",
      "evidence_refs": ["PyCQA/pyflakes:507:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:507:repair:be8803601900"],
  "evidence_refs": ["PyCQA/pyflakes:507:fix"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "read_set": ["role:function-argument-collector"],
  "write_set": ["role:function-argument-collector"],
  "invalidates": ["public-validation-fresh"]
}
```
