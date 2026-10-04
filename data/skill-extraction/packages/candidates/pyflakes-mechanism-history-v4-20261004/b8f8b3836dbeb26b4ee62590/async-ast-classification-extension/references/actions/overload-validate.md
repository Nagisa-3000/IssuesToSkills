# Validate overload classification

Run async and sync typing overload sequences, ordinary non-overload redefinition controls, and the affected suite. Review capability guards and unchanged decorator/diagnostic semantics.

Record actual commands, outputs, scope, and PASS/FAIL/UNKNOWN without source edits. A failed or unresolved check prevents acceptance. Adjacent controls are current obligations, not invented historical execution.

```arex-contract-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-validate",
  "intent": "Observe corrected async overload analysis and preserved diagnostic behavior.",
  "mechanism": "Run public overload targets and diagnostic controls against the extended classification.",
  "semantic_role": "validate-target-and-preservation",
  "owner_role": "overload-regression-tests",
  "operation": "Execute bound public target, control and affected-suite checks; review runtime guards and unchanged downstream semantics without source or expectation edits.",
  "kind": "validate",
  "inputs": [
    {"name": "overload-change", "semantic_role": "overload-validation-target", "artifact_kind": "code-and-test-change", "language": "python", "scope": "current-overload-classification", "phase": "post-edit", "state": "unvalidated", "optional": false}
  ],
  "outputs": [
    {"name": "overload-validation", "semantic_role": "overload-validation-results", "artifact_kind": "public-check-record", "language": "python", "scope": "current-overload-classification", "phase": "post-validation", "state": "outcomes-recorded", "optional": false}
  ],
  "preconditions": [
    {"key": "async-classification-extended", "value": true, "evaluator": "evidence"},
    {"key": "async-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-validation-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "async-target-behavior-correct", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-function-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-compatibility-preserved", "value": true, "evaluator": "evidence"},
    {"key": "downstream-semantics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "overload-target-and-controls",
      "instruction": "Require no unused-redefinition warnings for async and sync typing overload sequences and unchanged diagnostics for an ordinary non-overload redefinition control. Review unchanged decorator identity, downstream diagnostic rules and runtime guards. Record actual commands, outputs and PASS/FAIL/UNKNOWN; FAIL or unresolved UNKNOWN prevents acceptance.",
      "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "overload-suite",
      "instruction": "Run current affected overload/type-annotation tests including async and existing sync cases. Record test identities, results and exact scope; unavailable required checks remain UNKNOWN. Do not infer whole-project success.",
      "evidence_refs": ["PyCQA/pyflakes:470:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["local_template:verified-history:b8f8b3836dbeb26b4ee62590:overload-edit"],
  "read_set": ["role:overload-recognition", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/overload-validate.md",
  "package_id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590"
}
```
