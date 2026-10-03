# Validate target and adjacent behavior

Bind current public commands. Exercise the async regression, synchronous counterpart, ordinary non-overload redefinition controls, and affected suite. Review or publicly test runtime compatibility.

This Action makes no source edits. Record actual commands, outputs, scope, and PASS/FAIL/UNKNOWN results. Observed validation is not automatically passing validation: acceptance requires passing target and preservation checks. Adjacent controls are current safety obligations, not invented historical execution results.

```arex-contract-v4
{
  "id": "workflow:verified-history:a571de127bfc56dc56819c7c:validate",
  "intent": "Observe repaired async overload behavior and verify preserved adjacent behavior after edits.",
  "mechanism": "Run public regression and diagnostic controls against the edited checkout.",
  "semantic_role": "validate-overload-recognition-repair",
  "owner_role": "overload-regression-tests",
  "operation": "Run bound public reproductions and affected tests, review runtime guards, and record results without source edits.",
  "kind": "validate",
  "inputs": [],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "overload-repair-validation",
      "artifact_kind": "test-result-record",
      "language": "python",
      "scope": "current-checkout-overload-recognition",
      "phase": "post-edit",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "async-overload-recognition-corrected", "value": true, "evaluator": "evidence"},
    {"key": "async-overload-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "sync-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-ast-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "target-and-controls",
      "instruction": "Run current public async and sync typing overload sequences and an ordinary non-overload redefinition control. Require no unused-redefinition warnings for the overload sequences and unchanged diagnostics for the control. Review or publicly test supported-runtime AST guards. Record results; FAIL or unresolved UNKNOWN prevents acceptance.",
      "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "affected-suite",
      "instruction": "Run the current affected overload/type-annotation suite including the async regression and existing sync cases. Record actual scope and results; do not infer whole-project success.",
      "evidence_refs": ["PyCQA/pyflakes:470:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:a571de127bfc56dc56819c7c:extend-function-family",
    "workflow:verified-history:a571de127bfc56dc56819c7c:add-regression"
  ],
  "read_set": ["role:overload-recognition", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a571de127bfc56dc56819c7c"
}
```
