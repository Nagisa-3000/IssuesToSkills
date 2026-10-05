# Inspect inference and diagnostic selection

Read the current checker and test owners without modifying source or fixture files. Trace inference through the unavailable-result guard to the truthiness receiver. Confirm that the public symptom and current data flow match the historical mechanism.

Unknown interface semantics or unavailable owners leave applicability UNKNOWN; they do not produce a confirmed binding.

```arex-contract-v4
{
  "id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8:inspect",
  "intent": "Establish applicability and bind current semantic owners.",
  "mechanism": "Trace safe inference into the truthiness decision for an and/or refactoring diagnostic.",
  "semantic_role": "mechanism-inspection",
  "owner_role": "boolean-refactoring-checker",
  "operation": "Read current public checker and fixture anchors, compare the reported expression with the suggested ternary, and record compatible owner and inference-interface bindings without editing checkout files.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "located-mechanism", "semantic_role": "diagnostic-mechanism-binding", "artifact_kind": "review-record", "language": "python", "scope": "boolean-refactoring", "phase": "inspection", "state": "confirmed", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "mechanism-match-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "current-test-owner-bound", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "truthy-name-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unavailable-inference-policy-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-dataflow",
      "instruction": "Record anchors for inference, unavailable-result handling, and the truthiness receiver. Confirm that successful inference produces a value with a compatible bool_value interface, and bind the public fixture owner. Probe a=True, b=False, c=True: observe True for (a and b) or c and False for b if a else c. Verify that source and fixture contents were not changed by inspection.",
      "evidence_refs": ["pylint-dev/pylint:5200:body", "pylint-dev/pylint:5200:fix", "pylint-dev/pylint:5200:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:boolean-refactoring-checker", "role:boolean-refactoring-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5200:repair:8c7e2fae6fee"],
  "evidence_refs": ["pylint-dev/pylint:5200:body", "pylint-dev/pylint:5200:fix", "pylint-dev/pylint:5200:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:f4d7dae35352f15a7ccdd7e8"
}
```
