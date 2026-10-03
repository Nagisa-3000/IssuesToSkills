# Historical Workflow

Resolve bare decorator names through the available scopes, respecting the first binding and imported-symbol identity. Inspect the full decorator list before deciding whether the existing function qualifies for the overload exception.

Dependencies reconstruct the supplied repair's semantic requirements, not an execution trace. All packaged Actions are covered here.

```arex-workflow-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0",
  "goal": "Prevent false unused-redefinition diagnostics for typing.overload declarations with enclosing imports or additional decorators.",
  "mechanism": "First-binding lookup through the scope stack with typing.overload import identity, combined with any-match decorator scanning at the unused-redefinition gate.",
  "action_ids": [
    "workflow:verified-history:fc3525ab47a41bc94f54d0d0:inspect",
    "workflow:verified-history:fc3525ab47a41bc94f54d0d0:repair",
    "workflow:verified-history:fc3525ab47a41bc94f54d0d0:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "required_effects": [
    {"key": "recognition-repair-present", "value": true, "evaluator": "evidence"},
    {"key": "public-regression-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "required-public-checks-pass", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "first-binding-shadowing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-qualified-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "function-node-restriction-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:inspect",
      "after": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:repair",
      "reason": "Establish binding identity and one supported recognition defect before modifying the diagnostic exception.",
      "evidence_refs": ["PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:fix"]
    },
    {
      "before": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:repair",
      "after": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:validate",
      "reason": "Changed recognition and public regression assertions require post-edit execution; historical assertions are not current results.",
      "evidence_refs": ["PyCQA/pyflakes:434:fix", "PyCQA/pyflakes:434:regression"]
    }
  ]
}
```
