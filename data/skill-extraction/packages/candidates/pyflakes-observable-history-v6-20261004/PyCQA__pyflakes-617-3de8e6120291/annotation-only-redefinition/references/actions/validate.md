# Validate the repair and regression

Bind public current commands after discovering the checkout's runner. Empty historical command arrays are not executable instructions. Run the targeted regression and relevant annotation suite; inspect and, where public tests permit, exercise ordinary redefinition behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:validate",
  "intent": "Observe whether the candidate repair satisfies the public regression without changing ordinary definition behavior.",
  "mechanism": "Execute public annotation tests and review the ordinary-definition boundary.",
  "semantic_role": "annotation-redefinition-validation",
  "owner_role": "annotation-test-owner",
  "operation": "Execute current bound public tests and reproduction, inspect the diff boundary, and record results and tested scope without modifying source files.",
  "kind": "validate",
  "inputs": [
    {"name": "implementation", "semantic_role": "annotation-only-redefinition-implementation", "artifact_kind": "source-code", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "candidate", "optional": false},
    {"name": "regression", "semantic_role": "import-annotation-use-regression", "artifact_kind": "test-code", "language": "python", "scope": "current-checkout", "phase": "verification", "state": "ready", "optional": false}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "annotation-redefinition-validation-results", "artifact_kind": "test-result-record", "language": "python", "scope": "current-checkout", "phase": "verification", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "import-annotation-use-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": "PASS", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-definition-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-annotation-regression",
      "instruction": "Run the public import/annotation/use regression and relevant annotation suite using the current harness. Record actual outputs, failures, skips, and scope; require no false redefinition diagnostic.",
      "evidence_refs": ["PyCQA/pyflakes:617:regression", "PyCQA/pyflakes:617:body"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-ordinary-definition-boundary",
      "instruction": "Review the current diff and use available public checks to confirm ordinary value-bearing definitions retain their existing redefinition behavior. Record UNKNOWN if this assurance cannot be established.",
      "evidence_refs": ["PyCQA/pyflakes:617:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:edit",
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:regression"
  ],
  "read_set": ["role:annotation-binding-owner", "role:redefinition-predicate-owner", "role:annotation-test-owner"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7"
}
```

PASS is an expected effect conditional on actual successful checks, not an observed result of authoring this package. Broader validation is current-task work, not verified historical knowledge.
