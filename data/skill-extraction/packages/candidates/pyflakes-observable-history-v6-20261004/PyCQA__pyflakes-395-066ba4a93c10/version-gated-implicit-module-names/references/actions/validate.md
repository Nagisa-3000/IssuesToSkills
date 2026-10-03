# Validate the candidate

Bind public commands to the current analyzer and test runner. Run the supported-version reproduction, guarded regression, and adjacent undefined-name tests. Review the unsupported-version registration boundary and loop branches; use executable boundary checks where the public checkout supports them. Missing runtime coverage must be reported, not converted to PASS.

```arex-contract-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8:validate",
  "intent": "Establish current repair behavior and retained adjacent compatibility.",
  "mechanism": "Public reproduction, guarded regression execution, and adjacent behavior checks after the edit.",
  "semantic_role": "validate-implicit-module-name",
  "owner_role": "undefined-name-regression-suite",
  "operation": "Execute current public oracle bindings and review capability boundaries; record fresh tri-state results without changing implementation or tests.",
  "kind": "validate",
  "inputs": [
    {
      "name": "repair-candidate",
      "semantic_role": "version-gated-module-name-repair",
      "artifact_kind": "source-and-tests",
      "language": "python",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "modified",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-report",
      "semantic_role": "module-name-validation-results",
      "artifact_kind": "test-report",
      "language": "text",
      "scope": "current-checkout",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "guarded-regression-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "public-validation-observed", "value": true, "evaluator": "evidence", "description": "Requires actual passing current public checks and reviewed adjacent assurances."},
    {"key": "diagnostic-observation-current", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-magic-global-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "version-dependent-loop-types-preserved", "value": true, "evaluator": "evidence"},
    {"key": "pre36-registration-boundary-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "validate-public-reproduction",
      "instruction": "Run the current analyzer on a module containing a: int = 2 followed by print(__annotations__) on a supported Python version. Require no undefined-name diagnostic for __annotations__.",
      "evidence_refs": ["PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "validate-guarded-and-adjacent-tests",
      "instruction": "Run the current public module-annotations regression and undefined-name test suite. Confirm the bare module-level name is accepted on supported versions, the regression skips unsupported versions, existing magic-global behavior remains intact, and version-dependent loop branches retain their prior semantics. Report unexecuted runtime coverage explicitly.",
      "evidence_refs": ["PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
      "kind": "repository_test",
      "command": []
    }
  ],
  "validation_for": ["workflow:verified-history:4817630500584ee0981edde8:repair"],
  "read_set": ["role:implicit-module-name-registry", "role:python-version-capability-policy", "role:undefined-name-regression-suite"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "evidence_refs": ["PyCQA/pyflakes:395:body", "PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:4817630500584ee0981edde8"
}
```

Empty command arrays are unbound historical guidance, not executable validation. A failed or unavailable oracle does not establish this Action's successful effects.
