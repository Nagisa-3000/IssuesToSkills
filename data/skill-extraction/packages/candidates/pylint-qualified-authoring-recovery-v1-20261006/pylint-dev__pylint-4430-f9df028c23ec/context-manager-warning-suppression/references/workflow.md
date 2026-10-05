# Historical Workflow

The shared predicate, two guarded emission paths, and committed assertions support this realization. Operational contracts describe how to conditionally apply and validate that mechanism today; no execution of this Skill is claimed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:b74613551e6d8c24ed7692fa",
  "goal": "Suppress resource-use advice in supported context-manager implementation frames while preserving ordinary diagnostics.",
  "mechanism": "Classify the immediate Python AST frame and resolved contextmanager decorator and exclude that frame at both resource-advice emission paths.",
  "action_ids": [
    "workflow:verified-history:b74613551e6d8c24ed7692fa:inspect",
    "workflow:verified-history:b74613551e6d8c24ed7692fa:edit",
    "workflow:verified-history:b74613551e6d8c24ed7692fa:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4430:repair:f9df028c23ec"],
  "required_effects": [
    {"key": "managed-frame-advice-suppressed", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-resource-advice-preserved", "value": true, "evaluator": "evidence"},
    {"key": "resource-inference-filter-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-with-silence-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:b74613551e6d8c24ed7692fa:inspect",
      "after": "workflow:verified-history:b74613551e6d8c24ed7692fa:edit",
      "reason": "Bind both emission paths and immediate-frame semantics before adding the exclusion.",
      "evidence_refs": ["pylint-dev/pylint:4430:fix"]
    },
    {
      "before": "workflow:verified-history:b74613551e6d8c24ed7692fa:edit",
      "after": "workflow:verified-history:b74613551e6d8c24ed7692fa:validate",
      "reason": "Validate the modified classifier, emission guards, and public assertions together.",
      "evidence_refs": ["pylint-dev/pylint:4430:fix", "pylint-dev/pylint:4430:regression"]
    }
  ]
}
```
