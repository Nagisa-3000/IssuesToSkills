# Validate target and adjacent behavior

Bind commands to the current public checkout. Run the minimal regression and applicable original reproduction, then neighboring undefined-variable and successful export checks. Review the narrow handler and retained sentinel path. Record actual diagnostics, fatal-error absence, failures, and skips.

```arex-contract-v4
{
  "id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8:validate",
  "intent": "Verify crash containment and preserved behavior after both edits.",
  "mechanism": "Public regression execution, adjacent tests, and narrow success-path review.",
  "semantic_role": "repair-verification",
  "owner_role": "export-regression-suite",
  "operation": "Execute current bound public regression commands and adjacent checks without modifying tracked files. Record outcomes and review the narrow handler, retained sentinel handling, and unchanged successful inference path.",
  "kind": "validate",
  "inputs": [],
  "outputs": [],
  "preconditions": [
    {"key": "owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "inference-failure-guard-installed", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertion-present", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"},
    {"key": "target-crash-absent", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "undefined-variable-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "successful-export-checks-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "target-and-neighbors",
      "instruction": "Execute the bound minimal regression and applicable original reproduction. Require undefined-variable without a fatal analyzer error. Run neighboring undefined-variable and valid list/tuple export checks and compare diagnostics. Inspect retained sentinel handling and the narrow exception boundary. Record skips as untested, not passed; refresh validation freshness only when required checks pass.",
      "evidence_refs": ["pylint-dev/pylint:8740:body", "pylint-dev/pylint:8740:fix", "pylint-dev/pylint:8740:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:8740:repair:331e48f74654"],
  "evidence_refs": ["pylint-dev/pylint:8740:fix", "pylint-dev/pylint:8740:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:9a3cbe2612faf6a1d7c341e8",
  "read_set": ["role:module-export-checker", "role:export-regression-suite"],
  "write_set": [],
  "validation_for": [
    "workflow:verified-history:9a3cbe2612faf6a1d7c341e8:guard",
    "workflow:verified-history:9a3cbe2612faf6a1d7c341e8:regression"
  ]
}
```

These effects describe required observations, not completed execution. Stop on failed required checks; do not convert missing coverage or skips into PASS.
