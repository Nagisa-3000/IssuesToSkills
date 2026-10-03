# Historical Workflow

The mechanism is to repair missing asynchronous-function scope classification at its semantic owner, not suppress the final missing-parent exception. The Actions below reconstruct inspection, the supplied edit and regression, and public validation obligations. They do not assert historical test execution.

```arex-workflow-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891",
  "goal": "Prevent annotated asynchronous-function argument binding from escaping its intended function scope due to missing AST scope registration.",
  "mechanism": "Register asynchronous function definitions using ordinary function scope representation under the supported-version gate, and cover the annotated parameter/class-name collision.",
  "action_ids": [
    "workflow:verified-history:76dfcbfcb074afe10f1cb891:inspect",
    "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
    "workflow:verified-history:76dfcbfcb074afe10f1cb891:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "required_effects": [
    {"key": "async-function-scope-registered", "value": true, "evaluator": "evidence"},
    {"key": "annotated-async-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "annotated-async-analysis-correct", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-function-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-version-import-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:76dfcbfcb074afe10f1cb891:inspect",
      "after": "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
      "reason": "Current evidence must connect absent asynchronous scope registration to the argument-binding failure before modification.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix"]
    },
    {
      "before": "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
      "after": "workflow:verified-history:76dfcbfcb074afe10f1cb891:validate",
      "reason": "The registry edit and added regression need fresh public validation after modification.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"]
    }
  ]
}
```

Action cards: [inspect](actions/inspect.md), [repair](actions/repair.md), [validate](actions/validate.md). All packaged Actions belong to this single canonical Workflow. No Pattern or additional historical realization is claimed.
