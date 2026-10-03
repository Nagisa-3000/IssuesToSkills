# Inspect typing-factory annotation boundaries

Locate the current call visitor and its typing recognizer, annotation-state manager, and child traversal helper. Read the public regression suite and reproduce the reported boundary problem using current public commands.

Classify factory names and field labels separately from field types, constraints, bounds, and cast type arguments. Check the recognized factory's identity rather than relying solely on a function's spelling. Record current AST-shape restrictions and fallback behavior.

This is read/probe work; it must not change tracked source or tests. Public probe execution may produce disposable output. The output is a current classification review, not a claim that the historical checkout was inspected or executed.

```arex-contract-v4
{
  "id": "workflow:verified-history:3257ebe843a343f545c15939:inspect",
  "intent": "Determine whether the current failure is caused by annotation context leaking into typing-factory metadata.",
  "mechanism": "Read current call traversal and compare public reproductions with factory component roles.",
  "semantic_role": "boundary-diagnosis",
  "owner_role": "typing-call-traversal-owner",
  "operation": "Locate current semantic owners, inspect annotation and ordinary traversal, and record a public boundary classification without modifying tracked source or tests.",
  "kind": "probe",
  "inputs": [],
  "outputs": [
    {
      "name": "boundary-review",
      "semantic_role": "typing-factory-boundary-review",
      "artifact_kind": "analysis-record",
      "language": "python",
      "scope": "current-checkout",
      "phase": "pre-edit",
      "state": "observed",
      "optional": false
    }
  ],
  "preconditions": [],
  "effects": [
    {"key": "boundary-classification-observed", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "genuine-forward-reference-diagnostics-preserved", "value": true, "evaluator": "evidence"},
    {"key": "ordinary-call-traversal-preserved", "value": true, "evaluator": "evidence"},
    {"key": "supported-adjacent-typing-behavior-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "inspect-public-boundary",
      "instruction": "Using current public code and a bound public reproduction command, establish the recognized factory, annotation-state owner, metadata/type partition, and observed diagnostics. Confirm that the probe changes no tracked source or tests.",
      "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:575:repair:e3f26593eac9"],
  "evidence_refs": ["PyCQA/pyflakes:575:body", "PyCQA/pyflakes:575:fix"],
  "read_set": ["role:typing-call-traversal-owner", "role:annotation-regression-owner"],
  "write_set": [],
  "resource": "references/actions/inspect.md",
  "package_id": "workflow:verified-history:3257ebe843a343f545c15939"
}
```

If the current failure is a genuine missing type name, record non-applicability. If owner bindings or semantics remain unknown, continue probing rather than authorizing the edit.
