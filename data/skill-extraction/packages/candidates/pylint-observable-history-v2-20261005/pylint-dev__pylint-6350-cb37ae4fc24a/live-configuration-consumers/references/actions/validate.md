# Validate public behavior and preservation

Bind all commands to the current public checkout. Run the added regression and relevant adjacent tests. Supplement incomplete coverage with public controls and construction probes.

The committed historical test asserted status zero with duplicate-code enabled, unused-import disabled, and ignore-imports enabled. The additional preservation checks here are prospective requirements, not claims of historical execution.

```arex-contract-v4
{
  "id": "workflow:verified-history:44cf4d12e6c9f03961fb6377:validate",
  "intent": "Observe corrected option behavior and preserved adjacent behavior after modification.",
  "mechanism": "Execute the public import-only regression and controls, then inspect affected construction and runtime paths.",
  "semantic_role": "configuration-repair-validation",
  "owner_role": "configuration-regression-suite",
  "operation": "Execute bound public checks without editing source or tests; capture outputs, statuses, and PASS, FAIL, or UNKNOWN observations for every assurance.",
  "kind": "validate",
  "inputs": [
    {
      "name": "edited-consumer",
      "semantic_role": "configuration-consumer",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "configuration-and-similarity",
      "phase": "validation",
      "state": "edited-with-regression",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-observations",
      "semantic_role": "configuration-validation",
      "artifact_kind": "public-check-record",
      "language": "python",
      "scope": "configuration-and-similarity",
      "phase": "acceptance",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "adjacent-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "standalone-option-semantics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "similarity-algorithm-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "public-import-regression",
      "instruction": "Run the bound public import-only regression. Capture output and exit status; require absence of duplicate-code with ignore-imports enabled and successful status when unrelated diagnostics are isolated.",
      "evidence_refs": ["pylint-dev/pylint:6350:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-behavior-controls",
      "instruction": "Run relevant public adjacent tests and controls. Verify eligible duplication is still detected, unused-import is independently governed, standalone defaults remain usable, and all migrated settings including the zero minimum-lines path remain coherent. Record uncovered assurances as UNKNOWN and failures as FAIL.",
      "evidence_refs": ["pylint-dev/pylint:6350:body", "pylint-dev/pylint:6350:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:44cf4d12e6c9f03961fb6377:repair"],
  "read_set": ["role:configuration-consumer", "role:configuration-regression-suite"],
  "write_set": [],
  "source_ids": ["pylint-dev/pylint:6350:repair:cb37ae4fc24a"],
  "evidence_refs": ["pylint-dev/pylint:6350:body", "pylint-dev/pylint:6350:fix", "pylint-dev/pylint:6350:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:44cf4d12e6c9f03961fb6377"
}
```

`public-validation-observed` means fresh observations exist, not that every check passed. A repair-success claim requires successful target checks and discharged preservation assurances. FAIL or UNKNOWN prevents unconditional acceptance.
