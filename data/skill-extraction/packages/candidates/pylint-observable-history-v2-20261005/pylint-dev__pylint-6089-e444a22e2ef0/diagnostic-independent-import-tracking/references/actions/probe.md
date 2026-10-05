# Probe configuration-sensitive analysis

Locate the current owner, compare restricted and default configurations, and trace the initializer references. Record anchored evidence explaining how the early return skips shared analysis needed by unused-import. A warning mismatch alone does not establish the mechanism.

This operation reads code and runs public probes without changing repository source or test definitions. Its mechanism-confirmed output is conditional on successful current observations, not guaranteed by invoking it.

```arex-contract-v4
{
  "id": "workflow:verified-history:29cee29cbd97c1547d1b57cd:probe",
  "intent": "Determine whether the current defect matches the supported mechanism.",
  "mechanism": "Compare diagnostic configurations and inspect gated shared reference analysis.",
  "semantic_role": "configuration-sensitive-analysis-diagnosis",
  "owner_role": "variable-use-analysis",
  "operation": "Read bound code and run bound public reproductions without repository edits; record anchors and explain the diagnostic-enable gate and affected class initializer references.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
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
  "preconditions": [
    {"key": "role:variable-use-analysis", "value": true, "evaluator": "symbol_exists"},
    {"key": "public-reproduction-available", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "shared-analysis-gate-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuinely-unused-import-detection", "value": "preserved", "evaluator": "evidence"},
    {"key": "enabled-variable-diagnostics", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-gated-use-analysis",
      "instruction": "Run bound public restricted/default reproductions and inspect anchored code. Confirm actually referenced imports, same-named class initializers, and an early return before shared analysis controlled by unrelated diagnostics. Record symptom and mechanism separately. Verify no repository source or test edits.",
      "evidence_refs": ["pylint-dev/pylint:6089:body", "pylint-dev/pylint:6089:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:variable-use-analysis", "role:restricted-import-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6089:repair:e444a22e2ef0"],
  "evidence_refs": ["pylint-dev/pylint:6089:title", "pylint-dev/pylint:6089:body", "pylint-dev/pylint:6089:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:29cee29cbd97c1547d1b57cd"
}
```
