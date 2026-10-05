# Make plugin omission observable

Pair explicit plugin configuration and checker-specific options with nonempty,
independently reviewed diagnostic expectations. Use the current harness format
for identities, positions, multiplicity, scopes, and text.

Review existing configured-plugin fixtures with missing expectations. Correct
only justified false negatives. Do not blindly regenerate expectations from
the repair or suppress newly exposed valid messages.

```arex-contract-v4
{
  "id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833:fixtures",
  "intent": "Prevent silent optional-checker omission from passing functional tests.",
  "mechanism": "Author explicit plugin diagnostic assertions and correct justified false-negative expectations.",
  "semantic_role": "plugin-regression-assertions",
  "owner_role": "plugin-functional-fixtures",
  "operation": "Edit public fixture source, configuration, and expected output to exercise configured-plugin activation and checker-specific options; review checker behavior independently and repair justified existing silent expectations.",
  "kind": "edit",
  "inputs": [
    {"name": "diagnosis", "semantic_role": "bootstrap-diagnosis", "artifact_kind": "evidence-record", "language": "Python", "scope": "functional-harness", "phase": "diagnosis", "state": "confirmed"}
  ],
  "outputs": [
    {"name": "assertions", "semantic_role": "plugin-regression-assertions", "artifact_kind": "functional-fixture-set", "language": "Python", "scope": "plugin-functional-tests", "phase": "repair", "state": "edited"}
  ],
  "preconditions": [
    {"key": "bootstrap-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:plugin-functional-fixtures", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "discriminating-plugin-assertions", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-harness-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "missing-config-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "public-checks-passed"],
  "oracle": [
    {
      "id": "review-expectations",
      "instruction": "Review nonempty configured-plugin expectations against checker behavior independently of generated repair output. Confirm checker-specific option coverage, exact diagnostic rows, and no weakening of unrelated expectations; require final public validation.",
      "evidence_refs": ["pylint-dev/pylint:4331:body", "pylint-dev/pylint:4331:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4331:repair:d0591ba2a097"],
  "evidence_refs": ["pylint-dev/pylint:4331:body", "pylint-dev/pylint:4331:regression"],
  "read_set": ["role:plugin-functional-fixtures"],
  "write_set": ["role:plugin-functional-fixtures"],
  "resource": "references/actions/fixtures.md",
  "package_id": "workflow:verified-history:a8b32e3610a8e5ec2b10b833"
}
```
