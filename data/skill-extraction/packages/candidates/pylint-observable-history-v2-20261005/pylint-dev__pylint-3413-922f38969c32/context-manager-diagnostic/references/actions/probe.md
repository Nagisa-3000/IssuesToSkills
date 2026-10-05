# Probe current owners and inference boundaries

Read the current public checkout without changing tracked code. Resolve semantic owners, inspect message gates and visitor aliases, and observe inferred callable identities. Surface aliases are not sufficient evidence of classification membership.

This probe is a current-use prerequisite derived from the historical mechanism, not a claimed historical execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:a2197ca95e3d5f6edcfac42f:probe",
  "intent": "Establish compatible current bindings and inference boundaries.",
  "mechanism": "Inspect Python AST visitor ownership, message registration, and safely inferred callable identities for public allocation, acquisition, and direct-with examples.",
  "semantic_role": "diagnostic-boundary-discovery",
  "owner_role": "python-refactoring-checker",
  "operation": "Locate current checker, fixture, and integration owners; read their interfaces; record inferred names, visitor aliases, message gates, public reproductions, and interpreter limitations. Do not edit tracked code.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "reviewed-bindings",
      "semantic_role": "diagnostic-boundary-record",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "pre-edit",
      "state": "reviewed"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "owners-and-boundaries-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "resource-lifetime-semantics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-inference-boundaries",
      "instruction": "Record current public owner bindings, hashed anchors, inferred names and inference failures, registry and visitor interfaces, and direct-with routes. Compare tracked source hashes before and after the read-only probe.",
      "evidence_refs": ["pylint-dev/pylint:3413:fix", "pylint-dev/pylint:3413:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:python-refactoring-checker", "role:python-functional-fixtures", "role:diagnostic-consumers-and-docs"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:3413:repair:922f38969c32"],
  "evidence_refs": ["pylint-dev/pylint:3413:body", "pylint-dev/pylint:3413:fix", "pylint-dev/pylint:3413:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:a2197ca95e3d5f6edcfac42f"
}
```

A reviewed record must distinguish established compatibility from unknown or failed checks. Producing a record with unknown interfaces does not authorize implementation.
