# Align matching and add a regression

After policy and boundaries are established, add per-option matching metadata and dispatch through the canonical matched entry. A zero threshold denotes exact matching; nonzero thresholds count hyphens. Derive thresholds from current competitors, not the historical table.

Preserve existing value splitting, separate value consumption, and unmatched forwarding. Avoid a blanket prefix rule. The historical prefix-threshold implementation does not reject every string sharing a recognized prefix.

Add a public regression observing the early side effect. The historical realization uses isolated verbose stderr, not merely parsing success. Plugin-specific checks are current proposals, not historical committed coverage.

```arex-contract-v4
{
  "id": "workflow:verified-history:1013e5aeb1e4479ac812713d:align-routing",
  "intent": "Route supported abbreviations through the intended early callbacks without stealing neighboring options.",
  "mechanism": "Introduce collision-aware matching thresholds, canonical dispatch, and an isolated early-effect regression.",
  "semantic_role": "early-routing-repair",
  "owner_role": "early-option-router",
  "operation": "Edit the bound early registry and matcher and add a public regression at the bound test owner while preserving existing argument handling.",
  "kind": "edit",
  "inputs": [
    {"name": "routing-analysis", "semantic_role": "routing-policy-analysis", "artifact_kind": "evidence-report", "language": "python", "scope": "current-cli-option-pipeline", "phase": "pre-edit", "state": "reviewed"}
  ],
  "outputs": [
    {"name": "routing-patch", "semantic_role": "early-routing-repair", "artifact_kind": "source-and-test-patch", "language": "python", "scope": "current-cli-option-pipeline", "phase": "post-edit", "state": "awaiting-validation"}
  ],
  "preconditions": [
    {"key": "routing-policy-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "supported-abbreviation-bypasses-early-handler", "value": true, "evaluator": "evidence"},
    {"key": "current-prefix-boundaries-established", "value": true, "evaluator": "evidence"},
    {"key": "role:early-option-router", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:early-option-regressions", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "early-abbreviation-routing", "value": "aligned-with-established-policy", "evaluator": "evidence"},
    {"key": "early-effect-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "canonical-option-behavior", "value": "preserved", "evaluator": "evidence"},
    {"key": "neighbor-option-routing", "value": "preserved", "evaluator": "evidence"},
    {"key": "argument-consumption-and-forwarding", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-canonical-dispatch",
      "instruction": "Review the current diff against established boundaries: resolve callbacks and argument-taking metadata through canonical entries, preserve forwarding and consumption, and ensure the regression asserts an early effect.",
      "evidence_refs": ["pylint-dev/pylint:6810:fix", "pylint-dev/pylint:6810:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:6810:repair:44a3d96e1af9"],
  "evidence_refs": ["pylint-dev/pylint:6810:fix", "pylint-dev/pylint:6810:regression"],
  "resource": "references/actions/align-routing.md",
  "package_id": "workflow:verified-history:1013e5aeb1e4479ac812713d",
  "read_set": ["role:early-option-router", "role:main-option-parser", "role:early-option-regressions"],
  "write_set": ["role:early-option-router", "role:early-option-regressions"],
  "invalidates": ["public-validation-observed", "routing-probe-results-current"],
  "exclusions": [
    {"key": "prefix-collision-unresolved", "value": true, "evaluator": "evidence"},
    {"key": "downstream-abbreviation-policy", "value": "exact-only", "evaluator": "evidence"}
  ]
}
```
