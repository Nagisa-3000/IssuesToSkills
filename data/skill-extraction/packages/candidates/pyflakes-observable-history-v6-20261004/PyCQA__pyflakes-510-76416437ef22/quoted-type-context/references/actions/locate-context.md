# Locate missed annotation contexts

Reproduce the public symptom and inspect the current analyzer. Bind semantic owners rather than assuming historical filenames. Read/probe operations must not edit tracked source; capture diagnostics and owner anchors as current observations.

Identify the call and subscription visitors, import-binding recognition, string-annotation processing, annotation state, special Literal handling, and public tests. Confirm a compatible mechanism exists before proposing an edit.

```arex-contract-v4
{
  "id": "workflow:verified-history:3f957b40be188975fdc11a7e:locate",
  "intent": "Diagnose missing annotation traversal for recognized quoted typing expressions.",
  "mechanism": "Compare a public quoted-cast reproduction with current AST visitor and binding logic.",
  "semantic_role": "context-diagnosis",
  "owner_role": "python-annotation-analyzer",
  "operation": "Read current source and run a public minimal reproduction without editing tracked source; record owner bindings and diagnostic observations.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "context-map",
      "semantic_role": "annotation-owner-map",
      "artifact_kind": "binding-report",
      "language": "python",
      "scope": "annotation-analyzer",
      "phase": "diagnosis",
      "state": "located"
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "annotation-owners-located", "value": true, "evaluator": "evidence"},
    {"key": "compatible-annotation-mechanism", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "runtime-string-semantics", "value": "preserved", "evaluator": "evidence"},
    {"key": "annotation-state-restoration", "value": "preserved", "evaluator": "evidence"},
    {"key": "typing-literal-semantics", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "public-context-diagnosis",
      "instruction": "Use public input equivalent to the reported quoted cast, record which imports are marked unused, and inspect the bound owners for annotation entry, scope resolution and Literal handling. Confirm probes did not edit tracked source.",
      "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix"],
      "kind": "public_mre",
      "command": []
    }
  ],
  "read_set": ["role:python-annotation-analyzer", "role:annotation-regression-tests"],
  "write_set": [],
  "source_ids": ["PyCQA/pyflakes:510:repair:76416437ef22"],
  "evidence_refs": ["PyCQA/pyflakes:510:body", "PyCQA/pyflakes:510:fix"],
  "resource": "references/actions/locate-context.md",
  "package_id": "workflow:verified-history:3f957b40be188975fdc11a7e"
}
```

Outputs and effects are expected products of current probing, not observations already established for a new checkout. If the owner map or semantic compatibility is UNKNOWN, continue diagnosis only.
