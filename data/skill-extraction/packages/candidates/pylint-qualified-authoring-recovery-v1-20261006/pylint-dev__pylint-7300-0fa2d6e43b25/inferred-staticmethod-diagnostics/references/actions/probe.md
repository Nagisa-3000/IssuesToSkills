# Probe the diagnostic boundary

Locate current semantic owners and review inference without changing tracked code. Use isolated public reproductions where necessary. Record current anchors, inferred identities, unwanted diagnostics, and baseline controls. Do not equate a decorator's name with its semantics.

```arex-contract-v4
{
  "id": "workflow:verified-history:d64e04a769c8484780ab2708:probe",
  "intent": "Determine whether this local exemption applies.",
  "mechanism": "Compare inferred decorator qualified identity with the receiver-check branch that emits the false diagnostic.",
  "semantic_role": "diagnostic-boundary-probe",
  "owner_role": "method-argument-checker",
  "operation": "Read the current method-argument checker and decorator identity provider; run bound public reproductions in an isolated fixture; record anchors and baseline behavior without editing tracked code.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "bound-diagnostic-context",
      "semantic_role": "static-method-diagnostic-context",
      "artifact_kind": "public-code-and-observation-record",
      "language": "python",
      "scope": "method-argument-checking",
      "phase": "pre-repair",
      "state": "identity-and-boundary-established"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "checker-owner-located", "value": true, "evaluator": "symbol_exists", "description": "Resolve role:method-argument-checker in the current checkout."},
    {"key": "inferred-staticmethod-identity-established", "value": true, "evaluator": "evidence"},
    {"key": "target-false-diagnostic-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-method-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "direct-staticmethod-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-method-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "establish-current-boundary",
      "instruction": "In the bound public checkout, inspect the checker and inference result for aliased staticmethod; reproduce the unwanted diagnostic and record ordinary-method and direct-staticmethod baseline controls. Confirm no tracked-code modifications.",
      "evidence_refs": ["pylint-dev/pylint:7300:body", "pylint-dev/pylint:7300:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:method-argument-checker", "role:decorator-identity-provider", "role:method-argument-regressions"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:7300:repair:0fa2d6e43b25"],
  "evidence_refs": ["pylint-dev/pylint:7300:body", "pylint-dev/pylint:7300:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:d64e04a769c8484780ab2708"
}
```

The `symbol_exists` observation must resolve the owner role to an actual current symbol, not a historical path. Missing identity evidence leaves applicability unknown.
