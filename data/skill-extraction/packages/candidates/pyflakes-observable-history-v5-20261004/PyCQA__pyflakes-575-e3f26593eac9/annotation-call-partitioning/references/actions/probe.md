# Probe annotation-state propagation

Locate the semantic owners of Python call traversal, typing-name resolution, annotation-state transitions, and annotation tests. Reproduce the public symptom and compare it with a genuine unresolved type reference.

Do not edit on an UNKNOWN classification. A similarly named user function is not enough to justify special traversal.

```arex-contract-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939:probe",
  "intent": "Determine whether annotation state incorrectly reaches typing-call metadata.",
  "mechanism": "Inspect typing-aware call dispatch and contrast metadata strings with true type-expression strings using public examples.",
  "semantic_role": "applicability-probe",
  "owner_role": "python-annotation-call-analysis",
  "operation": "Locate current owners and collect evidence for argument-role classification.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "located-checkout",
      "semantic_role": "annotation-traversal-checkout",
      "artifact_kind": "source-checkout",
      "language": "python",
      "scope": "typing-call-analysis-and-tests",
      "phase": "repair",
      "state": "located-and-applicability-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "current-owner-bindings-observed", "value": true, "evaluator": "evidence"},
    {"key": "argument-role-misclassification-confirmed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "classify-public-symptom",
      "instruction": "In the current public checkout, compare a nested TypedDict metadata-label example against a missing name in a genuine type position; inspect the typing-aware dispatch and state propagation. Report applicability as PASS, FAIL, or UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:fix", "PyCQA/pyflakes:575:regression"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:fix"],
  "resource": "references/actions/probe.md",
  "package_id": "workflow:verified-history:3257ebe843a343f545c15939",
  "read_set": ["role:python-annotation-call-analysis", "role:python-typing-name-resolution", "role:python-annotation-regression-tests"],
  "write_set": []
}
```

The output state is a required successful result, not an observed result of authoring this package. An unsuccessful probe must not produce that state.
