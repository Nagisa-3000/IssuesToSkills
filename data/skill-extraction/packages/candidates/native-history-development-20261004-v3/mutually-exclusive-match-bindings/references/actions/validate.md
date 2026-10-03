# Execute public validation

Run the added assertion and current adjacent match tests with bound public argv.
Check equivalent `if`/`else` behavior, existing `try` alternative classification,
and a genuine sequential unused-name redefinition. Review or test compatibility
against the supported runtime policy.

Record command, interpreter, exit status, diagnostic output, and per-check
PASS/FAIL/UNKNOWN. Missing checks cannot establish acceptance. These controls
are current preservation obligations, not claimed historical executions.
Changed-test-only qualification does not establish whole-project acceptance.

```arex-contract-v4
{
  "id": "mutually-exclusive-match-bindings:validate",
  "intent": "Observe repair and preservation after implementation and regression edits.",
  "mechanism": "Execute public tests and diagnostic controls and inspect runtime compatibility.",
  "semantic_role": "repair-validation",
  "owner_role": "python-analyzer-public-validation",
  "operation": "Run bound public checks and record actual results for both modifications.",
  "kind": "validate",
  "inputs": [
    {"name": "classifier-change", "semantic_role": "match-alternative-implementation", "artifact_kind": "source-change", "language": "python", "scope": "current-analyzer", "phase": "repair", "state": "modified-unvalidated", "optional": false},
    {"name": "regression-change", "semantic_role": "distinct-case-regression-implementation", "artifact_kind": "test-change", "language": "python", "scope": "current-analyzer", "phase": "repair", "state": "modified-unvalidated", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "observed-repair-validation", "artifact_kind": "test-and-probe-record", "language": "python", "scope": "current-analyzer", "phase": "verification", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "match-cases-recognized-as-alternatives", "value": true, "evaluator": "evidence"},
    {"key": "distinct-case-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-passed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-if-try-alternatives-preserved", "value": true, "evaluator": "evidence"},
    {"key": "sequential-redefinition-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "python-ast-availability-respected", "value": true, "evaluator": "evidence"},
    {"key": "checkout-unmodified-by-validation", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-match-regression",
      "instruction": "Execute the current public match suite including the added distinct-case assertion; record actual results and diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:771:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-adjacent-behavior",
      "instruction": "Run public if/else, try-alternative, and sequential-redefinition controls; establish supported-runtime ast.Match availability handling. Record evidence separately for every preservation claim.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": [
    "mutually-exclusive-match-bindings:recognize",
    "mutually-exclusive-match-bindings:regression"
  ],
  "source_ids": ["PyCQA/pyflakes:771"],
  "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"],
  "read_set": ["role:python-branch-alternative-classifier", "role:python-match-regression-suite", "role:python-analyzer-public-validation"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "mutually-exclusive-match-bindings"
}
```

Bind each current Oracle with semantic check key
`oracle:<action_id>:<source_oracle_id>`. Render its public argv before running.
Only actual PASS evidence establishes the intended validation effect.
