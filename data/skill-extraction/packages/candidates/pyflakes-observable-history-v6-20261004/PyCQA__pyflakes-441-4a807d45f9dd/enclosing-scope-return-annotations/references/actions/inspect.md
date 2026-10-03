# Inspect annotation traversal and establish applicability

Locate the current function-traversal owner and annotation-test owner. Trace when return annotations are processed relative to function-scope entry. Observe the public positive reproduction and function-body-only negative control.

This operation reads code and runs non-editing public probes; it does not modify source files. Its output is an evidence-backed applicability record, not a successful repair.

```arex-contract-v4
{
  "id": "workflow:verified-history:46d18832864f51ea6f6d3968:inspect",
  "intent": "Establish whether the enclosing-scope annotation traversal repair applies.",
  "mechanism": "Compare enclosing-class visibility with function-body-only visibility and locate the later child traversal.",
  "semantic_role": "annotation-scope-diagnosis",
  "owner_role": "python-function-traversal",
  "operation": "Read current traversal code, resolve semantic owners, and run bound non-editing public reproductions; confirm existing enclosing-scope annotation handling before authorizing an edit.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "applicability",
      "semantic_role": "annotation-traversal-applicability",
      "artifact_kind": "inspection-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-repair",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {
      "key": "traversal-owner-located",
      "value": true,
      "evaluator": "symbol_exists",
      "description": "Resolve role:python-function-traversal in the current checkout."
    },
    {
      "key": "existing-enclosing-scope-annotation-handling-confirmed",
      "value": true,
      "evaluator": "evidence"
    },
    {
      "key": "later-function-scope-return-retraversal-confirmed",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "preserves": [
    {
      "key": "function-body-only-annotation-name-diagnostic-preserved",
      "value": true,
      "evaluator": "evidence"
    }
  ],
  "oracle": [
    {
      "id": "confirm-scope-mechanism",
      "instruction": "Without editing source, record the current public reproduction, verify that the body-only name is diagnosed, and inspect code anchors showing appropriate earlier annotation handling plus later function-scope return traversal. If any mechanism fact is unknown, do not authorize repair.",
      "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:441:repair:4a807d45f9dd"],
  "evidence_refs": ["PyCQA/pyflakes:441:body", "PyCQA/pyflakes:441:fix", "PyCQA/pyflakes:441:regression"],
  "read_set": ["role:python-function-traversal", "role:python-annotation-regression-tests"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:46d18832864f51ea6f6d3968"
}
```

The `symbol_exists` observation must bind the semantic role to a concrete current symbol; the predicate key alone proves nothing. Expected output is emitted only after the mechanism is observed.
