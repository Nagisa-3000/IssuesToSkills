# Probe receiver shape and deferred state

Locate the current private-member checker, type-call recognizer, mandatory-parameter helper, regression fixture and expectation owners. Inspect the complete recognizer and review class-exit timing and parameter-stack lifetime. Reproduce the public failure using bound commands; record actual bindings and code hashes.

Do not modify tracked source or expectations. If the mechanism is absent or uncertain, record FAIL or UNKNOWN rather than manufacturing a confirmed output.

```arex-contract-v4
{
  "id": "workflow:verified-history:c0bacc1cf00a988417910aa7:probe",
  "intent": "Establish whether the current failure matches the deferred receiver mechanism.",
  "mechanism": "Inspect AST receiver shape, unsafe name access and parameter-state lifecycle.",
  "semantic_role": "mechanism-probe",
  "owner_role": "private-member-checker",
  "operation": "Read current semantic owners and run a bound public reproduction; record bindings and observations without editing tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
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
  "preconditions": [],
  "effects": [
    {"key": "receiver-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:private-member-checker", "value": true, "evaluator": "symbol_exists"}
  ],
  "preserves": [
    {"key": "adjacent-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "narrow-receiver-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-deferred-receiver",
      "instruction": "Observe the call receiver at unsafe name access; inspect complete recognizer conditions and why parameter tracking may be empty during class analysis. Record current bindings and code hashes and verify tracked source and expectations remain unchanged.",
      "evidence_refs": ["pylint-dev/pylint:5569:body", "pylint-dev/pylint:5569:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5569:repair:642268f63624"],
  "evidence_refs": ["pylint-dev/pylint:5569:body", "pylint-dev/pylint:5569:fix"],
  "read_set": ["role:private-member-checker", "role:type-call-recognizer", "role:mandatory-parameter-helper", "role:private-member-regression", "role:private-member-expectations"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:c0bacc1cf00a988417910aa7"
}
```
