# Validate both modifications

Bind and render current public commands before execution. The empty argv arrays are deliberately unbound. Historical report commands are evidence, not automatic authorization for a current checkout.

Execute the focused assertion, mixed-signature reproduction, and adjacent public checks. Record actual scope, runtime, output, and current anchors. A required FAIL or UNKNOWN prevents a validated output. A target-test skip does not establish success on a supported runtime.

Where a public original-base control is available, compare the focused assertion against that base without changing the repair. This is optional current guidance, not a claim of historical execution. These expanded adjacent checks likewise are current assurance requirements, not invented historical results.

```arex-contract-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af:validate",
  "intent": "Establish current public evidence for the repair and preserved adjacent behavior.",
  "mechanism": "Execute the focused annotation assertion, public reproduction, and adjacent annotation and binding checks after all edits.",
  "semantic_role": "public-repair-validation",
  "owner_role": "annotation-test-suite",
  "operation": "Run bound public checks without editing tracked files, record outcomes, and produce a validated candidate only when all required checks pass.",
  "kind": "validate",
  "inputs": [
    {
      "name": "test-ready-candidate",
      "semantic_role": "argument-accounting-candidate",
      "artifact_kind": "checkout-with-evidence",
      "language": "python",
      "scope": "function-argument-accounting",
      "phase": "regression",
      "state": "assertion-present-unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validated-candidate",
      "semantic_role": "argument-accounting-candidate",
      "artifact_kind": "checkout-with-evidence",
      "language": "python",
      "scope": "function-argument-accounting",
      "phase": "validation",
      "state": "public-checks-passed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "positional-only-accounting-implemented", "value": true, "evaluator": "evidence"},
    {"key": "focused-assertion-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-fresh", "value": true, "evaluator": "evidence", "description": "Observed only after the bound checks pass on the current edited candidate."}
  ],
  "preserves": [
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "parameter-binding-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "focused-public-test",
      "instruction": "Execute the focused current public assertion on a runtime supporting positional-only syntax and verify no diagnostics. Record runtime and result; a skip is not target repair success.",
      "evidence_refs": ["PyCQA/pyflakes:507:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "mixed-signature-mre",
      "instruction": "Run the public mixed positional-only and keyword-only reproduction through the current analyzer and verify neither annotation import is falsely reported unused.",
      "evidence_refs": ["PyCQA/pyflakes:507:body"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-public-checks",
      "instruction": "Execute the public annotation suite and public checks for ordinary and keyword-only annotations, parameter bindings, genuine unused imports, and supported-runtime compatibility. Record the tested scope; do not infer whole-project, cross-project, or hidden acceptance.",
      "evidence_refs": ["PyCQA/pyflakes:507:fix", "PyCQA/pyflakes:507:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:507:repair:be8803601900"],
  "evidence_refs": ["PyCQA/pyflakes:507:body", "PyCQA/pyflakes:507:fix", "PyCQA/pyflakes:507:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "read_set": ["role:function-argument-collector", "role:annotation-test-suite"],
  "write_set": [],
  "validation_for": [
    "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
    "workflow:verified-history:b95b785d6a29c4b04e9050af:regression"
  ]
}
```
