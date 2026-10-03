# Historical Workflow

Recognize postponed references without making annotation-only declarations ordinary value assignments. Every packaged Action is included in this evidence-backed reconstruction.

```arex-workflow-v4
{
  "id": "workflow:verified-history:be71c3f9e9544046d28904cd",
  "goal": "Recognize annotation-only names in postponed type references while retaining value-binding diagnostics.",
  "mechanism": "Represent annotation-only declarations as distinct bindings, track annotation context, and condition lookup eligibility on postponement.",
  "action_ids": [
    "workflow:verified-history:be71c3f9e9544046d28904cd:inspect",
    "workflow:verified-history:be71c3f9e9544046d28904cd:repair",
    "workflow:verified-history:be71c3f9e9544046d28904cd:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:486:repair:5fc37cbda5bf"],
  "required_effects": [
    {"key": "annotation-only-binding-distinguished", "value": true, "evaluator": "evidence"},
    {"key": "postponed-reference-matrix-validated", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "bare-reference-without-postponement-remains-undefined", "value": true, "evaluator": "evidence"},
    {"key": "annotation-only-is-not-runtime-value-assignment", "value": true, "evaluator": "evidence"},
    {"key": "later-unused-value-assignment-reported-once", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:be71c3f9e9544046d28904cd:inspect",
      "after": "workflow:verified-history:be71c3f9e9544046d28904cd:repair",
      "reason": "Locate current owners and distinguish bare, quoted, future-postponed, and ordinary value contexts before changing lookup.",
      "evidence_refs": ["PyCQA/pyflakes:486:body", "PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"]
    },
    {
      "before": "workflow:verified-history:be71c3f9e9544046d28904cd:repair",
      "after": "workflow:verified-history:be71c3f9e9544046d28904cd:validate",
      "reason": "Validate the new binding/context behavior against accepted postponed references and retained undefined/unused diagnostics.",
      "evidence_refs": ["PyCQA/pyflakes:486:fix", "PyCQA/pyflakes:486:regression"]
    }
  ]
}
```
