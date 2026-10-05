# Validate diagnostic boundaries

Bind and render current public runner commands. Execute without expected-output update mode. Require silent allocation and acquisition in `__enter__` and supported decorated generators, including qualified and imported decorator forms. Ordinary function/module allocation and ordinary acquisition must retain advice; existing `with` must remain silent.

Review inference filters and run adjacent public checker tests. Verify safe module-frame rejection. If nested-function behavior matters, probe its immediate frame directly. Uninferable calls remain unverified.

```arex-contract-v4
{
  "id": "workflow:verified-history:b74613551e6d8c24ed7692fa:validate",
  "intent": "Observe corrected diagnostics and preserved adjacent behavior.",
  "mechanism": "Execute public regression assertions and frame-boundary probes against the edited checker.",
  "semantic_role": "public-diagnostic-validation",
  "owner_role": "diagnostic-regression-suite",
  "operation": "Execute current bound public tests without rewriting assertions; capture exit status, diagnostics, locations, and unknown results.",
  "kind": "validate",
  "inputs": [
    {"name": "managed-frame-patch", "semantic_role": "managed-frame-patch", "artifact_kind": "code-and-test-diff", "language": "Python", "scope": "resource-advice-checker", "phase": "post-edit", "state": "modified", "optional": false}
  ],
  "outputs": [
    {"name": "validation-report", "semantic_role": "public-diagnostic-validation", "artifact_kind": "test-observation-report", "language": "Python", "scope": "resource-advice-checker", "phase": "post-validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "public-regression-assertions-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-resource-advice-preserved", "value": true, "evaluator": "evidence"},
    {"key": "resource-inference-filter-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-with-silence-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-resource-advice-regressions",
      "instruction": "Run current public allocation/acquisition regressions and adjacent checker tests. Require managed silence, ordinary advice, existing with silence, safe module-frame rejection, and no unexpected diagnostics. Record inference-unavailable cases as unverified.",
      "evidence_refs": ["pylint-dev/pylint:4430:regression", "pylint-dev/pylint:4430:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:b74613551e6d8c24ed7692fa:edit"],
  "source_ids": ["pylint-dev/pylint:4430:repair:f9df028c23ec"],
  "evidence_refs": ["pylint-dev/pylint:4430:regression", "pylint-dev/pylint:4430:fix"],
  "read_set": ["role:resource-advice-emitter", "role:diagnostic-regression-suite"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:b74613551e6d8c24ed7692fa"
}
```

This operation does not modify source or fixtures. Its contract is not an execution result. A FAIL or UNKNOWN required check leaves repair success unverified.
