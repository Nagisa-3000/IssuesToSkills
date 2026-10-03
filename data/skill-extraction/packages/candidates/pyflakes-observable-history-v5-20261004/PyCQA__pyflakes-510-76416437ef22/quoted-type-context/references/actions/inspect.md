# Inspect the typing-boundary owner

Locate current Python analyzer code responsible for typing-name resolution, annotation state, string annotation parsing, call traversal, and subscription traversal. Bind the semantic role to real current symbols and record code anchors.

Reproduce the reported diagnostic using public code. Check whether names in quoted `cast` types and partially quoted subscriptions are missed. Inspect the existing `Literal` exception and whether direct imports, renamed imports, and shadowing are resolved through scope bindings.

The output is a current inspection artifact, not a historical path binding. No current execution is claimed here.

```arex-contract-v4
{
  "id": "workflow:verified-history:3f957b40be188975fdc11a7e:inspect",
  "intent": "Establish current applicability and locate the owner of quoted typing-expression traversal.",
  "mechanism": "Inspect Python AST traversal and import resolution, then reproduce the public diagnostic.",
  "semantic_role": "typing-boundary-inspection",
  "owner_role": "python-annotation-traversal",
  "operation": "Bind current owners and observe quoted-type versus ordinary-value behavior.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "inspected-owner",
      "semantic_role": "python-annotation-traversal",
      "artifact_kind": "code-and-observation-record",
      "language": "python",
      "scope": "current-public-checkout",
      "phase": "inspection",
      "state": "inspected",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "current-applicability-recorded",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "checkout-unmodified",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "inspect-public-reproduction",
      "instruction": "Locate and hash current owner anchors; run the public quoted-cast reproduction and record both the import-use diagnostic and the separate undefined-name diagnostic.",
      "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:python-annotation-traversal"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:510:repair:76416437ef22"],
  "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:3f957b40be188975fdc11a7e"
}
```

Bind the oracle to a current command before running it. A missing owner or uncertain reproduction permits further inspection, not speculative editing.
