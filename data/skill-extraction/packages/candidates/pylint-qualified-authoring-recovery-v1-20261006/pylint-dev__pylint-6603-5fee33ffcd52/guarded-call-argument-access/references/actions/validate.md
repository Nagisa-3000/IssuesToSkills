# Validate analyzer robustness and neighboring diagnostics

Bind commands to the current public harness. Run the empty-call analysis and the targeted checker tests, including existing valid-call cases. Capture exit status, analyzer messages, and test results; inspect failures rather than accepting a command's existence as evidence.

```arex-contract-v4
{
  "id": "workflow:verified-history:fd4221a31ba02747212c0c88:validate",
  "intent": "Observe that both edits prevent the crash without changing adjacent checker behavior.",
  "mechanism": "Analyze the public empty-call reproduction and run the checker regression with adjacent diagnostic assertions.",
  "semantic_role": "validate-guarded-analysis",
  "owner_role": "checker-regression-fixture",
  "operation": "Execute current public analyzer and repository-test bindings; record results and refresh stale validation observations. Do not modify tracked source or tests.",
  "kind": "validate",
  "inputs": [
    {"name": "guard-edit", "semantic_role": "guarded-eligibility-code", "artifact_kind": "source-change", "language": "python", "scope": "current-checker", "phase": "repair", "state": "edited", "optional": false},
    {"name": "regression-edit", "semantic_role": "empty-call-analysis-fixture", "artifact_kind": "test-change", "language": "python", "scope": "current-checker", "phase": "repair", "state": "edited", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "guarded-analysis-validation", "artifact_kind": "test-result", "language": "python", "scope": "current-checker", "phase": "verification", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "empty-call-access-guarded", "value": true, "evaluator": "evidence"},
    {"key": "empty-call-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "valid-call-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "runtime-call-validity-unchanged", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "empty-call-no-analyzer-crash",
      "instruction": "Analyze the public empty-call loop with the targeted checker enabled. Require no IndexError or fatal analysis failure from first-argument access. Ordinary diagnostics do not imply runtime validity and may make a linter's process exit nonzero.",
      "evidence_refs": ["pylint-dev/pylint:6603:body", "pylint-dev/pylint:6603:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "target-and-adjacent-regressions",
      "instruction": "Run the current repository harness for the empty-call fixture and existing adjacent valid-call assertions. Require passing test results and unchanged expected diagnostics for eligible nonempty calls. Record the actual command and results; do not infer whole-project correctness.",
      "evidence_refs": ["pylint-dev/pylint:6603:fix", "pylint-dev/pylint:6603:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:fd4221a31ba02747212c0c88:guard",
    "workflow:verified-history:fd4221a31ba02747212c0c88:regression"
  ],
  "read_set": ["role:call-eligibility-checker", "role:checker-regression-fixture"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6603:repair:5fee33ffcd52"],
  "evidence_refs": ["pylint-dev/pylint:6603:body", "pylint-dev/pylint:6603:fix", "pylint-dev/pylint:6603:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:fd4221a31ba02747212c0c88"
}
```

Observed failure or unavailable execution blocks a success claim. This contract has not itself been executed by source qualification.
