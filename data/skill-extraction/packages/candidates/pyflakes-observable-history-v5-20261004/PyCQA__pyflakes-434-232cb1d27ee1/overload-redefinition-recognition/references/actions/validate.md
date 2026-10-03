# Validate recognition and adjacent diagnostics

Resolve the current public runner and bind current argv commands before execution. Render those commands in the current plan. Empty historical command arrays mean no executable command was supplied, not that validation is optional.

Run both focused regressions and surrounding annotation tests. Probe ordinary repeated definitions, non-typing lookalikes, nearest-binding shadowing, existing attribute recognition, and both decorator positions. Where practical, use a public base control to show that the focused assertions expose the defect.

Record actual outcomes and exact scope. Unknown or failed required checks prevent a success claim. Changed-test-only execution does not establish whole-project correctness.

```arex-contract-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:validate",
  "intent": "Verify the repair and assertions while preserving adjacent diagnostics.",
  "mechanism": "Execute bound public regression tests and preservation probes.",
  "semantic_role": "repair-validation",
  "owner_role": "type-annotation-regressions",
  "operation": "Run current public oracles and record their results.",
  "kind": "validate",
  "inputs": [
    {"name": "repair", "semantic_role": "overload-recognition-change", "artifact_kind": "source-change", "language": "Python", "scope": "current-checkout", "phase": "implementation", "state": "modified", "optional": false},
    {"name": "assertions", "semantic_role": "overload-regression-change", "artifact_kind": "test-change", "language": "Python", "scope": "current-checkout", "phase": "regression", "state": "authored", "optional": false}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "overload-validation-result", "artifact_kind": "execution-record", "language": "Python", "scope": "current-checkout", "phase": "validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "regression-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-passed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nearest-binding-shadowing", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-redefinition-reporting", "value": "preserved", "evaluator": "evidence"},
    {"key": "existing-attribute-recognition", "value": "preserved", "evaluator": "evidence"},
    {"key": "function-source-guard", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "focused-and-adjacent-tests",
      "instruction": "Run the class-local and multiple-decorator regressions and surrounding public type-annotation tests; record results and exact test scope.",
      "evidence_refs": ["PyCQA/pyflakes:434:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "preservation-probes",
      "instruction": "Check ordinary repeated definitions, non-typing lookalikes, nearest-binding shadowing, existing attribute recognition, the retained function-source guard, and both decorator positions using public current probes and review.",
      "evidence_refs": ["PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:fix", "PyCQA/pyflakes:434:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:fc3525ab47a41bc94f54d0d0:repair",
    "workflow:verified-history:fc3525ab47a41bc94f54d0d0:regressions"
  ],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs": ["PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:fix", "PyCQA/pyflakes:434:regression"],
  "read_set": ["role:overload-recognition", "role:unused-redefinition-reporting", "role:type-annotation-regressions"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0"
}
```
