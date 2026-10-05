# Inspect current receiver matching

Read the public reproduction and current checker. Identify the relevant class, private attribute name, write receiver, read receiver, matcher owner, and fixture owner. Record actual bindings and code hashes without tracked-file edits.

A confirmed output is conditional on observing the evidenced mechanism. An absent owner or different cause produces UNKNOWN or FAIL, not a fabricated confirmed PortValue.

```arex-contract-v4
{
  "id": "workflow:verified-history:8486fdf9c04144c10d14213f:inspect",
  "intent": "Determine whether the current false positive has the evidenced receiver-matching mechanism.",
  "mechanism": "Trace equal-name private writes and reads through cls/self and inspect receiver-name comparison.",
  "semantic_role": "mechanism-probe",
  "owner_role": "private-member-use-matcher",
  "operation": "Read public source and reproduction, resolve current semantic owners, and record evidence without modifying tracked files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "receiver-analysis", "semantic_role": "receiver-match-analysis", "artifact_kind": "evidence-record", "language": "Python", "scope": "current-private-member-checker", "phase": "inspection", "state": "confirmed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "receiver-mechanism-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unrelated-private-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-receiver-pair",
      "instruction": "Review the public cls-write/self-read reproduction and current comparison. Confirm equal private names, relevant same-class scope, located matcher and fixture owners, and receiver-name equality as the cause. Record FAIL or UNKNOWN if unsupported. Verify no tracked-file edits.",
      "evidence_refs": ["pylint-dev/pylint:4657:body", "pylint-dev/pylint:4657:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:private-member-use-matcher", "role:private-member-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4657:repair:c02682670e0d"],
  "evidence_refs": ["pylint-dev/pylint:4657:body", "pylint-dev/pylint:4657:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:8486fdf9c04144c10d14213f"
}
```
