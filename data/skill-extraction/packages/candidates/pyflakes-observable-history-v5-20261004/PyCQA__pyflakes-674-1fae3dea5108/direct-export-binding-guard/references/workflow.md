# Historical Workflow: guard direct export assignment

Specialized binding construction must receive only the AST parent shapes it supports. The repair places the check in binding dispatch, preserving ordinary fallback for indirect targets.

```arex-workflow-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d",
  "goal": "Avoid internal errors for indirect export-name targets while retaining direct module-level export handling.",
  "mechanism": "Constrain specialized export-binding dispatch by immediate assignment-parent type and assert ordinary fallback behavior.",
  "action_ids": [
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:inspect",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
    "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "required_effects": [
    {"key": "indirect-target-special-export-binding", "value": false, "evaluator": "evidence"},
    {"key": "unpacking-regression-assertion-present", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "direct-module-export-processing", "value": "preserved", "evaluator": "evidence"},
    {"key": "ordinary-binding-fallback", "value": "preserved", "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:inspect",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
      "reason": "The parent assumption and fallback must be established before changing dispatch.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"]
    },
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:inspect",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
      "reason": "Bind the regression to the current analyzer and diagnostic test harness.",
      "evidence_refs": ["PyCQA/pyflakes:674:regression"]
    },
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:guard",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate",
      "reason": "Observe behavior after the dispatch modification.",
      "evidence_refs": ["PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"]
    },
    {
      "before": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:regression",
      "after": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:validate",
      "reason": "Execute the regression only after its assertion is present.",
      "evidence_refs": ["PyCQA/pyflakes:674:regression"]
    }
  ]
}
```

Inspection and validation are evidence-grounded reusable operations, not claims that particular historical commands were executed. The two modifying operations need not be ordered relative to each other; both precede final validation.
