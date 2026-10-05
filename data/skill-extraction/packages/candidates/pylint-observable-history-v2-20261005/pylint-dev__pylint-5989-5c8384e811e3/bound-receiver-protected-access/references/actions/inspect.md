# Inspect receiver-exemption semantics

Read the current implementation and run public reproductions without editing tracked sources. Record real semantic-owner bindings, code hashes, diagnostic settings, and the distinction between ordinary functions, static methods, and bound methods.

The historical report supplies the suspected mechanism, not proof that a new checkout has it. A diagnostic missing for another reason is not sufficient applicability evidence.

```arex-contract-v4
{
  "id": "workflow:verified-history:5eae2300be395ac5633f17e5:inspect",
  "intent": "Determine whether an unbound first parameter is incorrectly treated as an implicit receiver.",
  "mechanism": "Trace protected-access suppression through receiver classification and compare bound and unbound function contexts.",
  "semantic_role": "establish-receiver-exemption-mechanism",
  "owner_role": "receiver-classifier",
  "operation": "Locate current receiver-classifier, protected-access-checker, and protected-access-fixtures owners. Read without changing tracked sources. Probe ordinary-function and static-method accesses; inspect boundness, nearest-function, receiver-stack, no-argument, and call-expression branches. Record compatible bindings or a rejection.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "mechanism-review",
      "semantic_role": "receiver-exemption-applicability",
      "artifact_kind": "review-record",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-checkout-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "receiver-exemption-mechanism-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "legitimate-bound-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-protected-access-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "call-expression-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-suppression",
      "instruction": "Bind a current public reproduction and trace its suppression path. Confirm whether ordinary-function and static-method first arguments reach an implicit-receiver exemption without a boundness check; inspect adjacent bound-method and call-expression behavior. The read/probe must not edit tracked sources. Emit mechanism-confirmed output only after positive current evidence.",
      "evidence_refs": ["pylint-dev/pylint:5989:body", "pylint-dev/pylint:5989:fix", "pylint-dev/pylint:5989:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:5989:repair:5c8384e811e3"],
  "evidence_refs": ["pylint-dev/pylint:5989:body", "pylint-dev/pylint:5989:fix", "pylint-dev/pylint:5989:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:5eae2300be395ac5633f17e5",
  "read_set": ["role:receiver-classifier", "role:protected-access-checker", "role:protected-access-fixtures"],
  "write_set": [],
  "exclusions": [
    {"key": "missing-diagnostic-caused-only-by-disabled-rule", "value": true, "evaluator": "evidence"},
    {"key": "receiver-model-incompatible", "value": true, "evaluator": "evidence"}
  ]
}
```
