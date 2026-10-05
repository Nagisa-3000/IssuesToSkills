# Validate target and preserved behavior

Bind current public test commands from the current fixture owner. Execute the target and adjacent assertions and review unavailable-inference handling. Record actual command, exit status, diagnostics, and assurance evidence. Missing execution leaves the validation observation UNKNOWN.

This Action validates both modifications. It must not change implementation or expectations to accommodate unexpected output.

```arex-contract-v4
{
  "id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8:validate",
  "intent": "Observe target correction and adjacent preservation after code and fixture changes.",
  "mechanism": "Execute exact False-name and truthy-name diagnostic assertions and review the unchanged unavailable-inference policy.",
  "semantic_role": "public-repair-validation",
  "owner_role": "boolean-refactoring-tests",
  "operation": "Render and execute bound current public diagnostic tests, review the checker guard, and capture commands, outputs, exit codes, and assurance evidence without changing source or expected outputs.",
  "kind": "validate",
  "inputs": [
    {"name": "edited-checker", "semantic_role": "diagnostic-selection-implementation", "artifact_kind": "source-code", "language": "python", "scope": "boolean-refactoring", "phase": "repair", "state": "modified", "optional": false},
    {"name": "diagnostic-assertions", "semantic_role": "diagnostic-regression-assertions", "artifact_kind": "test-fixture", "language": "python", "scope": "boolean-refactoring", "phase": "repair", "state": "modified", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "public-diagnostic-validation", "artifact_kind": "test-report", "language": "python", "scope": "boolean-refactoring", "phase": "validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "inferred-value-is-truthiness-receiver", "value": true, "evaluator": "evidence"},
    {"key": "false-inferred-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "truthy-name-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unavailable-inference-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-diagnostics",
      "instruction": "Execute the bound current public fixture suite. Require simplify-boolean-expression with the fallback message for the False-assigned middle name, consider-using-ternary for the 42-assigned middle name, and no unexpected adjacent diagnostic changes. Review unavailable-inference policy against pre-edit anchors. Record actual command and results; missing execution is UNKNOWN and unexpected diagnostics are FAIL.",
      "evidence_refs": ["pylint-dev/pylint:5200:fix", "pylint-dev/pylint:5200:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:f4d7dae35352f15a7ccdd7e8:edit",
    "workflow:verified-history:f4d7dae35352f15a7ccdd7e8:regression"
  ],
  "read_set": ["role:boolean-refactoring-checker", "role:boolean-refactoring-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5200:repair:8c7e2fae6fee"],
  "evidence_refs": ["pylint-dev/pylint:5200:fix", "pylint-dev/pylint:5200:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8"
}
```
