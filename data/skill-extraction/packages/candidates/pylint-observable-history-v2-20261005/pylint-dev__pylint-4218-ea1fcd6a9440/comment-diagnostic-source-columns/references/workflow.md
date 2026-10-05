# Historical realization: source-anchored comment columns

The realization covers the report, implementation edit, and committed regression assertions of one repair. Probe and validation contracts are authored obligations grounded in those artifacts, not invented historical execution records.

```arex-workflow-v4
{
  "id": "workflow:verified-history:e90ff4df6c32dee9a7842f73",
  "goal": "Report comment-note diagnostics at the source position immediately after the comment hash while retaining note recognition and diagnostic content.",
  "mechanism": "Replace a note index local to the comment string with the comment token source-start column plus one, and update public coordinate assertions.",
  "action_ids": [
    "workflow:verified-history:e90ff4df6c32dee9a7842f73:probe",
    "workflow:verified-history:e90ff4df6c32dee9a7842f73:repair",
    "workflow:verified-history:e90ff4df6c32dee9a7842f73:validate"
  ],
  "source_ids": ["pylint-dev/pylint:4218:repair:ea1fcd6a9440"],
  "required_effects": [
    {"key": "source-anchor-applicability-established", "value": true, "evaluator": "evidence"},
    {"key": "comment-column-rule", "value": "token-source-start-plus-one", "evaluator": "evidence"},
    {"key": "public-column-expectations", "value": "source-anchored", "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "invariants": [
    {"key": "note-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "diagnostic-content-preserved", "value": true, "evaluator": "evidence"}
  ],
  "dependencies": [
    {
      "before": "workflow:verified-history:e90ff4df6c32dee9a7842f73:probe",
      "after": "workflow:verified-history:e90ff4df6c32dee9a7842f73:repair",
      "reason": "The report demonstrates differing source positions; the implementation establishes which coordinate owner and anchor realize the correction. Confirm those semantics in the current checkout before editing.",
      "evidence_refs": ["pylint-dev/pylint:4218:body", "pylint-dev/pylint:4218:fix"]
    },
    {
      "before": "workflow:verified-history:e90ff4df6c32dee9a7842f73:repair",
      "after": "workflow:verified-history:e90ff4df6c32dee9a7842f73:validate",
      "reason": "The implementation and expectation edits require fresh checks against source-anchored columns and unchanged diagnostic content.",
      "evidence_refs": ["pylint-dev/pylint:4218:fix", "pylint-dev/pylint:4218:regression"]
    }
  ]
}
```
