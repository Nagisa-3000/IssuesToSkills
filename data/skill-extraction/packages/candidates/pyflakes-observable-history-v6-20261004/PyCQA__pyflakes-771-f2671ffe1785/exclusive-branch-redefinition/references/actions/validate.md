# Validate the repair and adjacent behavior

Bind and execute current public checks after both edits. Preserve real redefinition detection rather than suppressing the diagnostic indiscriminately.

```arex-contract-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49:validate",
  "intent": "Observe whether the repair removes the false positive while retaining adjacent behavior.",
  "mechanism": "Execute the match regression and public controls, and review unchanged branch classification and runtime guarding.",
  "semantic_role": "repair-validation",
  "owner_role": "public-test-runner",
  "operation": "Bind current public commands; execute the new match regression, relevant adjacent suite, and public controls for existing branch alternatives and genuine sequential redefinitions. Review supported-runtime AST guarding and run available compatibility checks. Record commands, results, and unresolved coverage without changing tracked code.",
  "kind": "validate",
  "inputs": [
    {
      "name": "classifier",
      "semantic_role": "branch-alternative-classifier",
      "artifact_kind": "source-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified",
      "optional": false
    },
    {
      "name": "regression",
      "semantic_role": "match-exclusive-definition-regression",
      "artifact_kind": "test-code",
      "language": "python",
      "scope": "current-checkout",
      "phase": "repair",
      "state": "modified",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "branch-redefinition-validation",
      "artifact_kind": "test-results",
      "language": "python",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-runner-located", "value": true, "evaluator": "file_exists", "description": "Resolve role:public-test-runner in the current checkout."},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"},
    {"key": "match-case-alternatives-recognized", "value": true, "evaluator": "evidence"},
    {"key": "match-redefinition-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-if-try-classification-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-redefinition-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "match-regression",
      "instruction": "Run the bound public no-diagnostic match regression and relevant match suite. Require the reported false positive to be absent and record actual output.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-behavior",
      "instruction": "Run public controls for definitions in exclusive if branches and genuine sequential redefinitions; inspect existing if/try classifier semantics and the match runtime guard. Run available relevant compatibility checks. Record unsupported or unexecuted coverage as UNKNOWN rather than claiming preservation.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:45a56eede77a20492da56a49:classify",
    "workflow:verified-history:45a56eede77a20492da56a49:regression"
  ],
  "read_set": ["role:diagnostic-alternative-classifier", "role:match-regression-suite", "role:public-test-runner"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:45a56eede77a20492da56a49"
}
```

Empty command arrays are intentionally unbound. A current TaskContext must supply public argv commands; it must not target hidden acceptance tests. Validation observations, including failures, are distinct from a success claim. Any subsequent edit makes these observations stale.
