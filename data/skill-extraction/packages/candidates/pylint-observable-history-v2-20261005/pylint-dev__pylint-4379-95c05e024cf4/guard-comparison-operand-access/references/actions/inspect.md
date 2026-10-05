# Inspect comparison operand extraction

Read the bound checker and public fixture without modifying them. Reproduce or inspect the public failure, identify the right operand's AST kind, and verify that the candidate check only intends to extract names and constants. Locate the regression harness and existing supported examples. Do not infer applicability from a traceback label alone.

```arex-contract-v4
{
  "id": "workflow:verified-history:ba0f15907d742a3c30dae2cf:inspect",
  "intent": "Establish the unsafe operand access and current semantic bindings.",
  "mechanism": "Inspect the comparison extraction branch and publicly probe unsupported operand shapes.",
  "semantic_role": "operand-shape-diagnosis",
  "owner_role": "comparison-operand-extractor",
  "operation": "Read the bound owner and fixture; record hashed anchors, AST kinds, supported branches, and public failure evidence without changing checkout files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "reviewed-owner", "semantic_role": "operand-owner-review", "artifact_kind": "review-record", "language": "python", "scope": "comparison-operand-extractor", "phase": "diagnosis", "state": "reviewed"}
  ],
  "preconditions": [
    {"key": "role:comparison-operand-extractor", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:min-max-functional-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "operand-owner-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "supported-name-constant-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "neighboring-refactoring-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-shapes",
      "instruction": "Record whether the current negative literal is a unary node and membership operand is a list node, whether unsupported nodes reach constant-style access, and whether Name/Const extraction is the intended supported behavior. Confirm the probe made no source edits.",
      "evidence_refs": ["pylint-dev/pylint:4379:body", "pylint-dev/pylint:4379:fix", "pylint-dev/pylint:4379:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4379:repair:95c05e024cf4"],
  "evidence_refs": ["pylint-dev/pylint:4379:body", "pylint-dev/pylint:4379:fix", "pylint-dev/pylint:4379:regression"],
  "read_set": ["role:comparison-operand-extractor", "role:min-max-functional-regressions"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:ba0f15907d742a3c30dae2cf"
}
```
