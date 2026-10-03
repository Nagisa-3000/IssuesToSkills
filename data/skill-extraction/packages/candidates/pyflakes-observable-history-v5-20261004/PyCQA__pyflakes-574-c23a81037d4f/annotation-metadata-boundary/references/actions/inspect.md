# Inspect the annotation boundary

Locate current semantic owners for Python subscript analysis, annotation-state control, and annotation regression tests. Record real bindings and hashed anchors. Inspect how string nodes become forward annotations and how nested contexts and state restoration work.

Reproduce the public analyzer symptom and inspect AST slice shapes for supported runtimes. Do not confuse analyzer diagnostics with runtime evaluation of `Annotated`.

The output is an observation artifact, not proof of compatibility or repair. An absent symptom may indicate an already corrected boundary or a different cause.

```arex-contract-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:inspect",
  "intent": "Establish current applicability and owner bindings for the annotation boundary.",
  "mechanism": "Read semantic owners and probe the public reproduction and AST representation.",
  "semantic_role": "boundary-inspection",
  "owner_role": "python-annotation-subscript-analysis",
  "operation": "Locate traversal, state-control and test owners; record current bindings and observations.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "boundary-context",
      "semantic_role": "annotation-boundary-context",
      "artifact_kind": "code-and-probe-record",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "inspected",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-python-analyzer-checkout", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "boundary-owner-bindings-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "observe-boundary",
      "instruction": "Record the public diagnostic, supported slice shapes, recognition semantics, annotation-state behavior and hashed owner anchors. Determine whether metadata is incorrectly interpreted as a type.",
      "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "evidence_refs": ["PyCQA/pyflakes:574:title", "PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6",
  "read_set": [
    "role:python-annotation-subscript-analysis",
    "role:python-annotation-state-controller",
    "role:python-annotation-regression-suite"
  ],
  "write_set": []
}
```

Keep unresolved semantics UNKNOWN. An inspected port may contain unresolved observations; it does not itself satisfy the repair's evidence predicates.
