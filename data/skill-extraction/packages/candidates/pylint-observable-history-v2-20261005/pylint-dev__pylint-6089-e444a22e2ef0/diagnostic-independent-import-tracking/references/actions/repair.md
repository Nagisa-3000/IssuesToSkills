# Repair the gate and regression

Edit only the bound analysis and regression owners. Remove the early return that skips shared definition/scope analysis because unrelated diagnostics are disabled. Remove the cached used-before-assignment enablement flag only if it becomes unused. Keep needed caches and emission controls.

Add restricted-message coverage using resolvable standard-library imports and both call-wrapped and direct same-named class initializer references. Preserve existing neighboring controls. Do not suppress unused-import globally or rename attributes to bypass the trigger.

This combined modifying Action produces a candidate, not observed runtime success. Its validation Action must remain in the execution closure.

```arex-contract-v4
{
  "id": "workflow:verified-history:29cee29cbd97c1547d1b57cd:repair",
  "intent": "Restore shared import-use analysis and protect the triggering initializer forms.",
  "mechanism": "Remove the unrelated-diagnostic early return and add same-named initializer regression coverage.",
  "semantic_role": "diagnostic-independent-analysis-repair",
  "owner_role": "variable-use-analysis",
  "operation": "Edit bound analysis and regression owners to continue shared definition/statement/frame processing with unrelated diagnostics disabled; remove only obsolete enablement state and add restricted-message initializer cases.",
  "kind": "edit",
  "inputs": [
    {
      "name": "diagnosis",
      "semantic_role": "configuration-sensitive-analysis-diagnosis",
      "artifact_kind": "evidence-record",
      "language": "python",
      "scope": "variable-use-analysis",
      "phase": "pre-repair",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
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
  "preconditions": [
    {"key": "shared-analysis-gate-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:variable-use-analysis", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:restricted-import-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "shared-import-use-analysis", "value": "independent-of-unrelated-diagnostic-enablement", "evaluator": "evidence"},
    {"key": "restricted-class-import-regression", "value": "covered", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuinely-unused-import-detection", "value": "preserved", "evaluator": "evidence"},
    {"key": "enabled-variable-diagnostics", "value": "preserved", "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-analysis-and-regression-diff",
      "instruction": "Review the current diff. Shared analysis must not exit solely because both unrelated diagnostics are disabled. Needed emission controls must remain. Check any removed cache has no remaining references. Verify restricted-message regression coverage contains call-wrapped and direct imported references with same-named class attributes and retains existing controls. Diff review is not runtime acceptance.",
      "evidence_refs": ["pylint-dev/pylint:6089:fix", "pylint-dev/pylint:6089:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:variable-use-analysis", "role:restricted-import-regression-suite"],
  "write_set": ["role:variable-use-analysis", "role:restricted-import-regression-suite"],
  "source_ids": ["pylint-dev/pylint:6089:repair:e444a22e2ef0"],
  "evidence_refs": ["pylint-dev/pylint:6089:fix", "pylint-dev/pylint:6089:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:29cee29cbd97c1547d1b57cd"
}
```
