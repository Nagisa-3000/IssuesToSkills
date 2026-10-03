# Guard synthetic underscore initialization

At the current doctest initializer, insert the source-less synthetic `_` only if `_` is absent from the module scope. Preserve the normal insertion path when it is absent. Resolve the module scope semantically; do not assume a current scope stack index without inspection.

The historical implementation used `if '_' not in self.scopeStack[0]:` immediately around `self.addBinding(None, Builtin('_'))`. This Action does not authorize modifying the general parent traversal helper.

```arex-contract-v4
{
  "id": "workflow:verified-history:c76d35c9a48e360887b3c443:guard",
  "intent": "Avoid the synthetic binding collision at initialization.",
  "mechanism": "Guard synthetic underscore insertion with a module-scope absence check.",
  "semantic_role": "conditional-placeholder-initialization",
  "owner_role": "doctest-initializer",
  "operation": "Change unconditional source-less underscore initialization into initialization conditional on module-scope absence.",
  "kind": "edit",
  "inputs": [
    {"name": "initializer", "semantic_role": "doctest-initializer-code", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "baseline-reviewed", "optional": false}
  ],
  "outputs": [
    {"name": "initializer", "semantic_role": "doctest-initializer-code", "artifact_kind": "source", "language": "python", "scope": "current-checkout", "phase": "repair", "state": "conditionally-guarded", "optional": false}
  ],
  "preconditions": [
    {"key": "role:doctest-initializer", "value": true, "evaluator": "symbol_exists"},
    {"key": "source-less-insertion-collides-with-module-underscore", "value": true, "evaluator": "evidence"},
    {"key": "module-scope-binding", "value": "confirmed", "evaluator": "evidence"}
  ],
  "effects": [
    {"key": "synthetic-underscore-initialization", "value": "conditional-on-module-absence", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "existing-module-underscore", "value": "not-replaced-by-synthetic-binding", "evaluator": "evidence"},
    {"key": "no-module-underscore-doctests", "value": "preserved", "evaluator": "evidence"},
    {"key": "unused-import-diagnostic", "value": "preserved", "evaluator": "evidence"}
  ],
  "oracle": [
    {
      "id": "guard-review",
      "instruction": "Review the current diff to confirm that only synthetic underscore initialization is conditioned on absence in the confirmed module scope; defer behavioral acceptance to the linked validation Action.",
      "evidence_refs": ["PyCQA/pyflakes:421:fix"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:doctest-initializer", "role:binding-collision-handler"],
  "write_set": ["role:doctest-initializer"],
  "invalidates": ["baseline-reproduction-result", "doctest-suite-result", "initializer-code-anchor"],
  "source_ids": ["PyCQA/pyflakes:421:repair:2136e1e9f455"],
  "evidence_refs": ["PyCQA/pyflakes:421:body", "PyCQA/pyflakes:421:fix"],
  "resource": "references/actions/guard.md",
  "package_id": "workflow:verified-history:c76d35c9a48e360887b3c443"
}
```

The effect is expected until current review and public validation establish it. [Validate](validate.md) is mandatory after this modification.
