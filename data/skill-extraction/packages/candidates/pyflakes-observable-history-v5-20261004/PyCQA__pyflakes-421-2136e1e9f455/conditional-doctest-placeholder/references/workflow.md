# Workflow: avoid a synthetic doctest binding collision

This is the canonical historical Workflow. Its source describes the report, the guard, and the regression assertion. Locate/probe and current validation instructions operationalize that evidence; they do not assert that those steps were historically executed.

The code guard and regression addition can follow the locating probe independently. Validation requires both outputs. List position does not impose any additional dependency.

```arex-workflow-v4
{
  "id": "workflow:verified-history:c76d35c9a48e360887b3c443",
  "goal": "Prevent a source-less synthetic doctest underscore from colliding with a module-level underscore binding while retaining unused-import diagnostics.",
  "mechanism": "Initialize the synthetic doctest underscore only when the module scope does not already contain underscore.",
  "action_ids": [
    "workflow:verified-history:c76d35c9a48e360887b3c443:locate",
    "workflow:verified-history:c76d35c9a48e360887b3c443:guard",
    "workflow:verified-history:c76d35c9a48e360887b3c443:regression",
    "workflow:verified-history:c76d35c9a48e360887b3c443:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:421:repair:2136e1e9f455"],
  "required_effects": [
    {"key": "synthetic-underscore-initialization", "value": "conditional-on-module-absence", "evaluator": "evidence"},
    {"key": "global-underscore-regression", "value": "asserts-unused-import-without-crash", "evaluator": "evidence"},
    {"key": "current-public-validation", "value": "passed", "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "existing-module-underscore", "value": "not-replaced-by-synthetic-binding", "evaluator": "evidence"},
    {"key": "unused-import-diagnostic", "value": "preserved", "evaluator": "evidence"},
    {"key": "no-module-underscore-doctests", "value": "preserved", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:c76d35c9a48e360887b3c443:locate",
      "after": "workflow:verified-history:c76d35c9a48e360887b3c443:guard",
      "reason": "Establish the module-scope lookup and source-less insertion before changing its condition.",
      "evidence_refs": ["PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix"]
    },
    {
      "before": "workflow:verified-history:c76d35c9a48e360887b3c443:locate",
      "after": "workflow:verified-history:c76d35c9a48e360887b3c443:regression",
      "reason": "Bind the current doctest test owner before adding the evidenced regression assertion.",
      "evidence_refs": ["PyCQA/pyflakes:421:regression"]
    },
    {
      "before": "workflow:verified-history:c76d35c9a48e360887b3c443:guard",
      "after": "workflow:verified-history:c76d35c9a48e360887b3c443:validate",
      "reason": "Observe the repaired initializer behavior after its modification.",
      "evidence_refs": ["PyCQA/pyflakes:421:fix", "PyCQA/pyflakes:421:body"]
    },
    {
      "before": "workflow:verified-history:c76d35c9a48e360887b3c443:regression",
      "after": "workflow:verified-history:c76d35c9a48e360887b3c443:validate",
      "reason": "Run the newly added public regression after it exists.",
      "evidence_refs": ["PyCQA/pyflakes:421:regression"]
    }
  ]
}
```
