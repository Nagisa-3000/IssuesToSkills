# Validate diagnostics and neighboring exemptions

Run current public checks after the edit. Use current fixture conventions and current oracle bindings; historical line numbers are not current command selectors.

The new assertions require protected-access diagnostics for both external accesses. Also check retained fixture expectations and legitimate instance/class/metaclass receiver behavior, missing-function and empty-argument paths, and relevant call expressions. These are current validation obligations, not claims that each was independently exercised by historical CI.

```arex-contract-v4
{
  "id": "workflow:verified-history:5eae2300be395ac5633f17e5:validate",
  "intent": "Observe the repaired public diagnostic boundary and detect adjacent regressions.",
  "mechanism": "Execute the updated protected-access fixture and public neighboring receiver/expression checks against the modified checkout.",
  "semantic_role": "validate-receiver-exemption-repair",
  "owner_role": "protected-access-fixtures",
  "operation": "Bind and render current public test commands. Run the updated fixture and compatible adjacent receiver and call-expression checks without editing tracked sources. Record exit status, actual diagnostic identities and locations, unchanged expectations, skips, and unresolved checks. Do not report completion while required checks remain unknown or fail.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-delta",
      "semantic_role": "receiver-exemption-repair",
      "artifact_kind": "source-and-test-diff",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "receiver-exemption-validation",
      "artifact_kind": "public-test-result",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "post-validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "external-protected-access-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:protected-access-fixtures", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "current-public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "current-diagnostic-observations-fresh", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "legitimate-bound-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-protected-access-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "call-expression-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-protected-access",
      "instruction": "Execute current public protected-access regression checks. Require the ordinary-function and static-method accesses to emit the expected protected-access diagnostics with no unexpected new diagnostics, and retain previous fixture expectations. Record failures rather than interpreting an unrelated successful test as completion.",
      "evidence_refs": ["pylint-dev/pylint:5989:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-adjacent-receiver-behavior",
      "instruction": "Run or construct current public checks for legitimate bound receivers, no nearest function, no positional arguments, and relevant call-expression handling. Compare against the pinned baseline and intended exemptions. Document skips and unknowns; required unknowns block completion.",
      "evidence_refs": ["pylint-dev/pylint:5989:fix", "pylint-dev/pylint:5989:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5989:repair:5c8384e811e3"],
  "evidence_refs": ["pylint-dev/pylint:5989:fix", "pylint-dev/pylint:5989:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:5eae2300be395ac5633f17e5",
  "read_set": ["role:receiver-classifier", "role:protected-access-checker", "role:protected-access-fixtures"],
  "write_set": [],
  "validation_for": ["workflow:verified-history:5eae2300be395ac5633f17e5:repair"]
}
```
