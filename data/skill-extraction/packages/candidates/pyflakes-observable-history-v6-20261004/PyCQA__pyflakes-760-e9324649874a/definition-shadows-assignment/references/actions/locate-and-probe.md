# Locate owners and probe the missed diagnostic

Read the current public binding model and tests. Bind roles to actual objects and reproduce the asymmetric redefinition behavior. This Action does not modify code or tests.

Inspect how unused status and exemptions are handled separately from binding classification. Establish whether adding a definition-side assignment case is appropriate; do not infer compatibility solely from symbol names.

```arex-contract-v4
{
  "id": "workflow:verified-history:ee79eebf2283561900232caf:locate-and-probe",
  "intent": "Establish current applicability and locate semantic owners.",
  "mechanism": "Compare assignment-to-definition and definition-to-definition public diagnostic behavior, then inspect definition and assignment binding semantics.",
  "semantic_role": "binding-redefinition-applicability",
  "owner_role": "binding-redefinition-owner",
  "operation": "Read current public code and tests without editing them; record owner bindings, base anchors, diagnostic observations, and compatible policy.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "located-context",
      "semantic_role": "compatible-binding-redefinition-context",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "binding-owner-located", "value": true, "evaluator": "symbol_exists", "description": "Locate role:binding-redefinition-owner in the current checkout."},
    {"key": "assignment-owner-located", "value": true, "evaluator": "symbol_exists", "description": "Locate role:assignment-binding-owner in the current checkout."},
    {"key": "regression-owner-located", "value": true, "evaluator": "file_exists", "description": "Locate role:unused-redefinition-tests-owner in the current checkout."},
    {"key": "compatible-definition-assignment-policy", "value": true, "evaluator": "evidence", "description": "Current review and public probes establish the missing assignment-to-definition case and suitability of the existing diagnostic policy."}
  ],
  "preserves": [
    {"key": "superclass-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-assignment-rebinding-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "establish-current-applicability",
      "instruction": "Bind current public probes for a class assignment followed by a same-name method, two same-name definitions, and ordinary assignment rebinding; inspect the binding predicate and exemptions. Record results without modifying source or tests. Mark compatibility UNKNOWN or FAIL if evidence is insufficient or contradictory.",
      "evidence_refs": ["PyCQA/pyflakes:760:body", "PyCQA/pyflakes:760:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:760:repair:e9324649874a"],
  "evidence_refs": ["PyCQA/pyflakes:760:title", "PyCQA/pyflakes:760:body", "PyCQA/pyflakes:760:fix"],
  "read_set": ["role:binding-redefinition-owner", "role:assignment-binding-owner", "role:unused-redefinition-tests-owner"],
  "write_set": [],
  "resource": "references/actions/locate-and-probe.md",
  "package_id": "workflow:verified-history:ee79eebf2283561900232caf"
}
```

Predicate location descriptions identify current role objects, not historical file bindings. If an owner cannot be found, do not emit the established-context output. Empty command arrays require current oracle binding and are not executable commands.
