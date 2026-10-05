# Historical realization

The source demonstrates diagnostic enrichment and matching assertion edits. The following inspection and validation contracts are authored obligations grounded in that evidence, not claims that those operations ran historically.

```arex-workflow-v4
{
  "id": "workflow:verified-history:124787fcb0844f5e9acb613d",
  "goal": "Identify the inferred AST node kind in invalid special-class assignment diagnostics without changing rejection semantics.",
  "mechanism": "Add a diagnostic interpolation slot, supply inferred.__class__.__name__ at the existing rejection emission, and align corresponding assertions.",
  "action_ids": [
    "workflow:verified-history:124787fcb0844f5e9acb613d:inspect",
    "workflow:verified-history:124787fcb0844f5e9acb613d:edit",
    "workflow:verified-history:124787fcb0844f5e9acb613d:validate"
  ],
  "source_ids": ["pylint-dev/pylint:7467:repair:b47aa3076ee0"],
  "required_effects": [
    {"key": "diagnostic-kind-included", "value": true, "evaluator": "evidence"},
    {"key": "assertions-match-diagnostic", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "acceptance-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-metadata-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-checker-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:124787fcb0844f5e9acb613d:inspect",
      "after": "workflow:verified-history:124787fcb0844f5e9acb613d:edit",
      "reason": "Confirm the existing inferred-value rejection boundary and bind its owners before editing.",
      "evidence_refs": ["pylint-dev/pylint:7467:fix"]
    },
    {
      "before": "workflow:verified-history:124787fcb0844f5e9acb613d:edit",
      "after": "workflow:verified-history:124787fcb0844f5e9acb613d:validate",
      "reason": "Observe agreement of the changed template, supplied argument, and assertions while checking preserved behavior.",
      "evidence_refs": ["pylint-dev/pylint:7467:fix", "pylint-dev/pylint:7467:regression"]
    }
  ]
}
```
