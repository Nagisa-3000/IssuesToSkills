# Add public async regression coverage

At the bound public test owner, add two async declarations decorated by imported `typing.overload`, followed by an undecorated async implementation of the same name. Use the current suite's no-diagnostic assertion.

Handle runtimes that cannot parse async syntax according to current support policy. The historical test used type comments and `pass`; its concrete name and path are not current bindings. Omit this edit if equivalent coverage already exists and record evidence of that coverage.

```arex-contract-v4
{
  "id": "workflow:verified-history:a571de127bfc56dc56819c7c:add-regression",
  "intent": "Provide a public regression assertion for intentional async overload redefinitions.",
  "mechanism": "Test two decorated async overload declarations followed by their async implementation.",
  "semantic_role": "cover-async-overload-redefinitions",
  "owner_role": "overload-regression-tests",
  "operation": "Add a no-diagnostic async overload regression to the bound test owner with appropriate runtime compatibility handling.",
  "kind": "edit",
  "inputs": [
    {
      "name": "recognition-review",
      "semantic_role": "overload-node-omission-review",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout-overload-recognition",
      "phase": "pre-edit",
      "state": "confirmed"
    }
  ],
  "outputs": [],
  "preconditions": [
    {"key": "async-function-node-omission-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:overload-regression-tests", "value": true, "evaluator": "file_exists", "description": "The current public overload test owner is located and bound."}
  ],
  "effects": [
    {"key": "async-overload-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "sync-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-ast-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-regression-shape",
      "instruction": "Inspect the added public test for two typing overload async declarations, an async implementation of the same name, a no-diagnostic assertion, and runtime compatibility handling appropriate to current support policy.",
      "evidence_refs": ["PyCQA/pyflakes:470:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:overload-regression-tests"],
  "write_set": ["role:overload-regression-tests"],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:body", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/add-regression.md",
  "package_id": "workflow:verified-history:a571de127bfc56dc56819c7c"
}
```
