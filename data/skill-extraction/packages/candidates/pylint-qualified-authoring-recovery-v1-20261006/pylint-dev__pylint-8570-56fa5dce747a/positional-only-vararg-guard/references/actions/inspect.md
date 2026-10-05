# Inspect the diagnostic boundary

Locate the current semantic owners and inspect their actual argument-model meanings. Reproduce the public signature and mixed controls without modifying repository source. An unavailable behavioral probe is UNKNOWN, not inferred success.

```arex-contract-v4
{
  "id": "workflow:verified-history:0b7e98c0346a9448ab645489:inspect",
  "intent": "Establish whether the evidenced false-positive mechanism applies.",
  "mechanism": "Compare the argument partitions at the vararg/default diagnostic gate.",
  "semantic_role": "diagnostic-boundary-inspection",
  "owner_role": "signature-diagnostic-owner",
  "operation": "Read the current visitor and argument model, record hashed anchors, and probe the public reproduction and mixed controls without repository edits.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "boundary-analysis", "semantic_role": "signature-boundary-analysis", "artifact_kind": "review-record", "language": "python", "scope": "signature-diagnostic", "phase": "pre-edit", "state": "confirmed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "partition-mechanism-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "mixed-signature-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-diagnostic-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-partitions",
      "instruction": "Record owner anchors and confirmed positional-only versus positional-or-keyword meanings. Confirm the defaulted positional-only-only reproduction emits the target warning at the vararg/default gate; identify mixed controls. Verify the probe did not edit repository source.",
      "evidence_refs": ["pylint-dev/pylint:8570:body", "pylint-dev/pylint:8570:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:signature-diagnostic-owner", "role:argument-partition-model"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8570:repair:56fa5dce747a"],
  "evidence_refs": ["pylint-dev/pylint:8570:title", "pylint-dev/pylint:8570:body", "pylint-dev/pylint:8570:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:0b7e98c0346a9448ab645489"
}
```
