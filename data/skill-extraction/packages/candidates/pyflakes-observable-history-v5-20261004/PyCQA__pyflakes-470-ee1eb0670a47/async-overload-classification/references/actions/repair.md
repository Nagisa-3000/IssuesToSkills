# Extend the function-node family and add regression coverage

At the currently bound compatibility owner, include synchronous and async function definition AST classes wherever both are supported. Preserve a synchronous-only branch if older supported runtimes lack the async class.

Use that family in the existing overload source-node guard. Leave typing decorator identity and scope resolution unchanged; do not exempt all repeated async definitions.

At the current test owner, add two async `typing.overload` declarations followed by an async implementation. The historical assertion used type comments, `pass` declaration bodies, and `return s` in the implementation. Adapt the harness and syntax to the public current checkout, retaining any required runtime guard.

All effects below are expected targets pending validation. Bind current role predicates to real objects; historical file names are not bindings.

```arex-contract-v4
{
  "id": "workflow:verified-history:a571de127bfc56dc56819c7c:repair",
  "intent": "Recognize async overload declarations through the existing function classification path.",
  "mechanism": "Broaden only the function-node type guard using a compatible node family and add an async regression.",
  "semantic_role": "function-node-family-repair",
  "owner_role": "overload-classification",
  "operation": "Edit the compatible node family, overload guard, and public regression coverage.",
  "kind": "edit",
  "inputs": [
    {
      "name": "classification-findings",
      "semantic_role": "overload-classification-findings",
      "artifact_kind": "owner-map-and-probe-record",
      "language": "python",
      "scope": "current-checkout-overload-analysis",
      "phase": "diagnosis",
      "state": "reviewed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "overload-repair",
      "semantic_role": "overload-classification-change",
      "artifact_kind": "source-and-test-diff",
      "language": "python",
      "scope": "current-checkout-overload-analysis",
      "phase": "repair",
      "state": "modified-unvalidated",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "synchronous-only-guard-causes-async-failure", "value": true, "evaluator": "evidence"},
    {"key": "role:overload-classification", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:function-node-family", "value": true, "evaluator": "file_exists"},
    {"key": "role:overload-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "supported-runtime-policy-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "async-overload-redefinition-accepted", "value": true, "evaluator": "evidence", "description": "Expected behavior requiring post-edit observation."},
    {"key": "async-overload-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "typing-decorator-resolution-preserved", "value": true, "evaluator": "evidence"},
    {"key": "synchronous-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-redefinition-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-bounded-diff",
      "instruction": "Review the public diff for a compatible function-node family, use of that family in the overload guard, unchanged decorator resolution, and an async regression with two declarations plus an implementation and required runtime guards.",
      "evidence_refs": ["PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:470:repair:ee1eb0670a47"],
  "evidence_refs": ["PyCQA/pyflakes:470:fix", "PyCQA/pyflakes:470:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:a571de127bfc56dc56819c7c",
  "read_set": ["role:overload-classification", "role:function-node-family", "role:overload-regression-tests"],
  "write_set": ["role:overload-classification", "role:function-node-family", "role:overload-regression-tests"],
  "invalidates": ["pre-edit-diagnostic-results", "pre-edit-regression-results"]
}
```
