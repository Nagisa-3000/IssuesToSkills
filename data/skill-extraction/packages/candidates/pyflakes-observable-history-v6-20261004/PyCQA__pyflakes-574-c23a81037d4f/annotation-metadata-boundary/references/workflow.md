# Canonical Workflow

This Workflow captures the implementation mechanism and its public regression obligations. Inspection is an authored current applicability prerequisite, not a claim of a recorded historical investigation sequence.

```arex-workflow-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6",
  "goal": "Prevent Annotated metadata from being parsed as forward types while retaining type diagnostics.",
  "mechanism": "Partition multi-argument Annotated traversal into an inherited type context and a scoped non-annotation metadata context.",
  "action_ids": [
    "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:inspect",
    "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
    "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:validate"
  ],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "required_effects": [
    {"key": "metadata-traversal-context", "value": "non-annotation", "evaluator": "evidence"},
    {"key": "target-and-preservation-checks-pass", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "type-reference-checking-preserved", "value": true, "evaluator": "evidence"},
    {"key": "enclosing-annotation-state-preserved", "value": true, "evaluator": "evidence"},
    {"key": "literal-handling-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-expression-checking-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:inspect",
      "after": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
      "reason": "Bind the current visitor and scoped annotation context before changing traversal.",
      "evidence_refs": ["PyCQA/pyflakes:574:fix"]
    },
    {
      "before": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair",
      "after": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:validate",
      "reason": "Observe target behavior and retained diagnostics after source and regression changes.",
      "evidence_refs": ["PyCQA/pyflakes:574:regression"]
    }
  ]
}
```

Current ordering follows ports, prerequisites, verification obligations, and semantic dependencies, not merely this list. Already-satisfied operations may be omitted from a current task DAG only with current evidence. An already-correct checkout requires binding its existing source-and-tests artifact to validation; inspection's review-record output cannot substitute for that artifact. Such a reduced DAG does not alter the historical Workflow.
