# Validate repaired and adjacent behavior

Bind commands to the current public harness and render them before execution. No historical command was supplied. Execute positive regressions and adjacent checks without editing implementation or assertions. Record actual results and coverage limits.

```arex-contract-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:validate",
  "intent": "Observe corrected overload recognition and retained adjacent diagnostic behavior.",
  "mechanism": "Execute public positive regressions and preservation probes against the edited code.",
  "semantic_role": "recognition-validation",
  "owner_role": "type-annotation-regression-suite",
  "operation": "Execute currently bound public tests and probes without editing code or assertions; record commands, outcomes, and unresolved checks. Establish successful effects only from observed passing checks.",
  "kind": "validate",
  "inputs": [
    {"name": "recognition-change", "semantic_role": "recognition-change-under-test", "artifact_kind": "code-and-test-diff", "language": "Python", "scope": "current-public-checkout", "phase": "post-edit", "state": "awaiting-validation", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "recognition-validation-results", "artifact_kind": "public-test-record", "language": "Python", "scope": "current-public-checkout", "phase": "post-validation", "state": "outcomes-recorded", "optional": false}
  ],
  "preconditions": [
    {"key": "recognition-repair-present", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "required-public-checks-pass", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "first-binding-shadowing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-qualified-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "function-node-restriction-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-overload-regressions",
      "instruction": "Run current public equivalents of the class-contained and multiple-decorator assertions and the surrounding annotation suite. Confirm valid overload sequences do not emit false unused-redefinition diagnostics. Record actual execution outcomes.",
      "evidence_refs": ["PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-preservation",
      "instruction": "Run public checks for ordinary redefinition diagnostics, a non-typing inner binding shadowing an outer typing.overload import, existing qualified recognition, and retained function-node restrictions. Compare with the recorded baseline. These are current obligations, not claims of historical execution.",
      "evidence_refs": ["PyCQA/pyflakes:434:fix", "PyCQA/pyflakes:434:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:fc3525ab47a41bc94f54d0d0:repair"],
  "read_set": ["role:overload-recognition-and-redefinition-gate", "role:scope-stack-and-import-bindings", "role:type-annotation-regression-suite"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs": ["PyCQA/pyflakes:434:fix", "PyCQA/pyflakes:434:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0"
}
```

An outcomes-recorded output may contain failures. Fresh observations do not imply success. `required-public-checks-pass` is established only when every required repair and preservation check actually passes; FAIL or UNKNOWN prevents acceptance.
