# Validate target and preserved behavior

Bind current public commands and run the method-call contrasts plus existing function-call return-consistency cases. Record the tested revision, command, exit status, and actual diagnostics. Validation does not alter tracked source or expected diagnostics.

```arex-contract-v4
{
  "id": "workflow:verified-history:1ae2f8b80e4aba1ad79b8e22:validate",
  "intent": "Observe whether the repair fixes the target without weakening adjacent return analysis.",
  "mechanism": "Compare diagnostic outcomes across truthful NoReturn, ordinary return type, incorrect NoReturn, and existing function-call cases.",
  "semantic_role": "return-consistency-public-validation",
  "owner_role": "return-consistency-regression-suite",
  "operation": "Execute explicitly bound public validation on the edited checkout and record outcomes without modifying tracked code or expectations.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate-repair",
      "semantic_role": "bound-method-noreturn-change",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "return-consistency-analysis",
      "phase": "repair",
      "state": "edited-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "return-consistency-check-outcomes",
      "artifact_kind": "test-record",
      "language": "python",
      "scope": "return-consistency-analysis",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "method-regression-contrast-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-returning-method-warning-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-function-annotation-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "annotation-trust-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "check-method-contrast",
      "instruction": "Execute the current public method-call contrasts. Require no return-consistency warning for either NoReturn-annotated caller, and retain the warning for the ordinary-returning caller.",
      "evidence_refs": ["pylint-dev/pylint:8747:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "check-adjacent-return-analysis",
      "instruction": "Run current public existing function-call and adjacent return-consistency cases against their expected diagnostics. Review that existing annotation-recognition branches remain unchanged.",
      "evidence_refs": ["pylint-dev/pylint:8747:fix", "pylint-dev/pylint:8747:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:1ae2f8b80e4aba1ad79b8e22:repair"],
  "read_set": ["role:return-termination-recognizer", "role:return-consistency-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8747:repair:8614ccf21aa7"],
  "evidence_refs": ["pylint-dev/pylint:8747:fix", "pylint-dev/pylint:8747:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:1ae2f8b80e4aba1ad79b8e22"
}
```

Empty source-command arrays are unbound placeholders, not runnable commands. Missing execution is UNKNOWN. Recorded execution is not automatically PASS: failures block acceptance. Any subsequent edit makes `public-validation-observed` stale without removing the preservation obligations.
