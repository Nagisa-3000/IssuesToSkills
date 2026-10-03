# Inspect premature target binding

Locate current owners and read the visitor and test harness without editing them. Bind public probes comparing fresh-scope `x = x` and `x: int = x`. Trace whether handling the target introduces the binding before initializer analysis.

Existence predicates below use boolean values and role-qualified keys. A located symbol is not sufficient proof of the mechanism: current review and probe evidence must establish that separately.

Emit a mechanism-confirmed output only on confirmation. If the mechanism is absent or remains unknown, do not authorize editing.

```arex-contract-v4
{
  "id": "workflow:verified-history:88cc33218756cccdf2ac071b:inspect",
  "intent": "Establish whether premature target binding suppresses an undefined-name diagnostic.",
  "mechanism": "Compare ordinary and annotated assignment probes and trace the annotated-assignment visitor.",
  "semantic_role": "mechanism-inspection",
  "owner_role": "annotated-assignment-analyzer",
  "operation": "Read the bound Python visitor and public regression harness; run bound public reproductions without modifying source or tests.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspection",
      "semantic_role": "binding-order-inspection",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "annotated-assignment",
      "phase": "pre-edit",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [
    {
      "key": "role:annotated-assignment-analyzer",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "The current annotated-assignment visitor has been located and bound to this semantic owner."
    }
  ],
  "effects": [
    {
      "key": "early-target-binding-confirmed",
      "value": true,
      "evaluator": "evidence",
      "description": "Established only by current tracing and public probes demonstrating the reported mechanism."
    }
  ],
  "preserves": [
    {
      "key": "ordinary-assignment-diagnostics-preserved",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "annotation-and-initializer-dispatch-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "confirm-ordering",
      "instruction": "Record current owner anchors and visitor order. In fresh scopes compare ordinary and annotated self-initializer diagnostics. Confirm that target handling binds before initializer analysis. Record FAIL or UNKNOWN rather than manufacturing a confirmed output. Do not edit source or tests.",
      "evidence_refs": [
        "PyCQA/pyflakes:728:body",
        "PyCQA/pyflakes:728:fix"
      ],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": [
    "role:annotated-assignment-analyzer",
    "role:annotation-regression-suite"
  ],
  "write_set": [],
  "source_ids": [
    "PyCQA/pyflakes:728:repair:4dcd92e45efe"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:728:body",
    "PyCQA/pyflakes:728:fix"
  ],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:88cc33218756cccdf2ac071b"
}
```
