# Validate scope classification

Run the bound public collision, regression, ordinary counterpart, and affected annotation tests. Review compatibility and unchanged downstream traversal. Record unavailable runtime checks as UNKNOWN unless adequate public evidence establishes the assurance.

Do not edit source or expectations. A validation record containing failures is not acceptance.

```arex-contract-v4
{
  "id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-validate",
  "intent": "Observe corrected async scope analysis and preserved neighboring behavior.",
  "mechanism": "Run public reproductions and annotation controls against the changed registration.",
  "semantic_role": "validate-target-and-preservation",
  "owner_role": "annotation-regression-tests",
  "operation": "Execute bound public target, ordinary counterpart, affected-suite and compatibility checks; record actual outcomes without source or expectation edits.",
  "kind": "validate",
  "inputs": [
    {"name": "scope-change", "semantic_role": "scope-validation-target", "artifact_kind": "code-and-test-change", "language": "python", "scope": "current-scope-classification", "phase": "post-edit", "state": "unvalidated", "optional": false}
  ],
  "outputs": [
    {"name": "scope-validation", "semantic_role": "scope-validation-results", "artifact_kind": "public-check-record", "language": "python", "scope": "current-scope-classification", "phase": "post-validation", "state": "outcomes-recorded", "optional": false}
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
      "id": "scope-target-and-controls",
      "instruction": "Analyze the annotated async class/parameter collision and ordinary counterpart. Require no Module.parent crash or unexpected diagnostics. Review unchanged parent traversal and current capability guards. Record actual commands, outputs and PASS/FAIL/UNKNOWN for target and preservation checks.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-suite",
      "instruction": "Run the current regression and affected annotation suite including diagnostic controls. Record test identities, outcomes, tested scope and unavailable checks. FAIL or unresolved UNKNOWN prevents acceptance; do not infer whole-project safety.",
      "evidence_refs": ["PyCQA/pyflakes:401:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["local_template:verified-history:b8f8b3836dbeb26b4ee62590:scope-edit"],
  "read_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
  "resource": "references/actions/scope-validate.md",
  "package_id": "local_template:verified-history:b8f8b3836dbeb26b4ee62590"
}
```
