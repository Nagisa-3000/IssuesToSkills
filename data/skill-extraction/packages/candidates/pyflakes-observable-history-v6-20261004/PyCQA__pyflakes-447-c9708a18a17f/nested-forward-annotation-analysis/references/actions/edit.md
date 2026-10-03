# Edit context-aware quoted-annotation traversal

Modify the bound semantic owners, not historical paths.

The historical implementation supports these operations:

1. Introduce annotation context with save/restore in `try/finally`. Enter it for direct annotation traversal and parsed string annotations.
2. Re-enter annotation context when postponed traversal actually executes; context at scheduling time alone is insufficient.
3. Handle string AST nodes inside annotation context by parsing them through the existing string-annotation machinery, preserving original source coordinates and syntax-error reporting.
4. Schedule this work before deferred processing begins. If already processing deferred work, execute the nested string handler immediately rather than adding work to a completed or unavailable queue.
5. Track traversal under recognized `Literal` subscripts with save/restore, so their strings remain values rather than annotation expressions.
6. Resolve bare typing names through the nearest scope binding, accepting the appropriate imports from `typing` or `typing_extensions`. Preserve existing overload recognition when sharing the helper.
7. Account for the current AST representation: the historical patch routed string-valued Python 3.8+ `Constant` nodes to string handling and left non-string constants alone.
8. Add current regression assertions for the target and adjacent behavior.

Do not blindly extend module-alias recognition, typing constructs, or AST versions beyond current evidence. The historical helper's qualified attribute branch matched the module spellings `typing` and `typing_extensions`; only bare names used scope-aware import resolution.

```arex-contract-v4
{
  "id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:edit",
  "intent": "Make nested annotation string references visible to normal name analysis.",
  "mechanism": "Annotation and Literal context guards plus phase-aware string-annotation dispatch.",
  "semantic_role": "annotation-traversal-repair",
  "owner_role": "python-static-analysis-annotation-traversal",
  "operation": "Edit the current bound annotation traversal, string dispatch, typing recognition and deferred-phase owners, and add public regression assertions.",
  "kind": "edit",
  "inputs": [
    {
      "name": "traversal-context",
      "semantic_role": "bound-annotation-traversal-context",
      "artifact_kind": "task-context",
      "language": "python",
      "scope": "current-checkout",
      "phase": "diagnosis",
      "state": "mechanism-confirmed",
      "optional": false
    }
  ],
  "outputs": [
    {
      "name": "candidate",
      "semantic_role": "nested-annotation-repair-candidate",
      "artifact_kind": "checkout-change",
      "language": "python",
      "scope": "current-checkout",
      "phase": "implementation",
      "state": "awaiting-public-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "annotation-mechanism-observed", "value": true, "evaluator": "evidence"},
    {"key": "semantic-owners-bound", "value": true, "evaluator": "evidence"},
    {"key": "role:python-static-analysis-annotation-traversal", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:python-static-analysis-deferred-runner", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:python-typing-binding-recognition", "value": true, "evaluator": "symbol_exists"}
  ],
  "effects": [
    {"key": "nested-annotation-references-recognized", "value": true, "evaluator": "evidence"},
    {"key": "regression-assertions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "runtime-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "literal-strings-remain-data", "value": true, "evaluator": "evidence"},
    {"key": "existing-overload-behavior-preserved", "value": true, "evaluator": "evidence"},
    {"key": "analysis-phase-integrity-preserved", "value": true, "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "review-context-repair",
      "instruction": "Review the current diff against public owner bindings: verify context restoration, Literal exclusion, supported string AST dispatch, phase-aware scheduling, and retention of existing typing overload behavior. This review does not replace the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:447:repair:c9708a18a17f"],
  "evidence_refs": ["PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
  "read_set": ["role:python-static-analysis-annotation-traversal", "role:python-static-analysis-deferred-runner", "role:python-typing-binding-recognition", "role:python-annotation-regression-tests"],
  "write_set": ["role:python-static-analysis-annotation-traversal", "role:python-static-analysis-deferred-runner", "role:python-typing-binding-recognition", "role:python-annotation-regression-tests"],
  "resource": "references/actions/edit.md",
  "package_id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0"
}
```

Effects are required candidate behavior, not claims of observed success. Retain the explicit validation Action after every edit, including subsequent adjustments.
