# Validate target and adjacent behavior

Bind and render current public commands. Execute the chained receiver through the current analyzer harness and compare adjacent diagnostic expectations. Distinguish ordinary lint diagnostics from fatal analyzer failures.

Validate bare-name usage, accepted simple receivers, genuinely unused members in ordinary simple-receiver cases, and argument exclusion. If existing cases do not cover an assurance, add a current public probe before claiming it.

```arex-contract-v4
{
  "id": "workflow:verified-history:4244f18e715c9b86c7cef8e0:validate",
  "intent": "Verify crash removal and preservation against the edited snapshot.",
  "mechanism": "Exercise the public regression and compare adjacent diagnostic expectations through the current harness.",
  "semantic_role": "private-scan-public-validation",
  "owner_role": "private-usage-regressions",
  "operation": "Render current public oracle bindings, execute target and adjacent checks, review the limited diff, and record snapshot-linked outcomes without changing source.",
  "kind": "validate",
  "inputs": [
    {"name": "edited-snapshot", "semantic_role": "guarded-private-scan-and-regression", "artifact_kind": "source-snapshot", "language": "python", "scope": "private-member-analysis", "phase": "repair", "state": "guard-and-regression-present", "optional": false}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "private-scan-public-validation-evidence", "artifact_kind": "test-report", "language": "python", "scope": "private-member-analysis", "phase": "validation", "state": "public-checks-observed", "optional": false}
  ],
  "preconditions": [
    {"key": "guard-and-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-passed", "value": true, "evaluator": "evidence", "description": "Establish only after actual target and preservation checks pass on the recorded snapshot."}
  ],
  "preserves": [
    {"key": "simple-receiver-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "argument-exclusion-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-unused-emission-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "chained-receiver-regression",
      "instruction": "Run the public chained-receiver fixture through the bound current analyzer harness. Verify no fatal AttributeError and no unexpected unused-private-member warning. Record actual diagnostics and exit status.",
      "evidence_refs": ["pylint-dev/pylint:5261:body", "pylint-dev/pylint:5261:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-private-diagnostics",
      "instruction": "Execute public cases for bare-name usage, self/cls/class-name receivers, ordinary unused members, and argument exclusion. Compare baseline expectations and review the limited diff. Reject unexplained diagnostic changes.",
      "evidence_refs": ["pylint-dev/pylint:5261:fix", "pylint-dev/pylint:5261:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:4244f18e715c9b86c7cef8e0:repair"],
  "source_ids": ["pylint-dev/pylint:5261:repair:0a1ebd488fcd"],
  "evidence_refs": ["pylint-dev/pylint:5261:fix", "pylint-dev/pylint:5261:regression"],
  "read_set": ["role:private-usage-scan", "role:private-usage-regressions"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4244f18e715c9b86c7cef8e0"
}
```

Record failed reports, but do not establish the passing effect after FAIL or UNKNOWN. Later source edits require refreshed observations.
