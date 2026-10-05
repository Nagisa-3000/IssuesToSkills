# Validate the repair and adjacent behavior

Bind current public commands for the reproduction and relevant repository tests. Inspect diagnostics rather than exit status alone: normal lint warnings may produce nonzero exits.

Run the regression and neighboring private-member fixtures. Review or publicly probe live state, empty-state fallback, missing function ancestry, missing positional arguments and non-name nodes. Check ordinary names and nonmatching calls for unchanged policy.

Do not edit tracked source or expectations. Record current code hashes, Oracle bindings and outcomes. Infrastructure failures are UNKNOWN. Historical qualification is not execution of this Action.

```arex-contract-v4
{
  "id": "workflow:verified-history:c0bacc1cf00a988417910aa7:validate",
  "intent": "Observe no crash, the retained diagnostic and preserved adjacent behavior.",
  "mechanism": "Run the public reproduction and diagnostic-aware regression checks with parameter-lifecycle boundary review.",
  "semantic_role": "repair-validation",
  "owner_role": "private-member-regression",
  "operation": "Execute bound public checks and compare diagnostics and helper boundaries without editing tracked files.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "deferred-private-member-repair-candidate",
      "artifact_kind": "source-and-regression-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "deferred-private-member-validation",
      "artifact_kind": "public-check-results",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "recognized-call-name-access-avoided", "value": true, "evaluator": "evidence"},
    {"key": "deferred-parameter-identity-recoverable", "value": true, "evaluator": "evidence"},
    {"key": "regression-diagnostic-retained", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "narrow-receiver-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "public-receiver-reproduction",
      "instruction": "Run the bound public reproduction and inspect output for absence of the receiver AttributeError and fatal diagnostic. Distinguish ordinary warning exit status from a crash.",
      "evidence_refs": ["pylint-dev/pylint:5569:body"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "private-member-regression",
      "instruction": "Execute the regression and adjacent fixtures. Verify the assignment retains its expected unused-private-member diagnostic and neighboring expectations match.",
      "evidence_refs": ["pylint-dev/pylint:5569:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "parameter-lifecycle-boundaries",
      "instruction": "Inspect or publicly probe live-state lookup, empty-state nearest-function fallback, missing function, missing positional arguments and non-name nodes. Confirm false for unusable contexts and unchanged handling of nonmatching receivers.",
      "evidence_refs": ["pylint-dev/pylint:5569:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:c0bacc1cf00a988417910aa7:repair"],
  "source_ids": ["pylint-dev/pylint:5569:repair:642268f63624"],
  "evidence_refs": ["pylint-dev/pylint:5569:body", "pylint-dev/pylint:5569:fix", "pylint-dev/pylint:5569:regression"],
  "read_set": ["role:private-member-checker", "role:type-call-recognizer", "role:mandatory-parameter-helper", "role:private-member-regression", "role:private-member-expectations"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:c0bacc1cf00a988417910aa7"
}
```
