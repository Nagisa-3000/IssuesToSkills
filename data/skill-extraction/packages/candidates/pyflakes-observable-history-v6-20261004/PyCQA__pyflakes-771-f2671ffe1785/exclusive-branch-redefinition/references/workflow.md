# Workflow: classify mutually exclusive match definitions

The historical repair recognized match-case bodies in the existing alternative classifier and added a no-diagnostic regression. Current application first confirms that the same mechanism owns the symptom.

```arex-workflow-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49",
  "goal": "Remove false unused-redefinition diagnostics between mutually exclusive match cases.",
  "mechanism": "Extend the shared alternative-branch classifier with one alternative per match-case body, retaining existing branch handling and runtime compatibility.",
  "action_ids": [
    "workflow:verified-history:45a56eede77a20492da56a49:probe",
    "workflow:verified-history:45a56eede77a20492da56a49:classify",
    "workflow:verified-history:45a56eede77a20492da56a49:regression",
    "workflow:verified-history:45a56eede77a20492da56a49:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "required_effects": [
    {"key": "match-case-alternatives-recognized", "value": true, "evaluator": "evidence"},
    {"key": "match-redefinition-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "existing-if-try-classification-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-redefinition-detection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-runtime-compatibility-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:45a56eede77a20492da56a49:probe",
      "after": "workflow:verified-history:45a56eede77a20492da56a49:classify",
      "reason": "Bind the current classifier and confirm the missing match alternatives before editing it.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"]
    },
    {
      "before": "workflow:verified-history:45a56eede77a20492da56a49:probe",
      "after": "workflow:verified-history:45a56eede77a20492da56a49:regression",
      "reason": "Bind the current match test suite and reproduce the reported branch-specific symptom.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:regression"]
    },
    {
      "before": "workflow:verified-history:45a56eede77a20492da56a49:classify",
      "after": "workflow:verified-history:45a56eede77a20492da56a49:validate",
      "reason": "Validate the classifier after its modification.",
      "evidence_refs": ["PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"]
    },
    {
      "before": "workflow:verified-history:45a56eede77a20492da56a49:regression",
      "after": "workflow:verified-history:45a56eede77a20492da56a49:validate",
      "reason": "Execute the added public assertion only after it is present.",
      "evidence_refs": ["PyCQA/pyflakes:771:regression"]
    }
  ]
}
```

Preservation predicates are required current assurances, not claims that the supplied historical record executed all corresponding checks. The probe and public validation operationalize the historical mechanism without adding new historical events.
