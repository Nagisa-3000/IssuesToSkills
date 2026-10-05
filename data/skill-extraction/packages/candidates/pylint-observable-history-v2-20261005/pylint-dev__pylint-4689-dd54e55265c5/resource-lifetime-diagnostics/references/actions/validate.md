# Validate diagnostic boundaries

Bind and run public current commands; historical fixture names do not authorize execution in a different checkout. Test diagnostics without requiring the linter's fixture programs to execute their resource allocations.

```arex-contract-v4
{
  "id": "workflow:verified-history:d5bff35cdcd2562bddc778f8:validate",
  "intent": "Observe repaired boundaries and preservation behavior after modification.",
  "mechanism": "Execute paired negative and positive diagnostic cases plus adjacent public checks.",
  "semantic_role": "diagnostic-lifecycle-validation",
  "owner_role": "resource-regression-owner",
  "operation": "Run current bound public regression commands and inspect actual diagnostic sets. Record exit codes, expected versus actual messages, scope-state behavior, and preservation results. Do not change source or expected outputs to conceal failures.",
  "kind": "validate",
  "inputs": [
    {
      "name": "lifecycle-patch",
      "semantic_role": "resource-diagnostic-lifecycle-change",
      "artifact_kind": "patch",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "unvalidated"
    }
  ],
  "outputs": [
    {
      "name": "lifecycle-validation",
      "semantic_role": "resource-diagnostic-validation-observation",
      "artifact_kind": "test-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "post-edit",
      "state": "observed"
    }
  ],
  "preconditions": [
    {"key": "public-lifecycle-assertions-added", "value": true, "evaluator": "evidence"},
    {"key": "current-validation-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "unmanaged-resource-warnings-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-context-exemptions-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-refactoring-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-lifecycle-boundaries",
      "instruction": "Execute current public tests showing no target message for persistent ThreadPoolExecutor and ProcessPoolExecutor, assigned pools later used in with, global pools used in a nested function, and consumed tuple elements. Require target messages for unused tuple elements and ordinary unmanaged recognized resources. Check overwrite and checker state reset using current public probes.",
      "evidence_refs": ["pylint-dev/pylint:4689:regression", "pylint-dev/pylint:4689:fix"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "verify-preservation",
      "instruction": "Execute current public checks for direct-with and context-manager-owned resources, automatic-release exemptions, and neighboring refactoring messages affected by shared visitors. Record failures or UNKNOWN results; do not claim whole-project coverage from these checks.",
      "evidence_refs": ["pylint-dev/pylint:4689:fix", "pylint-dev/pylint:4689:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:d5bff35cdcd2562bddc778f8:repair"],
  "read_set": ["role:resource-diagnostic-owner", "role:resource-regression-owner"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:4689:repair:dd54e55265c5"],
  "evidence_refs": ["pylint-dev/pylint:4689:fix", "pylint-dev/pylint:4689:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:d5bff35cdcd2562bddc778f8"
}
```

PASS requires observed diagnostic agreement and preservation results, not merely a successful test collection. Validation is an authored requirement, not an assertion of historical execution. Any subsequent edit makes `public-validation-observed` stale and requires rerunning relevant checks.
