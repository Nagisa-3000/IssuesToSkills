# Add exact diagnostic regression coverage

Use a name assigned `False` as the middle operand in `condition and middle or fallback`. Assert `simplify-boolean-expression` and its fallback message, not merely the absence of a crash or a ternary message. Retain the adjacent name assigned `42` and its `consider-using-ternary` assertion.

A current base-with-regression run may establish the current failure before implementation changes. That is a newly executed public check if actually run, not a historical execution claim.

Retain the [validation Action](validate.md) after fixture modifications.

```arex-contract-v4
{
  "id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8:regression",
  "intent": "Make the False-inferred diagnostic defect observable while protecting adjacent truthy behavior.",
  "mechanism": "Pair a False-assigned middle-name assertion with a preserved truthy-name assertion.",
  "semantic_role": "diagnostic-regression-coverage",
  "owner_role": "boolean-refactoring-tests",
  "operation": "Add the public False-name fixture and exact simplification expectation in the bound harness; preserve the existing truthy-name ternary expectation and verify fixture discovery.",
  "kind": "edit",
  "inputs": [
    {"name": "located-mechanism", "semantic_role": "diagnostic-mechanism-binding", "artifact_kind": "review-record", "language": "python", "scope": "boolean-refactoring", "phase": "inspection", "state": "confirmed", "optional": false}
  ],
  "outputs": [
    {"name": "diagnostic-assertions", "semantic_role": "diagnostic-regression-assertions", "artifact_kind": "test-fixture", "language": "python", "scope": "boolean-refactoring", "phase": "repair", "state": "modified", "optional": false}
  ],
  "preconditions": [
    {"key": "role:boolean-refactoring-tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-test-owner-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "false-inferred-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "truthy-name-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unavailable-inference-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-diagnostic-assertions",
      "instruction": "Inspect discoverable fixtures and matching expected output. Require the False-assigned middle name to expect simplify-boolean-expression with the fallback message, while the 42-assigned middle name still expects consider-using-ternary. Verify correspondence between fixtures, annotations, and expected output in the current public harness.",
      "evidence_refs": ["pylint-dev/pylint:5200:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:boolean-refactoring-tests"],
  "write_set": ["role:boolean-refactoring-tests"],
  "source_ids": ["pylint-dev/pylint:5200:repair:8c7e2fae6fee"],
  "evidence_refs": ["pylint-dev/pylint:5200:regression"],
  "resource": "references/actions/regression.md",
  "package_id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8"
}
```
