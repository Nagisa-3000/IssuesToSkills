# Inspect the special-binding boundary

Locate semantic owners in the current Python analyzer. Review the immediate parent of the special name for direct assignment and unpacking. Verify that ordinary dispatch remains available when specialized export handling is skipped. Do not bind by historical line number.

```arex-contract-v4
{
  "id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d:inspect",
  "intent": "Establish whether the current defect matches the supported AST-parent mismatch.",
  "mechanism": "Compare specialized constructor assumptions with dispatch predicates and target-parent shapes.",
  "semantic_role": "binding-boundary-inspection",
  "owner_role": "python-binding-dispatch",
  "operation": "Read current dispatch, specialized constructor, parent tracking, and export tests; probe direct and unpacked target shapes.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {"name": "boundary", "semantic_role": "export-binding-boundary", "artifact_kind": "review", "language": "python", "scope": "current-checkout", "phase": "inspection", "state": "established"}
  ],
  "preconditions": [],
  "effects": [
    {"key": "binding-boundary-reviewed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "parent-shape-review",
      "instruction": "Record current code anchors and show whether unpacking gives the name an indirect parent while direct assignments have supported statement parents; verify fallback dispatch.",
      "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:674:repair:1fae3dea5108"],
  "evidence_refs": ["PyCQA/pyflakes:674:body", "PyCQA/pyflakes:674:fix", "PyCQA/pyflakes:674:regression"],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:f2c2b6fce32efbe8ccca4f4d",
  "read_set": ["role:python-binding-dispatch", "role:python-export-binding-constructor", "role:python-export-diagnostic-tests"],
  "write_set": []
}
```

An established review may conclude that this Workflow is inapplicable. Its output does not itself authorize modification; the guard's semantic prerequisites must pass.
