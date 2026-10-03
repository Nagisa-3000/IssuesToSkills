# Historical workflow: annotation-only bindings are not redefinitions

The dependency graph expresses the supplied repair mechanism and its verification requirements. It does not claim a newly observed historical sequence of developer actions.

```arex-workflow-v4
{
  "id": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7",
  "goal": "Eliminate false unused-import redefinition diagnostics caused by annotation-only bindings.",
  "mechanism": "Keep annotation-only metadata from participating as a new definition in the redefinition predicate, and assert the import/annotation/use behavior.",
  "action_ids": [
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:probe",
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:edit",
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:regression",
    "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:617:repair:3de8e6120291"],
  "required_effects": [
    {"key": "annotation-only-nonredefining", "value": true, "evaluator": "evidence"},
    {"key": "import-annotation-use-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": "PASS", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-definition-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:probe",
      "after": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:edit",
      "reason": "Confirm annotation-only semantics and locate the predicate owner before changing it.",
      "evidence_refs": ["PyCQA/pyflakes:617:body", "PyCQA/pyflakes:617:fix"]
    },
    {
      "before": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:edit",
      "after": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:regression",
      "reason": "This realization passes the candidate implementation to the regression authoring operation.",
      "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"]
    },
    {
      "before": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:edit",
      "after": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:validate",
      "reason": "Validation must observe the modified predicate.",
      "evidence_refs": ["PyCQA/pyflakes:617:fix", "PyCQA/pyflakes:617:regression"]
    },
    {
      "before": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:regression",
      "after": "workflow:verified-history:f7b7dad5578cfb8d7454d8e7:validate",
      "reason": "Validation must execute the added regression assertion.",
      "evidence_refs": ["PyCQA/pyflakes:617:regression"]
    }
  ]
}
```
