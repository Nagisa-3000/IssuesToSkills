# Canonical historical Workflow

This Workflow represents the recorded repair mechanism and paired regression obligations. Inspection and validation cards describe how to establish applicability and check a current realization; they do not assert undocumented historical executions.

```arex-workflow-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968",
  "goal": "Remove an erroneous undefined-name diagnostic for an enclosing-class return annotation without admitting function-body-only names into annotation scope.",
  "mechanism": "When return annotations already receive enclosing-scope handling, omit them from subsequent function-scope child traversal while continuing to omit decorators.",
  "action_ids": [
    "workflow:verified-history:46d18832864f51ea6f6d3968:inspect",
    "workflow:verified-history:46d18832864f51ea6f6d3968:repair",
    "workflow:verified-history:46d18832864f51ea6f6d3968:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "required_effects": [
    {
      "key": "return-annotation-traversal-corrected",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "paired-regressions-present",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "public-validation-observed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "function-body-only-annotation-name-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "ordinary-function-body-checking-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "decorator-handling-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:46d18832864f51ea6f6d3968:inspect",
      "after": "workflow:verified-history:46d18832864f51ea6f6d3968:repair",
      "reason": "Confirm the reported scope distinction and locate the traversal owner before applying the recorded omission.",
      "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:fix"]
    },
    {
      "before": "workflow:verified-history:46d18832864f51ea6f6d3968:repair",
      "after": "workflow:verified-history:46d18832864f51ea6f6d3968:validate",
      "reason": "The traversal change must satisfy both regression assertions and retain adjacent checking after the edit.",
      "evidence_refs": ["PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"]
    }
  ]
}
```
