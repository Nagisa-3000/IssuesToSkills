# Inspect applicability and bind owners

Read current public code and run public reproductions without modifying implementation or tests. Determine whether the defect is immediate-scope lookup, singleton decorator recognition, or something else. Record real role bindings, anchors, outcomes, and baseline preservation behavior.

```arex-contract-v4
{
  "id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0:inspect",
  "intent": "Establish applicability and bind the repair to current semantic owners.",
  "mechanism": "Inspect scope lookup and decorator scanning at the unused-redefinition diagnostic gate.",
  "semantic_role": "recognition-applicability",
  "owner_role": "overload-recognition-and-redefinition-gate",
  "operation": "Read bound code and run public class-scope and multiple-decorator reproductions without editing files; record import identity, current anchors, applicability, and preservation baselines.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "recognition-context", "semantic_role": "bound-recognition-context", "artifact_kind": "inspection-record", "language": "Python", "scope": "current-public-checkout", "phase": "pre-edit", "state": "applicability-established", "optional": false}
  ],
  "preconditions": [],
  "effects": [
    {"key": "recognition-applicability-established", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-redefinition-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "first-binding-shadowing-preserved", "value": true, "evaluator": "evidence"},
    {"key": "existing-qualified-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "function-node-restriction-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "establish-current-mechanism",
      "instruction": "Inspect bound owners and execute public reproductions. Confirm typing.overload binding identity and at least one supported defect. Record ordinary redefinition, shadowing, qualified recognition, and function-node baseline behavior. Do not edit code.",
      "evidence_refs": ["PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:overload-recognition-and-redefinition-gate", "role:scope-stack-and-import-bindings", "role:type-annotation-regression-suite"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs": ["PyCQA/pyflakes:434:title", "PyCQA/pyflakes:434:body", "PyCQA/pyflakes:434:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:fc3525ab47a41bc94f54d0d0"
}
```

UNKNOWN owners or mechanisms do not produce the successful output state. A contrary mechanism rejects applicability. Read/probe operations do not change implementation or assertions; this is not a global unchanged-checkout invariant for the editing Workflow.
