# Validate final state

Execute current publicly bound checks and review the final dispatch. A target fixture alone does not prove that every eligibility guard is preserved.

```arex-contract-v4
{
  "id": "workflow:verified-history:b980c9ec644c821d41e50e10:validate",
  "intent": "Observe corrected alias naming and preserved adjacent behavior after edits.",
  "mechanism": "Execute public naming regressions and reproduction controls, then inspect final guarded dispatch.",
  "semantic_role": "verify-repair",
  "owner_role": "naming-regression-suite",
  "operation": "Bind and run current public fixture and reproduction checks; review category, current diagnostic locations, ordinary-variable fallback, and eligibility guards without source edits.",
  "kind": "validate",
  "inputs": [],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "local-alias-validation",
      "artifact_kind": "test-and-review-record",
      "language": "python",
      "scope": "function-local-naming",
      "phase": "post-edit",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "explicit-local-alias-routing", "value": "typealias", "evaluator": "evidence"},
    {"key": "local-alias-controls-present", "value": true, "evaluator": "evidence"},
    {"key": "role:naming-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-variable-routing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "scope-guards-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-alias-policy-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-regression-assertions-retained", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-alias-diagnostics",
      "instruction": "Execute bound current public naming tests and reproduction. Require alias-category invalid-name for the bad explicit local alias and no new naming diagnostic for good simple and union-valued aliases or the ordinary union-annotated control. Check retained top-level expectations and inspect unchanged membership, argument-exclusion, import-redefinition guards and variable fallback. Record failures and skips.",
      "evidence_refs": ["pylint-dev/pylint:8536:body", "pylint-dev/pylint:8536:fix", "pylint-dev/pylint:8536:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": [
    "workflow:verified-history:b980c9ec644c821d41e50e10:route",
    "workflow:verified-history:b980c9ec644c821d41e50e10:regression"
  ],
  "source_ids": ["pylint-dev/pylint:8536:repair:b63c8a1c148e"],
  "evidence_refs": ["pylint-dev/pylint:8536:body", "pylint-dev/pylint:8536:fix", "pylint-dev/pylint:8536:regression"],
  "read_set": ["role:local-name-classifier", "role:naming-regression-suite"],
  "write_set": [],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:b980c9ec644c821d41e50e10"
}
```

Empty source argv arrays require explicit current binding. Render actual bound commands before execution. Set the validation effect only after required checks pass; required skips and UNKNOWN do not count. Any subsequent implementation or fixture edit makes the observation stale.
