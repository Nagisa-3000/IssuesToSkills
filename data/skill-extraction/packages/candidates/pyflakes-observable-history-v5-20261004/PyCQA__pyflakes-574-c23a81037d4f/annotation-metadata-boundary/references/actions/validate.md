# Validate target and adjacent behavior

Bind, render, and execute current public commands after the edit. Empty command arrays are placeholders.

Check both the original top-level reproduction and the historical function-annotation assertions. Exercise ordinary metadata name analysis and surrounding state restoration. Check current supported slice shapes, fallback traversal, target/context traversal, and applicable `Literal` regressions.

These additional invariant probes are current validation requirements derived from implementation facts, not claims of additional historical tests. Report broader suite results separately from the supplied changed-test-only qualification.

```arex-contract-v4
{
  "id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6:validate",
  "intent": "Observe removal of false metadata-string diagnostics without losing adjacent analysis.",
  "mechanism": "Execute public reproductions, focused tests and invariant probes after modification.",
  "semantic_role": "boundary-validation",
  "owner_role": "python-annotation-regression-suite",
  "operation": "Execute bound public checks, refresh anchors and record actual outcomes.",
  "kind": "validate",
  "inputs": [
    {
      "name": "boundary-context",
      "semantic_role": "annotation-boundary-context",
      "artifact_kind": "code-and-probe-record",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "repair",
      "state": "edited",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "validation-record",
      "semantic_role": "annotation-boundary-validation",
      "artifact_kind": "public-validation-record",
      "language": "Python",
      "scope": "current-public-checkout",
      "phase": "validation",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "boundary-edit-and-tests-present", "value": true, "evaluator": "evidence"},
    {"key": "current-public-oracles-bound", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {
      "key": "repair-public-validation",
      "value": true,
      "evaluator": "evidence",
      "description": "Claim only when executed checks establish the target effect and required preservation invariants."
    }
  ],
  "preserves": [
    {"key": "checkout-content", "value": "unchanged", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "metadata-reproduction",
      "instruction": "Analyze top-level Annotated[int, '>1'] and a function parameter annotated Annotated[int, '> 0']; verify no metadata-string forward-annotation syntax diagnostic.",
      "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:regression"],
      "kind": "public_mre",
      "command": []
    },
    {
      "id": "forward-type-regressions",
      "instruction": "Execute current equivalents of the four historical assertions: UndefinedName for Annotated['integer'], Annotated['integer', 1], and Union[Annotated['int', '>0'], 'integer']; no diagnostics for Annotated[int, '> 0']. Record diagnostic identities and available locations.",
      "evidence_refs": ["PyCQA/pyflakes:574:regression"],
      "kind": "repository_test",
      "command": []
    },
    {
      "id": "adjacent-traversal",
      "instruction": "Execute applicable annotation and Literal tests and public probes for metadata expression names, surrounding state restoration, fallback and target/context traversal, and supported AST representations. Report any unobserved invariant as UNKNOWN.",
      "evidence_refs": ["PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:574:repair:c23a81037d4f"],
  "evidence_refs": ["PyCQA/pyflakes:574:body", "PyCQA/pyflakes:574:fix", "PyCQA/pyflakes:574:regression"],
  "resource": "references/actions/validate.md",
  "package_id": "workflow:verified-history:cf4b82f5b317bd4e3ec515a6",
  "read_set": [
    "role:python-annotation-subscript-analysis",
    "role:python-annotation-state-controller",
    "role:python-annotation-regression-suite"
  ],
  "write_set": [],
  "validation_for": ["workflow:verified-history:cf4b82f5b317bd4e3ec515a6:repair"]
}
```

Retain failures and incomplete outcomes. Do not turn expected effects into observations. Further edits invalidate validation and require another run.
