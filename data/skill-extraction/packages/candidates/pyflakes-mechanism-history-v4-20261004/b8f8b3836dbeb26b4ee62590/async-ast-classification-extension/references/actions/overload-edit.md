# Extend overload classification and cover async declarations

Widen only the confirmed synchronous-only source-node gate to the runtime-supported function family. Reuse an existing equivalent family where possible. Preserve decorator identity checks and surrounding redefinition rules.

Provide missing no-diagnostic coverage for two decorated async declarations followed by an undecorated async implementation. Handle syntax-dependent coverage according to current runtime policy. Equivalent existing coverage may satisfy the test effect without another test edit.

```arex-contract-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-edit",
  "intent": "Recognize async typing overloads through the existing exemption and cover the sequence.",
  "mechanism": "Widen the supported function-node classification without changing decorator identity or diagnostic semantics.",
  "semantic_role": "extend-classification-and-cover",
  "owner_role": "overload-recognition",
  "operation": "Edit the bound source-node predicate and guarded family if needed, and add missing public async overload coverage while retaining existing assertions.",
  "kind": "edit",
  "inputs": [
    {"name": "overload-review", "semantic_role": "overload-omission-context", "artifact_kind": "code-and-probe-record", "language": "python", "scope": "current-overload-classification", "phase": "pre-edit", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "overload-change", "semantic_role": "overload-validation-target", "artifact_kind": "code-and-test-change", "language": "python", "scope": "current-overload-classification", "phase": "post-edit", "state": "unvalidated", "optional": false}
  ],
  "preconditions": [
    {"key": "classification-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-function-semantics-appropriate", "value": true, "evaluator": "evidence"},
    {"key": "runtime-policy-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "role:overload-recognition", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:function-node-family", "value": true, "evaluator": "file_exists"},
    {"key": "role:overload-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "async-classification-extended", "value": true, "evaluator": "evidence"},
    {"key": "async-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-function-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-compatibility-preserved", "value": true, "evaluator": "evidence"},
    {"key": "downstream-semantics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-overload-change",
      "instruction": "Inspect the actual diff: only function-node classification is widened; typing decorator identity and surrounding redefinition logic remain unchanged. Confirm capability-guarded AST references and new or equivalent no-diagnostic coverage for two decorated async declarations plus an async implementation. Retain fresh overload validation.",
      "evidence_refs": ["PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:overload-recognition", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": ["role:overload-recognition", "role:function-node-family", "role:overload-regression-tests"],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/overload-edit.md",
  "package_id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590"
}
```
