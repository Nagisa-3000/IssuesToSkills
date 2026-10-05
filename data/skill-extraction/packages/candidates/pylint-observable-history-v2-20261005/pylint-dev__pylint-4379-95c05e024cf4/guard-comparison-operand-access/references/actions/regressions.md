# Add unsupported-shape regressions

Bind the public fixture and its expected-output mechanism. Add the two supplied Python snippets, retaining all existing examples and expected suggestions. Neither added case is a min/max refactoring opportunity. Do not update expected diagnostics merely to mask a changed behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:ba0f15907d742a3c30dae2cf:regressions",
  "intent": "Retain public coverage for unsupported right-hand operand shapes.",
  "mechanism": "Add negative-literal equality and list-membership comparisons to the checker functional fixture.",
  "semantic_role": "unsupported-operand-regression-coverage",
  "owner_role": "min-max-functional-regressions",
  "operation": "Add var = 1; if var == -1: var = None and var2 = 1; if var2 in [1, 2]: var2 = None as separate correctly indented Python cases in the bound public harness. Retain existing fixture behavior and expected outputs.",
  "kind": "edit",
  "inputs": [
    {"name": "reviewed-owner", "semantic_role": "operand-owner-review", "artifact_kind": "review-record", "language": "python", "scope": "comparison-operand-extractor", "phase": "diagnosis", "state": "reviewed"}
  ],
  "outputs": [],
  "preconditions": [
    {"key": "operand-owner-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "role:min-max-functional-regressions", "value": true, "evaluator": "file_exists"},
    {"key": "public-fixture-harness-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "unsupported-shape-regressions-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-name-constant-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "neighboring-refactoring-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-regression-shapes",
      "instruction": "Inspect the fixture diff and expected-output bindings. Both supplied cases must be collected by the public harness, exercise unsupported operand shapes, and require no min/max suggestion; existing examples and expectations remain intact.",
      "evidence_refs": ["pylint-dev/pylint:4379:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4379:repair:95c05e024cf4"],
  "evidence_refs": ["pylint-dev/pylint:4379:body", "pylint-dev/pylint:4379:regression"],
  "read_set": ["role:min-max-functional-regressions"],
  "write_set": ["role:min-max-functional-regressions"],
  "resource": "references/actions/regressions.md",
  "package_id": "workflow:verified-history:ba0f15907d742a3c30dae2cf"
}
```
