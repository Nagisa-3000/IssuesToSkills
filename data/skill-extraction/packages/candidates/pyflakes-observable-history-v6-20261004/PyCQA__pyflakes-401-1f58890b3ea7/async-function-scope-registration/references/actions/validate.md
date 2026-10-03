# Validate the edit

Bind and render current public commands. Run the annotated asynchronous reproduction, new regression, neighboring annotation tests, and an ordinary-function counterpart. Review the gate and exercise supported runtimes where available. Report unavailable runtime checks as UNKNOWN rather than proven compatibility.

The supplied historical assertion and later changed-test qualification do not replace current execution. This Action does not edit source or test expectations. Failed outcomes must remain visible.

```arex-contract-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891:validate",
  "intent": "Observe corrected asynchronous analysis and verify preserved neighboring behavior.",
  "mechanism": "Execute public reproductions and repository tests against the modified scope registry.",
  "semantic_role": "scope-registration-validation",
  "owner_role": "annotation-regression-tests",
  "operation": "Run bound public reproduction and annotation checks, compare ordinary-function behavior, and review or probe supported-runtime compatibility; record actual outcomes without editing source or expectations.",
  "kind": "validate",
  "inputs": [
    {
      "name": "scope-patch",
      "semantic_role": "async-scope-validation-target",
      "artifact_kind": "code-and-test-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "async-scope-validation-result",
      "artifact_kind": "public-check-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-validation",
      "state": "outcomes-recorded",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "async-function-scope-registered", "value": true, "evaluator": "evidence"},
    {"key": "annotated-async-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-validation-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "annotated-async-analysis-correct", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-function-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-version-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "annotated-async-public-reproduction",
      "instruction": "Analyze the public class/parameter-name collision reproduction through the current analyzer. Require no Module.parent crash and no unexpected diagnostics; record actual command and outcome.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "annotation-regression-and-adjacent-tests",
      "instruction": "Execute the new regression and neighboring annotation tests, compare an ordinary-function counterpart, and review or exercise supported-version gating. Record passes, failures, and unavailable-runtime checks separately. Do not infer whole-project safety.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:76dfcbfcb074afe10f1cb891:repair"],
  "read_set": ["role:ast-scope-classification", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:76dfcbfcb074afe10f1cb891"
}
```

The output records outcomes, including failures. Intended effects and assurances become established facts only when corresponding current observations pass. Merely producing a validation record is not repair success.
