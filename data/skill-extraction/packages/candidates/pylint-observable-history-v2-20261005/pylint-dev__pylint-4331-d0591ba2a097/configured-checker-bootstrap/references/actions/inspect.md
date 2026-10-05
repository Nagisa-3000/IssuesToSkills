# Inspect the bootstrap lifecycle

Read current semantic owners and the public reproduction. Confirm module
importability, diagnostic enablement, and the actual parsing and application
sequence. Compare ordinary startup where available. Do not edit tracked files.
A failed or unknown diagnosis must not emit a confirmed diagnosis PortValue.

```arex-contract-v4
{
  "id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:inspect",
  "intent": "Distinguish missing configured-module registration from unrelated diagnostic failures.",
  "mechanism": "Inspect and probe the actual configuration-to-registration lifecycle.",
  "semantic_role": "bootstrap-diagnosis",
  "owner_role": "functional-harness-bootstrap",
  "operation": "Read current harness and public fixture configuration; probe importability and message enablement; record hashed anchors showing the lifecycle omission and compatible parser/loader semantics without modifying tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "diagnosis", "semantic_role": "bootstrap-diagnosis", "artifact_kind": "evidence-record", "language": "Python", "scope": "functional-harness", "phase": "diagnosis", "state": "confirmed"}
  ],
  "preconditions": [
    {"key": "role:functional-harness-bootstrap", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "bootstrap-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-parser-loader-compatible", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-harness-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-config-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "locate-gap",
      "instruction": "Record current anchors proving configuration is parsed and applied without registering its explicitly requested importable checker. Verify message enablement and parser/loader semantics. Confirm the probe changed no tracked source or fixture files.",
      "evidence_refs": ["pylint-dev/pylint:4331:body", "pylint-dev/pylint:4331:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4331:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4331:body", "pylint-dev/pylint:4331:fix"],
  "read_set": ["role:functional-harness-bootstrap", "role:plugin-functional-fixtures"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833"
}
```
