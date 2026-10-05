# Historical realization

This realization describes one repair mechanism. Diagnosis and validation contracts are conditional current operations, not claims about steps historically executed.

```arex-workflow-v4
{
  "id": "workflow:verified-history:659f8bc8e03e7014a22a5caa",
  "goal": "Recognize individual exception names in supported documented lists without suppressing genuine missing-documentation warnings.",
  "mechanism": "Align multiple-type grammar recognition with exception-list extraction and verify public diagnostics.",
  "action_ids": [
    "workflow:verified-history:659f8bc8e03e7014a22a5caa:diagnose",
    "workflow:verified-history:659f8bc8e03e7014a22a5caa:repair",
    "workflow:verified-history:659f8bc8e03e7014a22a5caa:validate"
  ],
  "source_ids": ["pylint-dev/pylint:2729:repair:183dcc4cb134"],
  "required_effects": [
    {"key": "documented-list-members-recognized", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "singleton-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "genuine-missing-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-type-forms-preserved", "value": true, "evaluator": "evidence"},
    {"key": "google-description-handling-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:659f8bc8e03e7014a22a5caa:diagnose",
      "after": "workflow:verified-history:659f8bc8e03e7014a22a5caa:repair",
      "reason": "Confirm documentation recognition or extraction causes the warning before editing.",
      "evidence_refs": ["pylint-dev/pylint:2729:body", "pylint-dev/pylint:2729:fix"]
    },
    {
      "before": "workflow:verified-history:659f8bc8e03e7014a22a5caa:repair",
      "after": "workflow:verified-history:659f8bc8e03e7014a22a5caa:validate",
      "reason": "Grammar, collector, and regression edits require fresh post-edit checks.",
      "evidence_refs": ["pylint-dev/pylint:2729:fix", "pylint-dev/pylint:2729:regression"]
    }
  ]
}
```

Current ordering follows actual ports, bindings, prerequisites, and stale observations. A current DAG can drop an already-satisfied edit, but cannot drop validation of a performed edit. Invariants are evidence-backed behavior obligations, not facts established by matching names.
