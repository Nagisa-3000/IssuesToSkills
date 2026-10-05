# Add constructor-return assertions

Use the current public fixture owner's expectation conventions. Add two branches returning differently named local objects. Both initialize a private attribute read through `self`; one initializes an additional private member also read through `self`.

Include a non-name return value. Historically this was unreachable `return 3+4`, with unrelated protected-access, no-member, and unreachable diagnostics disabled locally. Do not disable unused-private-member globally. Retain existing positive unused-member expectations.

```arex-contract-v4
{
  "id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2:regressions",
  "intent": "Make multiple returned names and non-name return safety observable in public fixtures.",
  "mechanism": "Specify branch-specific constructor assignments consumed through self and a non-Name return case.",
  "semantic_role": "specify-returned-instance-regressions",
  "owner_role": "private-member-regressions",
  "operation": "Edit bound public fixtures and necessary expectation artifacts to cover both returned local names, private self reads, and a non-name return while retaining existing diagnostic assertions.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "returned-instance-diagnosis", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "diagnosis", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "regression-edit", "semantic_role": "returned-instance-regression-edit", "artifact_kind": "test-change", "language": "Python", "scope": "current-checkout", "phase": "regression", "state": "edited"}
  ],
  "preconditions": [
    {"key": "returned-instance-mismatch-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:private-member-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "constructor-return-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-private-member-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "non-name-return-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-assertions",
      "instruction": "Inspect both returned-name branches, all intended self reads, the non-name return, and retained positive unused-member expectations. Confirm the target warning remains enabled.",
      "evidence_refs": ["pylint-dev/pylint:4668:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4668:repair:f6c813824183"],
  "evidence_refs": ["pylint-dev/pylint:4668:regression"],
  "resource": "references/actions/regressions.md",
  "package_id": "workflow:verified-history:c87ac9d043b1a02e14aba0d2",
  "read_set": ["role:private-member-regressions", "role:public-test-runner"],
  "write_set": ["role:private-member-regressions"],
  "invalidates": ["public-validation-observed"]
}
```

Fixture existence is not execution evidence. Retain [validation](validate.md).
