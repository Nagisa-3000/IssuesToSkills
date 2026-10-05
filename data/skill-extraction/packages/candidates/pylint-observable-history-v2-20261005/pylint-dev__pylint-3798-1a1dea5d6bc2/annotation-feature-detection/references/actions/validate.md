# Validate the modifications and adjacent behavior

Bind and render public current commands before execution. Observe collection and per-case outcomes, not just exit status. Execute all four alias cases; compare unaliased and absent-feature behavior against current pinned-base expectations. Include an ordinary runtime undefined-name control.

The adjacent controls are current safety requirements. They are not additional historical committed assertions. Where feasible, test the new fixture against the pinned base in an isolated checkout to establish discrimination without overwriting current work.

Record failures and skips honestly. `public-validation-observed` means a report exists, not that the repair succeeded. `target-and-controls-passed` may be asserted only after all required checks actually pass. This operation does not edit tracked implementation or test assertions.

```arex-contract-v4
{
  "id": "workflow:verified-history:ca64407d3ccfea06d7171181:validate",
  "intent": "Observe corrected alias behavior and preserved adjacent diagnostics.",
  "mechanism": "Execute focused annotation assertions and discriminating public controls after the edits.",
  "semantic_role": "public-repair-validation",
  "owner_role": "annotation-regression-suite",
  "operation": "Run bound public commands, inspect collection and diagnostics, and record outcomes and refreshed anchors without changing tracked implementation or assertions.",
  "kind": "validate",
  "inputs": [],
  "outputs": [
    {"name": "validation", "semantic_role": "annotation-validation-result", "artifact_kind": "test-report", "language": "Python", "scope": "current-checkout", "phase": "post-edit", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "detector-edit-present", "value": true, "evaluator": "evidence"},
    {"key": "alias-regression-defined", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "target-and-controls-passed", "value": true, "evaluator": "evidence", "description": "Conditional success effect: assert only if all required target cases execute and all controls pass."}
  ],
  "preserves": [
    {"key": "unaliased-feature-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "feature-absent-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-name-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "annotation-and-adjacent-controls",
      "instruction": "Execute the four alias annotation cases and verify absence of spurious target diagnostics. Run unaliased, absent-feature and ordinary runtime-name controls against pinned-base expectations. Record commands, collection, skips, exit status and per-case outcomes. Missing target cases, skips or regressed controls prevent a success claim.",
      "evidence_refs": ["pylint-dev/pylint:3798:body", "pylint-dev/pylint:3798:fix", "pylint-dev/pylint:3798:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:ca64407d3ccfea06d7171181:repair",
    "workflow:verified-history:ca64407d3ccfea06d7171181:regression"
  ],
  "source_ids": ["pylint-dev/pylint:3798:repair:1a1dea5d6bc2"],
  "evidence_refs": ["pylint-dev/pylint:3798:fix", "pylint-dev/pylint:3798:regression"],
  "read_set": ["role:annotation-feature-detector", "role:module-feature-metadata", "role:annotation-regression-suite"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:ca64407d3ccfea06d7171181"
}
```
