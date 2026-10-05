# Validate routing

Bind and render current public commands. Run the early-effect regression and relevant existing tests. Probe canonical spellings, supported abbreviations, competitors, required values, supported equals/separate forms, and unmatched forwarding.

The historical assertion expects verbose stderr from `Run(["--ve"])`, even though the invocation raises `SystemExit`. Exit status alone is not the oracle. Record actual observations only. Subsequent edits make validation stale and require rerunning the closure.

```arex-contract-v4
{
  "id": "workflow:verified-history:1013e5aeb1e4479ac812713d:validate-routing",
  "intent": "Observe the corrected early effect and preserved adjacent routing.",
  "mechanism": "Execute an isolated public regression and relevant neighboring CLI/configuration checks.",
  "semantic_role": "routing-validation",
  "owner_role": "early-option-regressions",
  "operation": "Execute bound current public checks and record commands, outputs, and exit statuses without changing tracked implementation files.",
  "kind": "validate",
  "inputs": [
    {"name": "routing-patch", "semantic_role": "early-routing-repair", "artifact_kind": "source-and-test-patch", "language": "python", "scope": "current-cli-option-pipeline", "phase": "post-edit", "state": "awaiting-validation"}
  ],
  "outputs": [
    {"name": "validation-report", "semantic_role": "routing-validation", "artifact_kind": "test-observation-report", "language": "python", "scope": "current-cli-option-pipeline", "phase": "post-validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "early-effect-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:early-option-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "routing-probe-results-current", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "canonical-option-behavior", "value": "preserved", "evaluator": "evidence"},
    {"key": "neighbor-option-routing", "value": "preserved", "evaluator": "evidence"},
    {"key": "argument-consumption-and-forwarding", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "execute-early-effect-regression",
      "instruction": "Run the bound isolated regression and inspect its observable early effect rather than relying on parsing success or exit status alone.",
      "evidence_refs": ["pylint-dev/pylint:6810:regression", "pylint-dev/pylint:6810:body"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "execute-adjacent-routing-checks",
      "instruction": "Run bound relevant existing tests and public checks for canonical spellings, competitors, value consumption, supported value forms, and unmatched forwarding; any regression blocks acceptance.",
      "evidence_refs": ["pylint-dev/pylint:6810:fix", "pylint-dev/pylint:6810:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6810:repair:44a3d96e1af9"],
  "evidence_refs": ["pylint-dev/pylint:6810:fix", "pylint-dev/pylint:6810:regression"],
  "resource": "references/actions/validate-routing.md",
  "package_id": "workflow:verified-history:1013e5aeb1e4479ac812713d",
  "read_set": ["role:early-option-router", "role:main-option-parser", "role:early-option-regressions"],
  "write_set": [],
  "validation_for": ["workflow:verified-history:1013e5aeb1e4479ac812713d:align-routing"]
}
```
