# Canonical historical Workflow

The repair extends the existing branch-alternative mechanism to match-case bodies and adds a focused no-diagnostic regression. Inspection and validation are reusable operations derived from the supplied report and repair, not claims that particular historical commands were run.

```arex-workflow-v4
{
  "id": "workflow:verified-history:45a56eede77a20492da56a49",
  "goal": "Avoid unused-name redefinition false positives between mutually exclusive match-case bodies.",
  "mechanism": "Expose each match-case body as an alternative through the existing branch classifier, guarded for Python AST availability.",
  "action_ids": [
    "workflow:verified-history:45a56eede77a20492da56a49:inspect",
    "workflow:verified-history:45a56eede77a20492da56a49:repair",
    "workflow:verified-history:45a56eede77a20492da56a49:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:771:repair:f2671ffe1785"],
  "required_effects": [
    {
      "key": "match-case-alternatives-recognized",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "public-regression-validated",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "existing-if-and-try-alternatives-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "legitimate-redefinition-diagnostics-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:45a56eede77a20492da56a49:inspect",
      "after": "workflow:verified-history:45a56eede77a20492da56a49:repair",
      "reason": "Confirm that the public false positive is attributable to the alternative-branch owner before changing it.",
      "evidence_refs": ["PyCQA/pyflakes:771:body", "PyCQA/pyflakes:771:fix"]
    },
    {
      "before": "workflow:verified-history:45a56eede77a20492da56a49:repair",
      "after": "workflow:verified-history:45a56eede77a20492da56a49:validate",
      "reason": "The new match classification and added regression require validation after modification.",
      "evidence_refs": ["PyCQA/pyflakes:771:fix", "PyCQA/pyflakes:771:regression"]
    }
  ]
}
```
