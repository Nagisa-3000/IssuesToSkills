# Repair the registry and add the guarded regression

Modify the bound implicit module-name registry to include `__annotations__` only when the current compatible capability policy supports Python 3.6 annotations. Add a guarded module-level regression expecting no undefined-name warning.

The historical implementation introduced `PY36_PLUS` and appended to `_MAGIC_GLOBALS` conditionally. It also changed a negative pre-3.5 flag into `PY35_PLUS`, retaining loop type behavior. Do not mechanically rename current flags: reuse equivalent capability checks where available.

```arex-contract-v4
{
  "id": "workflow:verified-history:4817630500584ee0981edde8:repair",
  "intent": "Correct supported-version module-name recognition and encode the policy in a guarded regression.",
  "mechanism": "Version-gated registration in the implicit module-name owner plus a module-scope undefined-name test.",
  "semantic_role": "repair-implicit-module-name",
  "owner_role": "implicit-module-name-registry",
  "operation": "Edit the bound registry and capability policy as necessary; add a regression for bare module-level __annotations__ skipped on unsupported versions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "reviewed-policy",
      "semantic_role": "module-name-policy-diagnosis",
      "artifact_kind": "review-record",
      "language": "text",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "reviewed",
      "optional": false
    }
  ],
  "outputs": [
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
  "preconditions": [
    {"key": "compatible-policy-reviewed", "value": true, "evaluator": "evidence"},
    {"key": "owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:implicit-module-name-registry", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:python-version-capability-policy", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:undefined-name-regression-suite", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "supported-module-annotations-recognition", "value": true, "evaluator": "evidence", "description": "Expected repair effect, requiring current validation."},
    {"key": "guarded-regression-present", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-magic-global-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "version-dependent-loop-types-preserved", "value": true, "evaluator": "evidence"},
    {"key": "pre36-registration-boundary-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed", "diagnostic-observation-current"],
  "oracle": [
    {
      "id": "review-gated-diff",
      "instruction": "Review the current diff for conditional module-name registration, a Python-3.6 capability boundary, a guarded regression, unchanged existing magic globals, and equivalent loop-type branches. This review does not substitute for the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:implicit-module-name-registry", "role:python-version-capability-policy", "role:undefined-name-regression-suite"],
  "write_set": ["role:implicit-module-name-registry", "role:python-version-capability-policy", "role:undefined-name-regression-suite"],
  "source_ids": ["PyCQA/pyflakes:395:repair:066ba4a93c10"],
  "evidence_refs": ["PyCQA/pyflakes:395:fix", "PyCQA/pyflakes:395:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:4817630500584ee0981edde8"
}
```

No new builtin, unconditional registration, or unrelated scope special case is authorized. Effects describe the candidate's intended behavior until independently observed.
