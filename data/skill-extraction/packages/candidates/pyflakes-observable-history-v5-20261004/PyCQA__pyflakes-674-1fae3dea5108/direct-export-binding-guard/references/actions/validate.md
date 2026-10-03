# Validate candidate dispatch and regression

Bind commands to the current public checkout. Execute the unpacking regression and adjacent export tests. Inspect coverage of the supported direct assignment forms, rather than assuming every branch is covered by the supplied historical test.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate",
  "intent": "Observe the corrected indirect-target behavior and preservation of direct export processing.",
  "mechanism": "Run public reproductions and diagnostic tests against both candidate edits.",
  "semantic_role": "export-binding-validation",
  "owner_role": "python-export-diagnostic-tests",
  "operation": "Execute the public unpacking regression, compare the reported crash reproduction, and run adjacent direct-export checks using current bound commands.",
  "kind": "validate",
  "inputs": [
    {"name": "guarded-implementation", "semantic_role": "export-dispatch-implementation", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "candidate", "state": "modified"},
    {"name": "regression-tests", "semantic_role": "export-diagnostic-regressions", "artifact_kind": "tests", "language": "python", "scope": "current-checkout", "phase": "candidate", "state": "modified"}
  ],
  "outputs": [
    {"name": "validation-observations", "semantic_role": "export-binding-validation-results", "artifact_kind": "test-results", "language": "python", "scope": "current-checkout", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "candidate-validation-recorded", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "candidate-source-and-tests", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "unpacking-diagnostic",
      "instruction": "Run the new public regression: analysis completes without an internal exception and reports the unused import.",
      "evidence_refs": ["PyCQA/pyflakes:674:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "reported-crash",
      "instruction": "Analyze the original comma-target reproduction with the current analyzer and confirm absence of the reported Tuple.value internal error; do not require a new invalid-assignment diagnostic.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-direct-exports",
      "instruction": "Run adjacent export/import diagnostics and publicly check supported direct assignment forms, including legitimate export warning suppression. Record missing coverage as UNKNOWN rather than claiming preservation.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d",
  "validation_for": [
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression"
  ],
  "read_set": ["role:python-binding-dispatch", "role:python-export-diagnostic-tests"],
  "write_set": []
}
```

An observed validation record can contain failures. Only actual passing checks support acceptance; this contract does not predict a successful run.
