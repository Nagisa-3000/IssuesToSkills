# Validate corrected and preserved diagnostics

Execute current bound public commands, not historical replay commands. Compare diagnostic content as well as test outcomes: legitimate diagnostics can affect a linter's exit code.

Observe both generator positives and both negative controls. Run neighboring homonym and late-binding checks where available and review the retained paths. Missing coverage remains UNKNOWN.

```arex-contract-v4
{
  "id": "workflow:verified-history:2d9cfc7283460de886b0b9d6:validate",
  "intent": "Observe correction of the false diagnostic and preservation of adjacent scope behavior.",
  "mechanism": "Execute positive and negative public diagnostic assertions and relevant neighboring scope checks.",
  "semantic_role": "scope-repair-validation",
  "owner_role": "scope-regression-suite",
  "operation": "Run the current bound public reproduction and diagnostic suite, compare diagnostics with expected results, inspect preserved scope paths and record PASS, FAIL or UNKNOWN for required assurances without editing tracked source.",
  "kind": "validate",
  "inputs": [
    {"name": "scope-patch", "semantic_role": "decorator-scope-repair", "artifact_kind": "patch", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "unvalidated", "optional": false}
  ],
  "outputs": [
    {"name": "validation-record", "semantic_role": "decorator-scope-validation", "artifact_kind": "test-observation", "language": "python", "scope": "current-checkout", "phase": "post-edit", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "diagnostic-boundary-assertions-added", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-undefined-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "nondecorator-homonym-protection-preserved", "value": true, "evaluator": "evidence"},
    {"key": "late-binding-check-path-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "diagnostic-boundaries",
      "instruction": "Render and execute current public commands. Verify no undefined x for either bound generator form on a function with parameter x; retain undefined x for a separate decorator(x), and undefined y in x*x*y for x in range(3). Run the applicable public suite and neighboring scope checks, review retained homonym and late-binding paths, and record incomplete assurance coverage as UNKNOWN.",
      "evidence_refs": ["pylint-dev/pylint:3791:body", "pylint-dev/pylint:3791:fix", "pylint-dev/pylint:3791:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:3791:repair:a054796d7008"],
  "evidence_refs": ["pylint-dev/pylint:3791:fix", "pylint-dev/pylint:3791:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:2d9cfc7283460de886b0b9d6",
  "validation_for": ["workflow:verified-history:2d9cfc7283460de886b0b9d6:repair"],
  "read_set": ["role:name-resolution-checker", "role:scope-regression-suite"],
  "write_set": []
}
```
