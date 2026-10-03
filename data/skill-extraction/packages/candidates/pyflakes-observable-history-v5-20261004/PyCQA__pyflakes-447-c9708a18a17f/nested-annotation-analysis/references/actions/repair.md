# Repair annotation-aware string traversal

Use the diagnosed current owners, not historical paths, to implement the mechanism.

1. Enter annotation context while traversing both source annotations and parsed string annotations. Restore the prior value with exception-safe nesting.
2. Preserve that context when postponed annotations execute later.
3. For a string node reached in annotation context, parse and traverse it as a forward annotation unless it is inside a recognized typing `Literal`.
4. Before deferred processing, schedule forward-string work. During deferred processing, handle newly discovered nested strings directly rather than enqueueing work that may no longer be accepted.
5. Track Literal context with save/restore. Recognize supported typing constructs through actual bindings where applicable; do not classify any bare identifier named `Literal` as typing merely by spelling.
6. Cover the checkout's applicable string AST forms.
7. Add target and adjacent regression assertions.

The historical helper recognized imported names by `ImportationFrom.fullName` and qualified attributes whose base name was `typing` or `typing_extensions`. It did not demonstrate arbitrary module-alias resolution. If current code already has stronger binding-aware recognition, retain it rather than copying a historical limitation.

Reusing typing recognition must preserve overload behavior. Keep ordinary strings ignored and retain the existing forward-annotation syntax-error path.

```arex-contract-v4
{
  "id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0:repair",
  "intent": "Make nested quoted type expressions participate in name-use analysis while protecting Literal values.",
  "mechanism": "Scoped annotation and Literal context, deferred-aware nested parsing, and compatible string-node dispatch.",
  "semantic_role": "annotation-string-traversal-repair",
  "owner_role": "python-annotation-analysis",
  "operation": "edit-annotation-traversal-and-regressions",
  "kind": "edit",
  "inputs": [
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
  "outputs": [
    {
      "name": "candidate-analysis",
      "semantic_role": "annotation-analysis-candidate",
      "artifact_kind": "patched-python-checkout",
      "language": "python",
      "scope": "annotation-analysis",
      "phase": "post-edit",
      "state": "awaiting-validation",
      "optional": false
    }
  ],
  "preconditions": [
    {"key": "annotation-owner-bindings-recorded", "value": true, "evaluator": "evidence"},
    {"key": "nested-quote-diagnostic-observed", "value": true, "evaluator": "evidence"},
    {"key": "role:python-annotation-analysis", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"},
    {"key": "current-deferred-and-literal-semantics-compatible", "value": true, "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "nested-annotation-names-traversed", "value": true, "evaluator": "evidence"},
    {"key": "literal-string-values-not-parsed", "value": true, "evaluator": "evidence"},
    {"key": "target-and-adjacent-regressions-added", "value": true, "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "ordinary-strings-not-forward-annotations", "value": true, "evaluator": "evidence"},
    {"key": "annotation-and-literal-context-restored", "value": true, "evaluator": "evidence"},
    {"key": "existing-overload-recognition-preserved", "value": true, "evaluator": "evidence"},
    {"key": "forward-annotation-syntax-error-reporting-preserved", "value": true, "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "review-context-and-dispatch",
      "instruction": "Review the patch for exception-safe context restoration, annotation context inside deferred callbacks, Literal suppression, supported AST string dispatch, and retention of the forward-annotation error path. Confirm tests address each changed semantic branch.",
      "evidence_refs": ["PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "source_ids": ["PyCQA/pyflakes:447:repair:c9708a18a17f"],
  "evidence_refs": ["PyCQA/pyflakes:447:fix", "PyCQA/pyflakes:447:regression"],
  "resource": "references/actions/repair.md",
  "package_id": "workflow:verified-history:b2b64a5ca411f99a2e3c45e0",
  "read_set": [
    "role:python-annotation-analysis",
    "role:python-string-node-dispatch",
    "role:python-deferred-analysis",
    "role:typing-construct-recognition",
    "role:annotation-regression-tests"
  ],
  "write_set": [
    "role:python-annotation-analysis",
    "role:python-string-node-dispatch",
    "role:python-deferred-analysis",
    "role:typing-construct-recognition",
    "role:annotation-regression-tests"
  ],
  "invalidates": [
    "pre-edit-diagnostic-results",
    "pre-edit-regression-results",
    "pre-edit-code-anchor-hashes"
  ],
  "exclusions": [
    {"key": "repair-is-global-unused-import-suppression", "value": true, "evaluator": "evidence"}
  ]
}
```

Effects here are intended postconditions, not reported execution results. This Action is incomplete without the [validation Action](validate.md).
