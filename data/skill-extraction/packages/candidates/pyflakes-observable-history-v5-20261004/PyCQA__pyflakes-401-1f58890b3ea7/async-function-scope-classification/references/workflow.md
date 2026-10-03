# Historical workflow

Inspect the current owners and mechanism before modifying them. The repair Action covers both supplied modifications: classifier registration and annotation regression. Validation follows both changes and records actual public outcomes.

```arex-workflow-v4
{
  "id": "workflow:verified-history:76dfcbfcb074afe10f1cb891",
  "goal": "Prevent annotated async argument scope lookup from ascending past the asynchronous function boundary.",
  "mechanism": "Register asynchronous function definitions as function scopes under a runtime capability guard and cover the same-name annotation reproduction.",
  "action_ids": [
    "workflow:verified-history:76dfcbfcb074afe10f1cb891:inspect",
    "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
    "workflow:verified-history:76dfcbfcb074afe10f1cb891:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:401:repair:1f58890b3ea7"],
  "required_effects": [
    {"key": "async-function-scope-classified", "value": true, "evaluator": "evidence"},
    {"key": "annotated-async-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-annotated-async-check-passes", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-function-scope-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-scope-entries-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-annotation-tests-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-safety-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:76dfcbfcb074afe10f1cb891:inspect",
      "after": "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
      "reason": "Establish the missing classification mechanism, registry representation, runtime policy, and test owner before modifying current code.",
      "evidence_refs": ["PyCQA/pyflakes:401:body", "PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"]
    },
    {
      "before": "workflow:verified-history:76dfcbfcb074afe10f1cb891:repair",
      "after": "workflow:verified-history:76dfcbfcb074afe10f1cb891:validate",
      "reason": "Public validation must exercise the changed classification and regression, and re-observe preserved behavior.",
      "evidence_refs": ["PyCQA/pyflakes:401:fix", "PyCQA/pyflakes:401:regression"]
    }
  ]
}
```

This dependency graph expresses semantic prerequisites and verification obligations, not a claimed historical sequence of commands. Current observations may satisfy an operation already; dropping it must not remove necessary public validation.
