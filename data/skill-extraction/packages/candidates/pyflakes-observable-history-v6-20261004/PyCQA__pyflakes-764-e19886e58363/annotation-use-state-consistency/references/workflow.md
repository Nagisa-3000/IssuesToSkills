# Canonical Workflow

This Workflow reconstructs the narrow repair mechanism supported by the report, merged assignment change, and regression assertion. Action order expresses semantic prerequisites, not an inferred historical command log.

```arex-workflow-v4
{
  "id": "workflow:verified-history:a9020121b14a346d4f659c0e",
  "goal": "Prevent a boolean-subscript crash in annotation usage tracking while retaining undefined-name and unused-local diagnostics.",
  "mechanism": "Use scope-and-node metadata for the annotation-only load's usage state so a later scope-sensitive store can consume the same representation.",
  "action_ids": [
    "workflow:verified-history:a9020121b14a346d4f659c0e:inspect",
    "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
    "workflow:verified-history:a9020121b14a346d4f659c0e:validate"
  ],
  "source_ids": [
    "PyCQA/pyflakes:764:repair:e19886e58363"
  ],
  "required_effects": [
    {
      "key": "annotation-usage-metadata",
      "value": "scope-and-load-node",
      "evaluator": "evidence"
    },
    {
      "key": "target-public-validation-observed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "invariants": [
    {
      "key": "annotation-only-load-undefined-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "nested-unused-local-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "adjacent-annotation-branch-behavior-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:a9020121b14a346d4f659c0e:inspect",
      "after": "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
      "reason": "Confirm the producer's boolean assignment and the consumer's structured usage-state contract before modifying their semantic owner.",
      "evidence_refs": [
        "PyCQA/pyflakes:764:body",
        "PyCQA/pyflakes:764:fix"
      ]
    },
    {
      "before": "workflow:verified-history:a9020121b14a346d4f659c0e:repair",
      "after": "workflow:verified-history:a9020121b14a346d4f659c0e:validate",
      "reason": "The changed metadata and regression assertion require fresh public checks of the reproducer and neighboring annotation behavior.",
      "evidence_refs": [
        "PyCQA/pyflakes:764:fix",
        "PyCQA/pyflakes:764:regression"
      ]
    }
  ]
}
```

Already satisfied inspection may be omitted from a current execution DAG only when its prerequisites and output facts are present as current evidence. Validation remains attached to any retained modification. All packaged Actions are covered by this canonical Workflow.
