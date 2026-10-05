# Repair the narrow guard and parameter fallback

Proceed only on a confirmed semantic match. Existence predicates use role keys and boolean values; existence does not itself prove semantic compatibility.

After matching assigned and read attribute names, but before name-based receiver access, continue the read loop when the existing narrow type-call recognizer accepts the receiver. Do not skip the entire checker or all calls.

Retain registered first-parameter lookup. When tracking is empty, obtain the nearest function ancestor. Return false if no function or positional argument exists; otherwise compare only a name node with that function's first positional argument name. Keep appropriate node/boolean signatures without inventing recognizer conditions.

Add the classmethod assignment and `type(self)` read regression to the bound fixture and retain its unused-private-member expectation. Review for unrelated edits. This edit invalidates validation freshness, not required behavior assurances.

```arex-contract-v4
{
  "id": "workflow:verified-history:c0bacc1cf00a988417910aa7:repair",
  "intent": "Repair the recognized receiver crash while retaining the diagnostic policy.",
  "mechanism": "Guard a narrow type-call before name access and recover parameter identity from function ancestry when traversal tracking is empty.",
  "semantic_role": "receiver-and-lifecycle-repair",
  "owner_role": "private-member-checker",
  "operation": "Modify the bound checker and parameter helper and add the public regression with its retained diagnostic expectation.",
  "kind": "edit",
  "inputs": [
    {
      "name": "reviewed-owners",
      "semantic_role": "deferred-private-member-repair-context",
      "artifact_kind": "binding-and-observation-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
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
  "preconditions": [
    {"key": "receiver-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:private-member-checker", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:mandatory-parameter-helper", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:type-call-recognizer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:private-member-regression", "value": true, "evaluator": "file_exists"},
    {"key": "role:private-member-expectations", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "recognized-call-name-access-avoided", "value": true, "evaluator": "evidence"},
    {"key": "deferred-parameter-identity-recoverable", "value": true, "evaluator": "evidence"},
    {"key": "regression-diagnostic-retained", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "narrow-receiver-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-narrow-repair",
      "instruction": "Review the diff for a recognized-call guard before name access, preserved live-state lookup, guarded ancestor fallback and retained assignment diagnostic. Reject blanket call suppression and unrelated edits. Runtime validation remains mandatory.",
      "evidence_refs": ["pylint-dev/pylint:5569:fix", "pylint-dev/pylint:5569:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5569:repair:642268f63624"],
  "evidence_refs": ["pylint-dev/pylint:5569:fix", "pylint-dev/pylint:5569:regression"],
  "read_set": ["role:type-call-recognizer", "role:private-member-checker", "role:mandatory-parameter-helper", "role:private-member-regression", "role:private-member-expectations"],
  "write_set": ["role:private-member-checker", "role:mandatory-parameter-helper", "role:private-member-regression", "role:private-member-expectations"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:c0bacc1cf00a988417910aa7"
}
```
