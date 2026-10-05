# Validate the diagnostic distinction

Execute bound current public checks after associated edits. Record failures rather than weakening assertions. This operation does not edit tracked code.

```arex-contract-v4
{
  "id": "workflow:verified-history:00bdb5de0892c0cbbab00de9:validate",
  "package_id": "workflow:verified-history:00bdb5de0892c0cbbab00de9",
  "resource": "references/actions/validate.md",
  "kind": "validate",
  "intent": "Observe corrected parameter recognition and preservation of legitimate type and adjacent diagnostics.",
  "mechanism": "Run the exact-message mixed-entry regression and neighboring public documentation tests.",
  "semantic_role": "validate-optional-inline-types",
  "owner_role": "documentation-checker-tests",
  "operation": "Run current bound commands for the mixed-entry regression and neighboring tests. Record diagnostics, exit statuses, pinned revision and anchor hashes. Verify both described name-only entries are documented and only the unannotated argument lacks type documentation. Compare adjacent failures with the pinned baseline. Do not edit tracked files or infer whole-project acceptance.",
  "inputs": [
    {"name": "candidate", "semantic_role": "optional-type-repair", "artifact_kind": "checkout-change", "language": "python", "scope": "parameter-documentation-checker", "phase": "repair", "state": "edited-unvalidated", "optional": false}
  ],
  "outputs": [
    {"name": "validation", "semantic_role": "optional-type-validation", "artifact_kind": "test-report", "language": "python", "scope": "parameter-documentation-checker", "phase": "validation", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "mixed-regression-authored", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "legitimate-type-diagnostics", "value": "preserved", "evaluator": "evidence"},
    {"key": "adjacent-docstring-behavior", "value": "preserved", "evaluator": "evidence"}
  ],
  "validation_for": ["workflow:verified-history:00bdb5de0892c0cbbab00de9:repair"],
  "oracle": [
    {
      "id": "mixed-entry-diagnostics",
      "instruction": "Execute the bound current mixed-entry test. Require exactly missing-type-doc for the unannotated description-only argument and no missing-param-doc for either described name-only argument.",
      "evidence_refs": ["pylint-dev/pylint:5222:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-docstring-tests",
      "instruction": "Execute bound public neighboring tests for explicit NumPy types, starred arguments and other supported styles. Compare failures with the pinned baseline, retain unexplained failures, and report scope without claiming whole-project correctness.",
      "evidence_refs": ["pylint-dev/pylint:5222:fix", "pylint-dev/pylint:5222:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "read_set": ["role:numpy-parameter-parser", "role:parameter-documentation-checker", "role:documentation-checker-tests"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:5222:repair:1d3a7ff32b0f"],
  "evidence_refs": ["pylint-dev/pylint:5222:fix", "pylint-dev/pylint:5222:regression"]
}
```

Record PASS, FAIL, or UNKNOWN for each bound semantic check. Merely running a command does not make its assertions PASS. Further edits stale the validation observation and require reruns.
