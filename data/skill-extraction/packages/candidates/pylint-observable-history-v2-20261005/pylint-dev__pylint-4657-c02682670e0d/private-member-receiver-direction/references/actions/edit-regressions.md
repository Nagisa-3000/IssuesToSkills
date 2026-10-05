# Add directional boundary assertions

Use current public fixture conventions. Add the reported classmethod mutation/property read without an unused-private-member expectation. Add the inverse-direction case with an instance private write and only a `cls` read, retaining the unused-private-member expectation. If `cls` is unbound, retain undefined-variable as in the historical fixture.

Preserve existing expectations. Historical `HIGH` confidence annotations are facts about that fixture format, not instructions to rewrite a current format. Direct same-receiver controls may be added where coverage is missing; that is current validation planning, not additional historical evidence.

```arex-contract-v4
{
  "id": "workflow:verified-history:8486fdf9c04144c10d14213f:edit-regressions",
  "intent": "Encode the positive repair and inverse-direction negative boundary.",
  "mechanism": "Pair a cls-write/self-read no-warning assertion with a self-write/cls-read retained-warning assertion.",
  "semantic_role": "regression-authoring",
  "owner_role": "private-member-regression-suite",
  "operation": "Edit public fixtures and expected diagnostics using current harness conventions while preserving established expectations.",
  "kind": "edit",
  "inputs": [
    {"name": "receiver-analysis", "semantic_role": "receiver-match-analysis", "artifact_kind": "evidence-record", "language": "Python", "scope": "current-private-member-checker", "phase": "inspection", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "regression-change", "semantic_role": "directional-private-member-regressions", "artifact_kind": "test-change", "language": "Python", "scope": "current-private-member-checker", "phase": "repair", "state": "edited"}
  ],
  "preconditions": [
    {"key": "role:private-member-regression-suite", "value": true, "evaluator": "file_exists"},
    {"key": "receiver-mechanism-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "directional-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "instance-write-not-used-by-class-read", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-private-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-boundary-assertions",
      "instruction": "Review assertions for no unused warning on cls-write/self-read, an unused warning on self-write with only cls-read, undefined-variable for unbound cls, and retained preexisting diagnostic expectations.",
      "evidence_refs": ["pylint-dev/pylint:4657:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:private-member-regression-suite"],
  "write_set": ["role:private-member-regression-suite"],
  "source_ids": ["pylint-dev/pylint:4657:repair:c02682670e0d"],
  "evidence_refs": ["pylint-dev/pylint:4657:body", "pylint-dev/pylint:4657:regression"],
  "resource": "references/actions/edit-regressions.md",
  "package_id": "workflow:verified-history:8486fdf9c04144c10d14213f"
}
```
