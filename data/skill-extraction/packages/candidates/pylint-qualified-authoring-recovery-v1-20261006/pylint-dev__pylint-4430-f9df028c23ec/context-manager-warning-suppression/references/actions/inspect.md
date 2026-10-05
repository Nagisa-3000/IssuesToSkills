# Inspect diagnostic ownership and frame semantics

Read current public code without changing source or fixtures. Locate both emission paths, safe-inference filters, immediate-frame API, resolved-decorator helper, and regression runner. Compare managed and ordinary allocation/acquisition probes. Observe module and nested-function frames directly rather than inferring ownership from textual ancestry.

```arex-contract-v4
{
  "id": "workflow:verified-history:b74613551e6d8c24ed7692fa:inspect",
  "intent": "Establish applicability and bind current semantic owners.",
  "mechanism": "Trace resource-advice emission and probe immediate AST frames and resolved decorators.",
  "semantic_role": "diagnostic-binding",
  "owner_role": "resource-advice-emitter",
  "operation": "Read public owners and reproduce managed and ordinary cases without editing source or fixtures; record bindings, code anchors, and current Oracle commands.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "diagnostic-binding", "semantic_role": "diagnostic-binding", "artifact_kind": "owner-binding-report", "language": "Python", "scope": "resource-advice-checker", "phase": "pre-edit", "state": "observed", "optional": false}
  ],
  "preconditions": [
    {"key": "role:resource-advice-emitter", "value": true, "evaluator": "symbol_exists"},
    {"key": "public-base-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "emission-paths-and-frames-observed", "value": true, "evaluator": "evidence"},
    {"key": "managed-frame-false-positive-reproduced", "value": true, "evaluator": "evidence"},
    {"key": "resolved-decorator-identity-supported", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-resource-advice-preserved", "value": true, "evaluator": "evidence"},
    {"key": "resource-inference-filter-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-with-silence-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-frame-cases",
      "instruction": "Record managed-frame warnings and ordinary controls; identify both emission paths, immediate-frame behavior, and resolved decorator identity. Confirm no source or fixture modifications. If reproduction or identity is unknown, do not report the corresponding effect as observed.",
      "evidence_refs": ["pylint-dev/pylint:4430:body", "pylint-dev/pylint:4430:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["pylint-dev/pylint:4430:repair:f9df028c23ec"],
  "evidence_refs": ["pylint-dev/pylint:4430:body", "pylint-dev/pylint:4430:fix"],
  "read_set": ["role:resource-advice-emitter", "role:ast-frame-classifier", "role:diagnostic-regression-suite"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:b74613551e6d8c24ed7692fa"
}
```

Effects are intended successful-probe outcomes, not existing observations. Unknown owners permit public discovery only. Bind a current command before executing the Oracle.
