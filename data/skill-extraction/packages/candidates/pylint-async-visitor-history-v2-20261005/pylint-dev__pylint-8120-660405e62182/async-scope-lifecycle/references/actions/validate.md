# Validate the correction and adjacent behavior

Bind and render current public argv commands before execution. Run the public checker suite and scope examples, comparing complete diagnostic outcomes rather than exit status alone. Inspect the final diff and lifecycle registrations.

Record actual command output, exit status, and semantic checks. PASS requires execution and matching observations; missing execution is UNKNOWN. Any subsequent edit makes the validation observation stale.

```arex-contract-v4
{
  "id": "workflow:verified-history:9a2315892fecfccf9d5c6c14:validate",
  "intent": "Observe corrected async isolation and preserved adjacent behavior after both edits.",
  "mechanism": "Execute public checker assertions and compare independent-scope and same-scope diagnostics.",
  "semantic_role": "validate-scope-isolation",
  "owner_role": "checker-public-validation",
  "operation": "Execute current-bound public checks and review the final diff without further tracked source modification.",
  "kind": "validate",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "async-lifecycle-parity", "value": true, "evaluator": "evidence"},
    {"key": "async-isolation-assertions-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-lifecycle-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "within-scope-diagnostics-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "run-checker-regressions",
      "instruction": "Execute the bound public suite; require no unexpected diagnostics in async isolation cases and unchanged positive within-scope expectations. Record output and exit status, and review retained synchronous/class/module lifecycle behavior.",
      "kind": "repository_test",
      "evidence_refs": ["pylint-dev/pylint:8120:fix", "pylint-dev/pylint:8120:regression"]
    },
    {
      "id": "compare-public-scope-cases",
      "instruction": "Execute separate async functions and methods and synchronous equivalents; require no cross-scope warning. Execute a supported incompatible same-scope reassignment and require its expected diagnostic.",
      "kind": "public_mre",
      "evidence_refs": ["pylint-dev/pylint:8120:body", "pylint-dev/pylint:8120:regression"]
    }
  ],
  "validation_for": [
    "workflow:verified-history:9a2315892fecfccf9d5c6c14:repair",
    "workflow:verified-history:9a2315892fecfccf9d5c6c14:regressions"
  ],
  "read_set": ["role:assignment-type-checker", "role:checker-regression-suite", "role:checker-public-validation"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:8120:repair:660405e62182"],
  "evidence_refs": ["pylint-dev/pylint:8120:body", "pylint-dev/pylint:8120:fix", "pylint-dev/pylint:8120:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:9a2315892fecfccf9d5c6c14"
}
```
