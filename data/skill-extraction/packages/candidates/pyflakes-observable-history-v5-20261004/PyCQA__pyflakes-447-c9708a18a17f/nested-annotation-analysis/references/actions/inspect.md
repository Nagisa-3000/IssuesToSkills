# Inspect annotation-string traversal

Locate the current semantic owners before proposing an edit. Reproduce the diagnostic with a public minimal example; compare partial quotation with whole-annotation quotation. Inspect, rather than assume, whether the string visitor ignores nested annotation strings.

Identify annotation-context lifetime, deferred queue behavior, AST string representations, and typing/Literal recognition. A lack of current evidence is `UNKNOWN`, not permission to edit.

```arex-contract-v4
{
  "id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:inspect",
  "intent": "Determine whether a nested quoted annotation loses name-use analysis and bind its current owners.",
  "mechanism": "Public reproduction plus semantic review of annotation, string, typing and deferred traversal.",
  "semantic_role": "annotation-traversal-diagnosis",
  "owner_role": "python-annotation-analysis",
  "operation": "inspect-and-reproduce",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "located-analysis",
      "semantic_role": "annotation-analysis-owner-map",
      "artifact_kind": "reviewed-python-checkout",
      "language": "python",
      "scope": "annotation-analysis",
      "phase": "pre-edit",
      "state": "diagnosed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "public-checkout-pinned", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "annotation-owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "nested-quote-diagnostic-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-unmodified", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "diagnose-partial-quotation",
      "instruction": "Run a public reproduction using an imported type only inside Optional['Type[int]']; compare the whole-quoted form and inspect the responsible visitors. Record diagnostics, code anchors and semantic bindings.",
      "evidence_refs": ["PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:447:repair:c9708a18a17f"],
  "evidence_refs": ["PyCQA/pyflakes:447:title", "PyCQA/pyflakes:447:body", "PyCQA/pyflakes:447:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0",
  "read_set": [
    "role:python-annotation-analysis",
    "role:python-string-node-dispatch",
    "role:python-deferred-analysis",
    "role:typing-construct-recognition",
    "role:annotation-regression-tests"
  ],
  "write_set": []
}
```

The output is a current evidence-backed owner map, not simply a matching filename. The oracle's empty command means no current executable command has been supplied; bind one publicly before execution.
