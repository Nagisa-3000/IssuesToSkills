# Validate continuation and preserved behavior

Bind and render commands for the current public checkout before execution. No historical pytest selection automatically authorizes a current command.

Exercise the actual configuration/reporting path, not only a loader unit test. Observe a diagnostic containing plugin identity and exception information, no unhandled missing-module startup traceback, and continued ordinary source analysis. Verify early statistics, missing-file context, and default template handling.

Run public regression and adjacent checks for valid plugins, duplicate suppression, configuration hooks, normal/default/custom text reporting, and exceptions outside `ModuleNotFoundError`. A configuration error may still yield a nonzero diagnostic exit status.

Record commands, results, failures, and skips. UNKNOWN or skipped checks are not PASS. These current requirements are authored validation definitions, not claims about historical test execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:855459481b02863b85df5b59:validate",
  "intent": "Observe recovery and preserved adjacent behavior using current public checks.",
  "mechanism": "Exercise configuration diagnostics and ordinary analysis after the coupled lifecycle repair.",
  "semantic_role": "recovery-validation",
  "owner_role": "regression-suite",
  "operation": "Execute bound public reproductions and repository tests, recording configuration output, continuation, early reporting, valid plugins, and unrelated exception propagation.",
  "kind": "validate",
  "inputs": [
    {"name": "repair-candidate", "semantic_role": "plugin-recovery-candidate", "artifact_kind": "checkout", "language": "Python", "scope": "current-checkout", "phase": "startup", "state": "modified", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "plugin-recovery-validation", "artifact_kind": "test-record", "language": "Python", "scope": "current-checkout", "phase": "startup", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "Set only after actual execution and recorded results; failed assurances reject acceptance."}
  ],
  "preserves": [
    {"key": "ordinary-analysis-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "valid-plugin-lifecycle-preserved", "value": true, "evaluator": "evidence"},
    {"key": "unrelated-exception-propagation-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "configuration-and-continuation",
      "instruction": "Run the current public absent-plugin reproduction through configuration and reporting. Observe a plugin-specific configuration error with useful exception information, no unhandled startup traceback, and the ordinary source diagnostic.",
      "evidence_refs": ["pylint-dev/pylint:4555:body", "pylint-dev/pylint:4555:fix", "pylint-dev/pylint:4555:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "adjacent-lifecycle-and-reporting",
      "instruction": "Run current public regression and adjacent checks for valid plugins, duplicate suppression, optional hooks, early reporter state, default and custom templates, normal diagnostics, and unrelated exceptions. Record failures and skips explicitly.",
      "evidence_refs": ["pylint-dev/pylint:4555:fix", "pylint-dev/pylint:4555:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4555:repair:cbd3cc07515e"],
  "evidence_refs": ["pylint-dev/pylint:4555:body", "pylint-dev/pylint:4555:fix", "pylint-dev/pylint:4555:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:855459481b02863b85df5b59",
  "validation_for": ["workflow:verified-history:855459481b02863b85df5b59:repair"],
  "read_set": ["role:plugin-startup", "role:plugin-configuration", "role:diagnostic-handler", "role:text-reporter", "role:regression-suite"],
  "write_set": []
}
```
