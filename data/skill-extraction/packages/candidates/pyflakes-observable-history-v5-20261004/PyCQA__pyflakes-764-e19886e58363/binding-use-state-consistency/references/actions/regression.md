# Add the interacting annotation regression

Use the bound public diagnostic harness to assert the complete reproduction: annotation-only outer binding, outer attribute read, and same-name inner assignment. Assert both undefined-name and unused-local diagnostics. A no-exception-only test is weaker than the supplied regression.

If an equivalent public test already exists, record that fact instead of duplicating it; its successful execution still needs current validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e:regression",
  "intent": "Encode the interacting diagnostic behavior as a public regression.",
  "mechanism": "Assert undefined-name and unused-local diagnostics for the three-part annotation/read/local-assignment reproduction.",
  "semantic_role": "interaction-regression-authoring",
  "owner_role": "annotation-regression-tests",
  "operation": "Add a focused regression using the current public diagnostic test harness.",
  "kind": "edit",
  "inputs": [
    {"name": "inspected-contract", "semantic_role": "binding-use-contract", "artifact_kind": "analysis-record", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "inspected", "optional": false}
  ],
  "outputs": [
    {"name": "interaction-test", "semantic_role": "annotation-interaction-regression", "artifact_kind": "test-code", "language": "Python", "scope": "binding-use-analysis", "phase": "current", "state": "authored", "optional": false}
  ],
  "preconditions": [
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "diagnostic-harness-contract", "value": "undefined-name-and-unused-local", "evaluator": "evidence"},
    {"key": "boolean-to-structured-mismatch", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "interaction-regression", "value": "present", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-test-assertions", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-regression-assertions",
      "instruction": "Review that the test retains all three interacting constructs and asserts both diagnostics, without weakening existing assertions.",
      "evidence_refs": ["PyCQA/pyflakes:764:body", "PyCQA/pyflakes:764:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:764:repair:e19886e58363"],
  "evidence_refs": ["PyCQA/pyflakes:764:regression", "PyCQA/pyflakes:764:body"],
  "read_set": ["role:annotation-regression-tests"],
  "write_set": ["role:annotation-regression-tests"],
  "invalidates": ["annotation-suite-result", "interaction-test-result"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:a9020121b14a346d4f659c0e"
}
```

Test creation is not test execution. [Validation](validate.md) must check this modification.
