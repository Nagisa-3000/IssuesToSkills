# Historical Workflow: delayed annotated-assignment target binding

This Workflow abstracts the supplied report, merged implementation, and regression assertion. The inspection and validation Actions describe public reconstruction checks; their presence does not assert that those checks were historically executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b",
  "goal": "Restore undefined-name reporting for an annotated assignment initializer that references its unbound target.",
  "mechanism": "Analyze the annotation and initializer before visiting the target that installs the assignment binding; lock the behavior with an undefined-name regression assertion.",
  "action_ids": [
    "workflow:verified-history:88cc33218756cccdf2ac071b:inspect",
    "workflow:verified-history:88cc33218756cccdf2ac071b:reorder",
    "workflow:verified-history:88cc33218756cccdf2ac071b:regression",
    "workflow:verified-history:88cc33218756cccdf2ac071b:validate"
  ],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "required_effects": [
    {
      "key": "initializer-analyzed-before-new-target-binding",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "undefined-self-reference-regression-present",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "target-and-adjacent-checks-pass",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "annotation-processing-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "initializer-special-branches-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "adjacent-annotation-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:88cc33218756cccdf2ac071b:inspect",
      "after": "workflow:verified-history:88cc33218756cccdf2ac071b:reorder",
      "reason": "Confirm that premature target binding explains the reported annotated-assignment diagnostic asymmetry before changing traversal.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:body",
        "PyCQA/pyflakes:728:fix"
      ]
    },
    {
      "before": "workflow:verified-history:88cc33218756cccdf2ac071b:inspect",
      "after": "workflow:verified-history:88cc33218756cccdf2ac071b:regression",
      "reason": "Locate the relevant regression owner and reproduce the exact undefined-name case.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:body",
        "PyCQA/pyflakes:728:regression"
      ]
    },
    {
      "before": "workflow:verified-history:88cc33218756cccdf2ac071b:reorder",
      "after": "workflow:verified-history:88cc33218756cccdf2ac071b:validate",
      "reason": "The corrected traversal must be checked after the implementation edit.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:fix",
        "PyCQA/pyflakes:728:regression"
      ]
    },
    {
      "before": "workflow:verified-history:88cc33218756cccdf2ac071b:regression",
      "after": "workflow:verified-history:88cc33218756cccdf2ac071b:validate",
      "reason": "Validation must execute the newly added regression assertion.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:regression"
      ]
    }
  ]
}
```

The implementation edit and regression edit have no evidenced mandatory order relative to one another. Both must precede final validation.
