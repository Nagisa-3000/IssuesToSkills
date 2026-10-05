# Validate both modifications and adjacent behavior

Bind and render current public commands before execution. Run configured-plugin
fixtures and adjacent ordinary fixtures after relevant edits. Check exact
diagnostics and checker-specific option behavior. Review absent configuration
and missing-file handling; execute their public tests where available and
report unknown coverage explicitly.

An isolated unmodified-bootstrap control may establish that strengthened
assertions discriminate missing plugin activation rather than environment
failure. Do not damage the working checkout. This is current validation
guidance, not a claim that historical CI performed that control.

```arex-contract-v4
{
  "id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:validate",
  "intent": "Verify configured-plugin activation and preserved neighboring behavior.",
  "mechanism": "Execute public configured-plugin and adjacent tests and review initialization and error-handling preservation.",
  "semantic_role": "public-repair-validation",
  "owner_role": "functional-test-runner",
  "operation": "Execute rendered current public Oracle commands and record argv, exit statuses, diagnostics, skips, adjacent results, and preservation evidence without editing source or expectations. Mark success only when required checks pass.",
  "kind": "validate",
  "inputs": [
    {"name": "bootstrap", "semantic_role": "bootstrap-repair", "artifact_kind": "source-code", "language": "Python", "scope": "functional-harness", "phase": "repair", "state": "edited"},
    {"name": "assertions", "semantic_role": "plugin-regression-assertions", "artifact_kind": "functional-fixture-set", "language": "Python", "scope": "plugin-functional-tests", "phase": "repair", "state": "edited"}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "public-repair-validation", "artifact_kind": "test-observations", "language": "Python", "scope": "functional-tests", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "configured-registration-before-application", "value": true, "evaluator": "evidence"},
    {"key": "discriminating-plugin-assertions", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "public-checks-passed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-harness-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-config-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "plugin-diagnostics",
      "instruction": "Run current configured-plugin fixtures and require exact reviewed diagnostics and observable checker-specific configuration behavior. Distinguish diagnostic mismatches from import or runtime failures.",
      "evidence_refs": ["pylint-dev/pylint:4331:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-behavior",
      "instruction": "Run adjacent ordinary fixtures and available absent-config tests; review checker initialization, reporter setup, suppression settings, and missing-file handling. Record skips and unknown coverage without inferring whole-project correctness.",
      "evidence_refs": ["pylint-dev/pylint:4331:body", "pylint-dev/pylint:4331:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:a8b32e3610a8e5ec2b10b833:register",
    "workflow:verified-history:a8b32e3610a8e5ec2b10b833:fixtures"
  ],
  "source_ids": ["pylint-dev/pylint:4331:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4331:fix", "pylint-dev/pylint:4331:regression"],
  "read_set": ["role:functional-harness-bootstrap", "role:plugin-functional-fixtures", "role:functional-test-runner"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833"
}
```

A failed run still produces an observation record, but cannot establish
`public-checks-passed`. Empty command arrays require current public bindings;
historical replay commands do not authorize current execution.
