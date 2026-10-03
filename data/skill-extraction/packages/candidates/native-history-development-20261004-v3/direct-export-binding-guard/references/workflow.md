# Canonical historical Workflow

The implementation and regression assertion support this repair mechanism. Current validation obligations below do not imply undocumented historical execution.

```arex-workflow-v4
{
  "id": "direct-export-binding-guard",
  "goal": "Prevent indirect module-level export targets from crashing assignment-only export handling.",
  "mechanism": "Guard special export dispatch by compatible immediate assignment parent types, retaining ordinary binding and adding an indirect-target unused-import regression.",
  "action_ids": [
    "direct-export-binding-guard.inspect",
    "direct-export-binding-guard.guard-and-regress",
    "direct-export-binding-guard.validate"
  ],
  "source_ids": ["PyCQA/pyflakes:674"],
  "required_effects": [
    {"key": "export-dispatch-parent-compatible", "value": true, "evaluator": "evidence"},
    {"key": "indirect-export-regression-defined", "value": true, "evaluator": "evidence"},
    {"key": "current-public-validation", "value": "passed", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "direct-module-export-handling", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-unused-import-analysis", "value": "preserved", "evaluator": "evidence"},
    {"key": "module-scope-restriction", "value": "preserved", "evaluator": "evidence"},
    {"key": "existing-earlier-binding-branches", "value": "preserved", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "direct-export-binding-guard.inspect",
      "after": "direct-export-binding-guard.guard-and-regress",
      "reason": "Establish the current parent mismatch and available fallback before changing dispatch.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"]
    },
    {
      "before": "direct-export-binding-guard.guard-and-regress",
      "after": "direct-export-binding-guard.validate",
      "reason": "Validate the changed dispatch and regression, including retained unused-import behavior.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"]
    }
  ]
}
```
