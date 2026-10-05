# Validate the target and adjacent behavior

Bind and render current public commands before running them. Inspect diagnostic output: a normal lint failure on invalid source is not necessarily a fatal analyzer failure.

Run the module-level declaration-plus-assignment reproduction and the bound regression suite. Compare existing nested nonlocal and ordinary assignment behavior to the pre-edit baseline. Record actual outcomes; do not mark validation observed on test definitions alone. If either code or assertions change again, repeat validation.

```arex-contract-v4
{
  "id": "workflow:verified-history:4e26a5bccbfef931bbba5ba0:validate",
  "intent": "Observe that the repair prevents the fatal root-scope failure without weakening diagnostics or adjacent scope behavior.",
  "mechanism": "Execute the public reproduction and diagnostic fixture checks against the modified checker.",
  "semantic_role": "scope-repair-validation",
  "owner_role": "scope-diagnostic-fixtures",
  "operation": "Execute currently bound public minimal reproduction and repository tests, inspect diagnostics, compare adjacent baseline, and record commands and results without further source edits.",
  "kind": "validate",
  "inputs": [
    {"name": "modified-checkout", "semantic_role": "scope-repair-checkout", "artifact_kind": "checkout", "language": "python", "scope": "assignment-checker-and-functional-fixtures", "phase": "post-edit", "state": "guard-and-regression-added", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "scope-repair-public-observations", "artifact_kind": "test-report", "language": "python", "scope": "assignment-checker-and-functional-fixtures", "phase": "verification", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "root-parent-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "assignment-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "root-scope-crash-prevented", "value": true, "evaluator": "evidence"},
    {"key": "invalid-nonlocal-diagnostic-retained", "value": true, "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "nested-nonlocal-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-assignment-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "root-scope-diagnostic",
      "instruction": "Run the currently bound module-level nonlocal-plus-assignment reproduction. Require the ordinary invalid-nonlocal diagnostic and no fatal analyzer diagnostic or missing-parent exception; interpret exit status together with output.",
      "evidence_refs": ["pylint-dev/pylint:8735:body", "pylint-dev/pylint:8735:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "scope-fixture-regressions",
      "instruction": "Run the currently bound public diagnostic fixture and adjacent nested nonlocal/ordinary assignment tests. Require matching target assertions and unchanged existing expectations; record any uncovered behavior as unknown.",
      "evidence_refs": ["pylint-dev/pylint:8735:regression", "pylint-dev/pylint:8735:fix"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:4e26a5bccbfef931bbba5ba0:guard"],
  "source_ids": ["pylint-dev/pylint:8735:repair:33d3f22b767e"],
  "evidence_refs": ["pylint-dev/pylint:8735:body", "pylint-dev/pylint:8735:fix", "pylint-dev/pylint:8735:regression"],
  "read_set": ["role:assignment-scope-checker", "role:scope-diagnostic-fixtures"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4e26a5bccbfef931bbba5ba0"
}
```
