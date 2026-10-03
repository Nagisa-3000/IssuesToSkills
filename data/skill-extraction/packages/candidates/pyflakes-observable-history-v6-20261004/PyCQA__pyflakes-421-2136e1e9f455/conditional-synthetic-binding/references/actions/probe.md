# Locate and diagnose the collision

Resolve the doctest scope initializer and binding insertion owner in the current checkout. Inspect where the module scope is retained and where the synthetic `_` is introduced. Determine whether collision handling accesses the synthetic binding's absent AST source.

Use a current public reproduction equivalent in mechanism to the original report. Do not edit the checkout during this operation. A reproduction need not use an unavailable dependency: the supplied regression demonstrates an import alias and a `pass` doctest. Keep the original report distinct from an adapted probe.

```arex-contract-v4
{
  "id": "workflow:verified-history:c76d35c9a48e360887b3c443:probe",
  "intent": "Determine whether the current failure matches synthetic underscore insertion into a doctest scope with an existing module underscore binding.",
  "mechanism": "Inspect scope ownership and source-less binding collision handling, then reproduce through public doctest analysis.",
  "semantic_role": "collision-diagnosis",
  "owner_role": "doctest-scope-initializer",
  "operation": "Read current code and run a public diagnostic probe without modifying tracked source or tests; record resolved owners and mechanism evidence.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "diagnosis",
      "semantic_role": "binding-collision-diagnosis",
      "artifact_kind": "diagnostic-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "collision-mechanism-confirmed", "value": true, "evaluator": "evidence"},
    {"key": "role:doctest-scope-initializer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:doctest-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "preserves": [
    {"key": "unused-module-import-diagnostic-preserved", "value": true, "evaluator": "evidence"},
    {"key": "absent-module-underscore-placeholder-preserved", "value": true, "evaluator": "evidence"},
    {"key": "adjacent-doctest-analysis-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "confirm-collision",
      "instruction": "Inspect current scope and insertion owners and run a public doctest-enabled reproduction. Confirm that an existing module underscore and unconditional source-less placeholder insertion cause the failure. This probe does not edit source or tests.",
      "evidence_refs": ["PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:421:repair:2136e1e9f455"],
  "evidence_refs": ["PyCQA/pyflakes:421:title", "PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix"],
  "read_set": ["role:doctest-scope-initializer", "role:binding-insertion-owner", "role:doctest-regression-tests"],
  "write_set": [],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:c76d35c9a48e360887b3c443"
}
```

The declared effects are successful-probe targets. If diagnosis is inconclusive, record UNKNOWN and do not emit a mechanism-confirmed PortValue.
