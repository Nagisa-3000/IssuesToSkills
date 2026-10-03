# Inspect the load-context dependency

Locate the current load handler, every caller, parent-metadata initialization, augmented-assignment visitor, and adjacent diagnostic tests. Analyze the public reproducer without executing it. Confirm that early target load handling can reach context lookup before ordinary traversal has initialized metadata.

Determine whether the parent abstraction is the immediate AST owner or a normalized enclosing node. An incompatible abstraction is a stop condition, not permission to invent an adapter.

```arex-contract-v4
{
  "id": "workflow:verified-history:73c1883f7ed05d43025127fa:inspect",
  "intent": "Establish applicability and current semantic owner bindings.",
  "mechanism": "Trace early augmented-assignment load handling against parent-metadata initialization and ordinary load dispatch.",
  "semantic_role": "load-context-diagnosis",
  "owner_role": "ast-load-analysis",
  "operation": "Inspect current public code and analyze a minimal source string.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "context-diagnosis",
      "semantic_role": "load-context-diagnosis",
      "artifact_kind": "review-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "applicability-established",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "load-context-applicability", "value": "classified", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-source", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "locate-early-context-read",
      "instruction": "Review all load-handler callers and reproduce the public analyzer failure. Record whether target metadata is absent at the early load call and whether explicit owner context is semantically suitable.",
      "evidence_refs": ["PyCQA/pyflakes:744:body", "PyCQA/pyflakes:744:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:744:repair:e0d7a6be8959"],
  "evidence_refs": ["PyCQA/pyflakes:744:body", "PyCQA/pyflakes:744:fix"],
  "read_set": ["role:ast-load-analysis", "role:parent-context-provider", "role:augmented-assignment-analysis", "role:diagnostic-regression-tests"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:73c1883f7ed05d43025127fa"
}
```

The output is a current review record. If applicability remains UNKNOWN, do not produce a satisfied repair prerequisite.
