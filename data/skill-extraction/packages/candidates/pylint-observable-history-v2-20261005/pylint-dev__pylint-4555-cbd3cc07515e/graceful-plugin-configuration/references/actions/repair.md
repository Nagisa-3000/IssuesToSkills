# Repair missing-module recovery and early diagnostics

Apply only when current semantic review establishes compatibility and the role bindings below resolve.

Retain configured names even when loading fails. In the evidenced two-phase lifecycle, contain `ModuleNotFoundError` during loading/registration so startup advances. During configuration loading/hooks, report the error with plugin identity and exception information.

Support diagnostics before ordinary file initialization: initialize needed statistics when absent, use configuration context if no file path exists, and make a default text template available early. Preserve valid plugin registration, duplicate suppression, optional hooks, normal diagnostics, and custom-template behavior.

Add public regression coverage combining a missing configured module with an ordinary source diagnostic. Add current checks for configuration-error output and early reporting; the historical committed fixture directly asserted only continuation.

Do not broaden catching to `Exception`. Historically the `try` blocks also enclosed registration and configuration hooks. Stop if current requirements need a distinct missing-dependency classification mechanism; do not silently invent one.

Effects below describe expected candidate behavior, not observed execution. The separate validate Action must establish behavioral success.

```arex-contract-v4
{
  "id": "workflow:verified-history:855459481b02863b85df5b59:repair",
  "intent": "Replace a missing-plugin startup crash with a configuration diagnostic and continued analysis.",
  "mechanism": "Defer missing-module reporting to configuration and support diagnostics before normal per-file initialization.",
  "semantic_role": "missing-plugin-recovery",
  "owner_role": "plugin-startup",
  "operation": "Edit bound plugin startup, configuration, diagnostic definitions and handler, text reporter, and public regression owners as a coupled repair.",
  "kind": "edit",
  "inputs": [
    {"name": "lifecycle-review", "semantic_role": "plugin-lifecycle-review", "artifact_kind": "review-record", "language": "Python", "scope": "current-checkout", "phase": "startup", "state": "observed", "optional": false}
  ],
  "outputs": [
    {"name": "repair-candidate", "semantic_role": "plugin-recovery-candidate", "artifact_kind": "checkout", "language": "Python", "scope": "current-checkout", "phase": "startup", "state": "modified", "optional": false}
  ],
  "preconditions": [
    {"key": "current-lifecycle-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "missing-module-mechanism-compatible", "value": true, "evaluator": "evidence"},
    {"key": "role:plugin-startup", "value": true, "evaluator": "symbol_exists", "description": "Resolve the plugin startup owner to current hashed symbol anchors."},
    {"key": "role:plugin-configuration", "value": true, "evaluator": "symbol_exists", "description": "Resolve the configuration-hook owner to current hashed symbol anchors."},
    {"key": "role:diagnostic-handler", "value": true, "evaluator": "symbol_exists", "description": "Resolve diagnostic definitions and emission state to current symbols."},
    {"key": "role:text-reporter", "value": true, "evaluator": "symbol_exists", "description": "Resolve current text reporter initialization and formatting symbols."},
    {"key": "role:regression-suite", "value": true, "evaluator": "file_exists", "description": "Resolve the current public regression resources; historical paths are not bindings."}
  ],
  "effects": [
    {"key": "missing-plugin-diagnostic-and-continuation", "value": true, "evaluator": "evidence", "description": "Expected candidate behavior; requires subsequent execution."},
    {"key": "early-reporting-supported", "value": true, "evaluator": "evidence", "description": "Expected statistics, configuration-path, and default-template behavior."}
  ],
  "preserves": [
    {"key": "ordinary-analysis-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "valid-plugin-lifecycle-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-exception-propagation-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-coupled-change",
      "instruction": "Review the current diff for retained plugin identity, precise ModuleNotFoundError boundaries, configuration diagnostics, safe early message state, default template readiness, and public continuation coverage. Do not infer execution success from review.",
      "evidence_refs": ["pylint-dev/pylint:4555:fix", "pylint-dev/pylint:4555:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4555:repair:cbd3cc07515e"],
  "evidence_refs": ["pylint-dev/pylint:4555:fix", "pylint-dev/pylint:4555:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:855459481b02863b85df5b59",
  "read_set": ["role:plugin-startup", "role:plugin-configuration", "role:diagnostic-handler", "role:text-reporter", "role:regression-suite"],
  "write_set": ["role:plugin-startup", "role:plugin-configuration", "role:diagnostic-handler", "role:text-reporter", "role:regression-suite"],
  "invalidates": ["public-validation-observed"],
  "exclusions": [
    {"key": "recovery-requires-broad-exception-catching", "value": true, "evaluator": "evidence"},
    {"key": "current-policy-requires-fail-fast", "value": true, "evaluator": "evidence"}
  ]
}
```
