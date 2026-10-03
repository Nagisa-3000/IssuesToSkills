# Canonical Workflow

Include positional-only names and annotations in the existing argument-accounting pipeline, then validate the focused regression and preserved behavior.

All four Action cards are covered below. The ordering between implementation and regression edits reflects this realization's matching ports, not an undocumented claim about developer chronology. Current DAGs may omit already satisfied operations only when current evidence supports doing so; modifying operations retain their validation closure.

```arex-workflow-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "goal": "Remove false unused-import diagnostics caused by omitted positional-only parameter annotations.",
  "mechanism": "Extend function-argument collection to include positional-only names and annotations with compatible AST access, retain a focused assertion, and validate the edited candidate.",
  "action_ids": [
    "workflow:verified-history:b95b785d6a29c4b04e9050af:probe",
    "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
    "workflow:verified-history:b95b785d6a29c4b04e9050af:regression",
    "workflow:verified-history:b95b785d6a29c4b04e9050af:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:507:repair:be8803601900"],
  "required_effects": [
    {"key": "positional-only-accounting-implemented", "value": true, "evaluator": "evidence"},
    {"key": "focused-assertion-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-fresh", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "adjacent-annotation-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "parameter-binding-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-unused-import-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:b95b785d6a29c4b04e9050af:probe",
      "after": "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
      "reason": "Confirm the current omission and compatible AST support before editing the collector.",
      "evidence_refs": ["PyCQA/pyflakes:507:body", "PyCQA/pyflakes:507:fix"]
    },
    {
      "before": "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
      "after": "workflow:verified-history:b95b785d6a29c4b04e9050af:regression",
      "reason": "The regression operation consumes this realization's implementation-edited candidate; this is not a historical chronology claim.",
      "evidence_refs": ["PyCQA/pyflakes:507:fix", "PyCQA/pyflakes:507:regression"]
    },
    {
      "before": "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
      "after": "workflow:verified-history:b95b785d6a29c4b04e9050af:validate",
      "reason": "Behavioral validation must follow the collector modification.",
      "evidence_refs": ["PyCQA/pyflakes:507:fix", "PyCQA/pyflakes:507:regression"]
    },
    {
      "before": "workflow:verified-history:b95b785d6a29c4b04e9050af:regression",
      "after": "workflow:verified-history:b95b785d6a29c4b04e9050af:validate",
      "reason": "Execute the focused assertion after the test edit and refresh public observations after all modifications.",
      "evidence_refs": ["PyCQA/pyflakes:507:regression"]
    }
  ]
}
```
