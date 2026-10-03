# Extend the function-node gate

Replace the confirmed synchronous-only check with the current supported function-node family. Reuse an existing equivalent family when possible; otherwise introduce a guarded family.

Preserve typing decorator identity checks and surrounding binding/redefinition logic. Do not globally suppress async redefinition warnings. Historical node classes and runtime guards are not assumed to match a current backend.

Existence predicates resolve current semantic owners and have boolean values. Effects below are expected until reviewed and validated.

```arex-contract-v4
{
  "id": "workflow:verified-history:a571de127bfc56dc56819c7c:extend-function-family",
  "intent": "Recognize async typing overload definitions through the existing exemption.",
  "mechanism": "Widen only the overload function-node gate to the runtime-supported function AST family.",
  "semantic_role": "repair-overload-function-node-gate",
  "owner_role": "overload-recognition",
  "operation": "Edit the source-node predicate and, if needed, its guarded node family while retaining decorator identity checks.",
  "kind": "edit",
  "inputs": [
    {
      "name": "recognition-review",
      "semantic_role": "overload-node-omission-review",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout-overload-recognition",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "outputs": [],
  "preconditions": [
    {"key": "async-function-node-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:overload-recognition", "value": true, "evaluator": "symbol_exists", "description": "The current overload-recognition symbol is located and bound."},
    {"key": "role:function-node-family", "value": true, "evaluator": "file_exists", "description": "The current owner resource for supported function-node types and runtime policy is located and bound."}
  ],
  "effects": [
    {"key": "async-overload-recognition-corrected", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "sync-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-ast-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-gate-edit",
      "instruction": "Review the current diff. Confirm only the function-node family is widened, typing decorator checks remain intact, and unavailable AST classes remain guarded according to current runtime policy.",
      "evidence_refs": ["PyCQA/pyflakes:470:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:overload-recognition", "role:function-node-family"],
  "write_set": ["role:overload-recognition", "role:function-node-family"],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:fix"],
  "resource": "references/actions/extend-function-family.md",
  "package_id": "workflow:verified-history:a571de127bfc56dc56819c7c"
}
```
