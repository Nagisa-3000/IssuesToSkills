# Diagnose the receiver mismatch

Read the current checker and fixture conventions. Confirm the assignment scope, simple returned receiver name, same-name private read through `self`, and unwanted public diagnostic. Record actual role bindings and hashes; do not reuse historical paths as current bindings. This probe does not edit source or fixtures.

```arex-contract-v4
{
  "id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:locate",
  "intent": "Determine whether the current issue fits the constructor-local receiver mismatch.",
  "mechanism": "Compare assignment receiver, constructor return names, consumer receiver, and current matching rules.",
  "semantic_role": "diagnose-returned-instance-usage",
  "owner_role": "private-member-checker",
  "operation": "Read current public checker and fixture owners, execute a bound public reproduction, and record anchors and semantic facts without changing file contents.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "diagnosis", "semantic_role": "returned-instance-diagnosis", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "returned-instance-mismatch-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "non-name-return-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-public-mismatch",
      "instruction": "Capture the unwanted diagnostic and public anchors establishing assignment scope, simple return name, and self consumption. Confirm no source or fixture content changed during the probe.",
      "evidence_refs": ["pylint-dev/pylint:4668:body", "pylint-dev/pylint:4668:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4668:repair:f6c813824183"],
  "evidence_refs": ["pylint-dev/pylint:4668:body", "pylint-dev/pylint:4668:fix"],
  "resource": "references/actions/locate.md",
  "package_id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2",
  "read_set": ["role:private-member-checker", "role:private-member-regressions", "role:public-test-runner"],
  "write_set": []
}
```

A confirmed output is conditional on actual observations. If already fixed, record that and stop unnecessary editing. Missing identity or runner evidence remains UNKNOWN.
