# Probe advisory disable bookkeeping

Locate the current owners and trace a public configuration containing an unresolved numeric identifier followed by a valid disable. Inspect whether failure occurs in advisory ID-to-symbol tracking rather than required configuration validation. Do not edit the checkout.

Record anchored findings, identifier resolution, configuration loading, and the public diagnostic observation. A symptom-only report leaves applicability UNKNOWN.

```arex-contract-v4
{
  "id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b:probe",
  "intent": "Establish the narrow missing-lookup mechanism and current semantic owners.",
  "mechanism": "Trace numeric-ID advisory registration and configuration continuation.",
  "semantic_role": "mechanism-probe",
  "owner_role": "disable-bookkeeping",
  "operation": "Read current code and run a bound public reproduction without modifying tracked files; identify registry lookup, exception boundary, and later disable.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "mechanism-evidence",
      "semantic_role": "advisory-disable-mechanism",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "mechanism-classified", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "known-numeric-registration-preserved", "value": true, "evaluator": "evidence"},
    {"key": "symbolic-disable-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-errors-not-suppressed", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "locate-and-reproduce",
      "instruction": "Record anchored owner bindings and demonstrate whether an unresolved numeric advisory lookup raises KeyError and prevents a later valid disable. Confirm configuration loading and required unknown-ID policy. Verify this probe makes no tracked-file changes.",
      "evidence_refs": ["pylint-dev/pylint:4265:body", "pylint-dev/pylint:4265:fix", "pylint-dev/pylint:4265:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:disable-bookkeeping", "role:message-registry", "role:configuration-regression"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4265:repair:c92e3ab78778"],
  "evidence_refs": ["pylint-dev/pylint:4265:body", "pylint-dev/pylint:4265:fix", "pylint-dev/pylint:4265:regression"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:ef9c08f5cc5fb6362cf0902b"
}
```
