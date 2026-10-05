# Validate both edits and adjacent behavior

Resolve the current public runner and bind commands before execution. Compare observed diagnostics as well as exit status. Exercise the target, inverse-direction boundary, supported same-receiver uses, unequal-name controls, and established adjacent expectations.

If feasible, verify that the positive regression detects the original defect on an isolated pre-edit control. This is a current check, not a historical execution claim. The later qualification environment and commands do not automatically bind to the current checkout.

Only passing, current checks establish the intended validation effect. Failures and unavailable checks must remain FAIL or UNKNOWN.

```arex-contract-v4
{
  "id": "workflow:verified-history:8486fdf9c04144c10d14213f:validate",
  "intent": "Observe correctness of both modifications and preservation of adjacent diagnostics.",
  "mechanism": "Execute public positive/negative regression boundaries and established private-member checks against the edited checker.",
  "semantic_role": "public-validation",
  "owner_role": "public-check-runner",
  "operation": "Render and execute current public Oracle commands, recording actual diagnostics, exit status, code anchors, and tri-state results without editing source or expectations to hide failures.",
  "kind": "validate",
  "inputs": [
    {"name": "matcher-change", "semantic_role": "directional-private-member-matcher", "artifact_kind": "source-change", "language": "Python", "scope": "current-private-member-checker", "phase": "repair", "state": "edited"},
    {"name": "regression-change", "semantic_role": "directional-private-member-regressions", "artifact_kind": "test-change", "language": "Python", "scope": "current-private-member-checker", "phase": "repair", "state": "edited"}
  ],
  "outputs": [
    {"name": "validation-report", "semantic_role": "directional-private-member-validation", "artifact_kind": "test-report", "language": "Python", "scope": "current-private-member-checker", "phase": "validation", "state": "observed"}
  ],
  "preconditions": [
    {"key": "directional-matcher-installed", "value": true, "evaluator": "evidence"},
    {"key": "directional-regressions-present", "value": true, "evaluator": "evidence"},
    {"key": "role:public-check-runner", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "attribute-name-equality-required", "value": true, "evaluator": "evidence"},
    {"key": "instance-write-not-used-by-class-read", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-private-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-directional-regressions",
      "instruction": "Run current bound public checks. Require no unused warning for cls-write/self-read, recognized cls-to-cls and self-to-self uses, unequal names not counted as use, retained unused warning for self-write with only cls-read, retained undefined-variable for unbound cls, and unchanged established adjacent expectations. Record failures and unavailable checks explicitly.",
      "evidence_refs": ["pylint-dev/pylint:4657:fix", "pylint-dev/pylint:4657:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:8486fdf9c04144c10d14213f:edit-matcher",
    "workflow:verified-history:8486fdf9c04144c10d14213f:edit-regressions"
  ],
  "read_set": ["role:private-member-use-matcher", "role:private-member-regression-suite", "role:public-check-runner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4657:repair:c02682670e0d"],
  "evidence_refs": ["pylint-dev/pylint:4657:fix", "pylint-dev/pylint:4657:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:8486fdf9c04144c10d14213f"
}
```
