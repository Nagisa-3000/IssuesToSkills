# Workflow: explicit parent context for early loads

This is a source-backed reconstruction of one repair, not a claim of recorded historical execution of the authored inspection and validation steps.

```arex-workflow-v4
{
  "id": "workflow:verified-history:73c1883f7ed05d43025127fa",
  "goal": "Prevent early augmented-assignment load analysis from reading uninitialized parent metadata while preserving adjacent diagnostics.",
  "mechanism": "Make parent context explicit in load analysis and supply it according to ordinary versus early dispatch semantics.",
  "action_ids": [
    "workflow:verified-history:73c1883f7ed05d43025127fa:inspect",
    "workflow:verified-history:73c1883f7ed05d43025127fa:repair",
    "workflow:verified-history:73c1883f7ed05d43025127fa:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:744:repair:e0d7a6be8959"],
  "required_effects": [
    {"key": "explicit-parent-context-installed", "value": true, "evaluator": "evidence"},
    {"key": "augmented-load-regression-added", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-load-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "builtin-print-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "augmented-value-target-order-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:73c1883f7ed05d43025127fa:inspect",
      "after": "workflow:verified-history:73c1883f7ed05d43025127fa:repair",
      "reason": "Confirm metadata timing and caller parent semantics before changing the interface.",
      "evidence_refs": ["PyCQA/pyflakes:744:body", "PyCQA/pyflakes:744:fix"]
    },
    {
      "before": "workflow:verified-history:73c1883f7ed05d43025127fa:repair",
      "after": "workflow:verified-history:73c1883f7ed05d43025127fa:validate",
      "reason": "Validate the changed interface, added regression, and preserved adjacent behavior after editing.",
      "evidence_refs": ["PyCQA/pyflakes:744:fix", "PyCQA/pyflakes:744:regression"]
    }
  ]
}
```

Current ordering follows bound ports, prerequisites, semantic dependencies, and verification, not merely historical list position. Already satisfied operations may be omitted only with current evidence for their outputs and effects. Historical contracts remain immutable. A fresh observation is distinct from a behavioral assurance; editing invalidates validation freshness, not the required preservation invariants.
