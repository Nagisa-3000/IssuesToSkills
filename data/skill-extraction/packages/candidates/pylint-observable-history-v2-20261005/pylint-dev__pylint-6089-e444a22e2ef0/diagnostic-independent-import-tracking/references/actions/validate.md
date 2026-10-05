# Validate target and adjacent behavior

Bind and render current public reproduction and repository-test commands. Observe diagnostics explicitly; empty output or an exit code alone is insufficient. Run restricted and default configurations, genuine-unused controls, and enabled-variable-diagnostic controls.

Record commands, exit statuses, output, candidate anchors, and tri-state results. Infrastructure failure is UNKNOWN; behavioral failure is FAIL. Do not assert successful validation until all required checks pass. This operation does not modify repository source or test definitions.

```arex-contract-v4
{
  "id": "workflow:verified-history:29cee29cbd97c1547d1b57cd:validate",
  "intent": "Observe corrected import-use behavior and preservation of adjacent diagnostics.",
  "mechanism": "Execute current public initializer regressions and relevant variable/import controls.",
  "semantic_role": "diagnostic-independent-analysis-validation",
  "owner_role": "restricted-import-regression-suite",
  "operation": "Run bound public reproductions and repository tests against the candidate without source edits; record target and preservation checks and disclose unrun coverage.",
  "kind": "validate",
  "inputs": [
    {
      "name": "candidate",
      "semantic_role": "diagnostic-independent-analysis-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "variable-use-analysis-and-regressions",
      "phase": "post-repair",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation",
      "semantic_role": "diagnostic-independent-analysis-validation",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "variable-use-analysis-and-regressions",
      "phase": "post-repair",
      "state": "checks-observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "restricted-class-import-regression", "value": "covered", "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuinely-unused-import-detection", "value": "preserved", "evaluator": "evidence"},
    {"key": "enabled-variable-diagnostics", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "verify-public-import-configurations",
      "instruction": "Run bound public restricted/default reproductions. Require no false unused-import warning for either initializer and require a genuine-unused control to remain reportable. Capture expected and observed diagnostics explicitly, not process exit alone.",
      "evidence_refs": ["pylint-dev/pylint:6089:body", "pylint-dev/pylint:6089:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "verify-adjacent-variable-import-tests",
      "instruction": "Run the bound restricted-message regression and relevant existing import/variable tests. Check enabled undefined-variable and used-before-assignment controls and neighboring import-use cases. Record failures and unrun coverage explicitly; assert successful validation only when required checks pass.",
      "evidence_refs": ["pylint-dev/pylint:6089:fix", "pylint-dev/pylint:6089:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:29cee29cbd97c1547d1b57cd:repair"],
  "read_set": ["role:variable-use-analysis", "role:restricted-import-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6089:repair:e444a22e2ef0"],
  "evidence_refs": ["pylint-dev/pylint:6089:body", "pylint-dev/pylint:6089:fix", "pylint-dev/pylint:6089:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:29cee29cbd97c1547d1b57cd"
}
```
