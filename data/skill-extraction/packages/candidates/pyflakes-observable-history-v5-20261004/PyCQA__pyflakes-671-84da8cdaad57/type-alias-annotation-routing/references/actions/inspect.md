# Inspect TypeAlias initializer routing

Locate the semantic owners in the current checkout. Review the annotated-assignment handler's target, annotation, and value branches, the typing-aware marker recognizer, and the annotation path's treatment of quoted type expressions.

Run a bound public reproduction using a quoted explicit alias. Compare it with the supplied quoted-function-annotation example. Record diagnostics and current symbol bindings; do not infer applicability from the name `TypeAlias` alone.

The output is a current routing assessment, not a repaired implementation. If the failure is absent or the annotation path cannot resolve quoted expressions, report that boundary rather than inventing an adapter.

```arex-contract-v4
{
  "id": "workflow:verified-history:d3771ee821e88935b9bcf1ce:inspect",
  "intent": "Establish whether an explicit TypeAlias initializer is being processed as an ordinary value.",
  "mechanism": "Compare a public quoted-alias reproduction with current annotated-assignment dispatch and existing annotation handling.",
  "semantic_role": "routing-assessment",
  "owner_role": "annotated-assignment-dispatch",
  "operation": "Locate current owners, inspect their routing, and observe public reproductions.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "routing-assessment",
      "semantic_role": "type-alias-routing-assessment",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "current-routing-assessed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "checkout-content",
      "value": "unchanged",
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "observe-alias-mismatch",
      "instruction": "Bind and run a current public reproduction of a quoted explicit alias; record whether its imported type is falsely unused, compare quoted function annotations, and review the marker and routing owners.",
      "evidence_refs": [
        "PyCQA/pyflakes:671:body",
        "PyCQA/pyflakes:671:fix"
      ],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": [
    "PyCQA/pyflakes:671:repair:84da8cdaad57"
  ],
  "evidence_refs": [
    "PyCQA/pyflakes:671:title",
    "PyCQA/pyflakes:671:body",
    "PyCQA/pyflakes:671:fix"
  ],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:d3771ee821e88935b9bcf1ce",
  "read_set": [
    "role:annotated-assignment-dispatch",
    "role:typing-marker-recognition",
    "role:annotation-processing",
    "role:type-annotation-regressions"
  ],
  "write_set": []
}
```

An empty source command is intentional: no current checkout command has been bound or executed by this package.
