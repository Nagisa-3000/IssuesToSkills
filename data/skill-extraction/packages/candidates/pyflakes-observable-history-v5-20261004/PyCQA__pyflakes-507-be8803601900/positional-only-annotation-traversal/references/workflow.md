# Historical repair Workflow

This Workflow captures the supplied repair's mechanism and the verification obligations needed for current reuse. The Action order expresses semantic dependencies, not a historical execution transcript.

```arex-workflow-v4
{
  "id": "workflow:verified-history:b95b785d6a29c4b04e9050af",
  "goal": "Avoid an unused-import false positive when an imported name is used in a positional-only parameter annotation.",
  "mechanism": "Include positional-only parameter names and annotations in the existing function-signature collection pipeline, guarded for runtimes that expose the AST field, and protect the behavior with a version-aware regression.",
  "action_ids": [
    "workflow:verified-history:b95b785d6a29c4b04e9050af:inspect",
    "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
    "workflow:verified-history:b95b785d6a29c4b04e9050af:validate"
  ],
  "source_ids": [
    "PyCQA/pyflakes:507:repair:be8803601900"
  ],
  "required_effects": [
    {
      "key": "positional-only-annotations-collected",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "annotation-only-import-not-reported-unused",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "focused-regression-present",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "ordinary-and-keyword-only-collection-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "supported-runtime-compatibility-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "existing-defaults-and-binding-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:b95b785d6a29c4b04e9050af:inspect",
      "after": "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
      "reason": "Locate the current collector and establish omission of the positional-only AST category before applying the evidenced change.",
      "evidence_refs": [
        "PyCQA/pyflakes:507:body",
        "PyCQA/pyflakes:507:fix"
      ]
    },
    {
      "before": "workflow:verified-history:b95b785d6a29c4b04e9050af:repair",
      "after": "workflow:verified-history:b95b785d6a29c4b04e9050af:validate",
      "reason": "Validate the modified collector and the newly added regression, including runtime gating and adjacent annotation behavior.",
      "evidence_refs": [
        "PyCQA/pyflakes:507:fix",
        "PyCQA/pyflakes:507:regression"
      ]
    }
  ]
}
```
