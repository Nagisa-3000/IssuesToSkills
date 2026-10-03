# Validate the guard and regression assertion

Bind the current public test runner and reproduction commands. No historical execution command was supplied, so the contract leaves commands empty until current binding.

Run the regression and relevant annotation tests. Review or probe the guard's two unaffected insertion cases and annotation-expression use handling. These adjacent checks are current validation requirements derived from the narrow mechanism, not additional historical test claims.

```arex-contract-v4
{
  "id": "workflow:verified-history:eedcc58f60ba24cb02758489:validate",
  "intent": "Observe the repaired reproduction and retained neighboring binding behavior.",
  "mechanism": "Run public regression tests and check both unaffected scope-update cases.",
  "semantic_role": "annotation-binding-validation",
  "owner_role": "public-annotation-test-runner",
  "operation": "Execute current-bound public reproduction and annotation tests; inspect or probe ordinary replacement, absent-name annotation insertion, and annotation-expression use handling; record outcomes and scope.",
  "kind": "validate",
  "inputs": [
    {"name": "guarded-updater", "semantic_role": "annotation-safe-binding-updater", "artifact_kind": "source-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "edited"},
    {"name": "regression-assertion", "semantic_role": "export-annotation-test", "artifact_kind": "test-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "edited"}
  ],
  "outputs": [
    {"name": "validation-observations", "semantic_role": "annotation-binding-validation-results", "artifact_kind": "test-report", "language": "Python", "scope": "current-checkout", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "annotation-replacement-guard-present", "value": true, "evaluator": "evidence"},
    {"key": "export-annotation-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-rebinding-preserved", "value": true, "evaluator": "evidence"},
    {"key": "absent-name-annotation-insertion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "annotation-expression-use-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "export-annotation-mre",
      "instruction": "Run the public conditional __all__ assignment/annotation reproduction through the current analyzer and require no diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:605:body", "PyCQA/pyflakes:605:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-tests",
      "instruction": "Run the current regression and relevant annotation tests. Separately review or probe absent-name annotation insertion, ordinary replacement, and annotation-expression import-use handling; record PASS, FAIL, or UNKNOWN and actual coverage.",
      "evidence_refs": ["PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:eedcc58f60ba24cb02758489:guard",
    "workflow:verified-history:eedcc58f60ba24cb02758489:regression"
  ],
  "source_ids": ["PyCQA/pyflakes:605:repair:43541ee1dd39"],
  "evidence_refs": ["PyCQA/pyflakes:605:fix", "PyCQA/pyflakes:605:regression"],
  "read_set": ["role:scope-binding-insertion-owner", "role:annotation-regression-test-owner", "role:public-annotation-test-runner"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:eedcc58f60ba24cb02758489"
}
```

For each current oracle, record its Action ID, source oracle ID, public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound command before execution.

An observed failure is not a satisfied validation effect. UNKNOWN cannot authorize a claim of success. Independent hidden acceptance, if required by the host, occurs after the solver stops and is not a source of guidance.
