# Validate the target and adjacent diagnostics

Bind current public commands for the reproduction and repository tests. Execute them and retain outputs, selection, exit status, and code anchors. Ensure test selection is nonempty. Verify both the absence of the target false positive and continued reporting of genuine exception-variable uses outside their handler.

The historical added case uses `ValueError`, a direct `if e` filter, and an in-handler `print(e)`. The preceding annotated outside-handler `print(e)` supplies the adjacent behavior boundary. Additional tests may increase current assurance but are not new historical support.

```arex-contract-v4
{
  "id": "workflow:verified-history:afcebec8041ecae4f0debb6d:validate",
  "intent": "Observe target correction and preservation of nearby assignment diagnostics after the edit.",
  "mechanism": "Run the public collision regression and retained exception-scope controls against the patched checkout.",
  "semantic_role": "scope-repair-validation",
  "owner_role": "assignment-diagnostic-regressions",
  "operation": "Execute current bound reproduction and diagnostic regression commands without editing tracked artifacts; record fresh target and adjacent behavior observations.",
  "kind": "validate",
  "inputs": [
    {"name": "patched-scope-case", "semantic_role": "scope-repair-artifacts", "artifact_kind": "public-code-and-tests", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "patched-unvalidated", "optional": false}
  ],
  "outputs": [
    {"name": "scope-validation-record", "semantic_role": "scope-validation-evidence", "artifact_kind": "public-test-observations", "language": "python", "scope": "current-checkout", "phase": "post-validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "direct-filter-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "collision-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "direct-filter-collision-diagnostic", "value": "absent", "evaluator": "evidence"},
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-exception-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-candidate-filter-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-collision",
      "instruction": "Run the bound public reproduction and verify that the direct comprehension filter name produces no used-before-assignment diagnostic despite the same-spelling handler binding.",
      "evidence_refs": ["pylint-dev/pylint:5817:body", "pylint-dev/pylint:5817:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-scope-controls",
      "instruction": "Run the current public regression selection, including the collision and genuine outside-handler use. Require nonempty selection, correct expected diagnostics and successful repository-test completion; review that ordinary filtering remains active outside the direct-filter case.",
      "evidence_refs": ["pylint-dev/pylint:5817:fix", "pylint-dev/pylint:5817:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:afcebec8041ecae4f0debb6d:repair"],
  "source_ids": ["pylint-dev/pylint:5817:repair:67055f422132"],
  "evidence_refs": ["pylint-dev/pylint:5817:body", "pylint-dev/pylint:5817:fix", "pylint-dev/pylint:5817:regression"],
  "read_set": ["role:assignment-candidate-filter", "role:assignment-diagnostic-regressions"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:afcebec8041ecae4f0debb6d"
}
```

A failure or unknown test result cannot satisfy the declared validation effects. Empty command arrays require current binding before execution; they are not runnable historical commands.
