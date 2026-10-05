# Inspect applicability

Locate current owners and trace the public reproduction to the shared condition. Inspect reachable node kinds, their identifier fields, inferred-object equality, receiver safety, and fixture format. Use read-only inspection or isolated reproduction without changing tracked checkout files.

Successful effects require current evidence. Incompatible findings produce FAIL; unresolved findings remain UNKNOWN.

```arex-contract-v4
{
  "id": "workflow:verified-history:bc4129e7b226dfae4c87ca01:inspect",
  "intent": "Establish the supported iterable-side Name/Attribute mismatch and current bindings.",
  "mechanism": "Trace the reproduction and inspect the actual node interfaces and existing condition.",
  "semantic_role": "applicability-probe",
  "owner_role": "iteration-condition-owner",
  "operation": "Read current condition, AST APIs, and fixtures; reproduce in isolation; record hashed anchors and owner bindings without changing tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [],
  "preconditions": [],
  "effects": [
    {"key": "current-owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "supported-node-shapes-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "receiver-name-contract-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "fixture-expectation-format-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "inference-equality-guard-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-iteration-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "separate-copy-not-diagnosed-as-iterated-set", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-current-node-contract",
      "instruction": "Record hashed current anchors and iterable kind. Verify Name.name, Attribute.attrname, reachable shapes, inference equality, receiver safety, fixture format, and condition/API/fixture/runner bindings. Report FAIL or UNKNOWN for unmet requirements and confirm tracked files are unchanged.",
      "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:fix", "pylint-dev/pylint:7528:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:iteration-condition-owner", "role:ast-node-api-owner", "role:iteration-regression-owner", "role:iteration-test-runner-owner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:7528:repair:aca8dd546e6e"],
  "evidence_refs": ["pylint-dev/pylint:7528:body", "pylint-dev/pylint:7528:fix", "pylint-dev/pylint:7528:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:bc4129e7b226dfae4c87ca01"
}
```
