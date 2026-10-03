# Repair narrowly scoped annotation entry

Use the bound analyzer owners to implement the historical mechanism in current code. Recognize imported typing members through their actual imported names, including renamed bare imports. Retain specific `cast` recognition and add any-member recognition only for the typing-subscription branch.

Enter annotation context through a restoration-safe helper. Process a string first positional argument of recognized `cast` as an annotation; keep normal traversal and do not treat its runtime value argument as annotation syntax. Enter annotation context for recognized typing subscriptions without bypassing existing special Literal handling. Adapt string AST representation to the supported Python versions; the historical patch used `ast.Str`.

Add public regression assertions alongside the relevant existing tests. Do not silently extend this mechanism to arbitrary calls, subscriptions, module aliases, or every argument of typing APIs.

```arex-contract-v4
{
  "id": "workflow:verified-history:3f957b40be188975fdc11a7e:repair",
  "intent": "Repair quoted type use recognition with narrow annotation-context entry.",
  "mechanism": "Scoped typing-member recognition plus restoration-safe annotation traversal.",
  "semantic_role": "context-repair",
  "owner_role": "python-annotation-analyzer",
  "operation": "Edit the bound recognition helper, annotation-context manager and call/subscription visitors; add public tests for quoted casts, aliases, nested quoted subscriptions and runtime-string noninterpretation.",
  "kind": "edit",
  "inputs": [
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
  "outputs": [
    {
      "name": "patched-analyzer",
      "semantic_role": "annotation-context-repair",
      "artifact_kind": "source-tree",
      "language": "python",
      "scope": "annotation-analyzer",
      "phase": "repair",
      "state": "modified"
    }
  ],
  "preconditions": [
    {"key": "annotation-owners-located", "value": true, "evaluator": "evidence"},
    {"key": "compatible-annotation-mechanism", "value": true, "evaluator": "evidence"},
    {"key": "role:python-annotation-analyzer", "value": true, "evaluator": "symbol_exists"},
    {"key": "role:annotation-regression-tests", "value": true, "evaluator": "file_exists"}
  ],
  "effects": [
    {"key": "quoted-type-name-use", "value": "recognized", "evaluator": "evidence"}
  ],
  "preserves": [
    {"key": "runtime-string-semantics", "value": "preserved", "evaluator": "evidence"},
    {"key": "annotation-state-restoration", "value": "preserved", "evaluator": "evidence"},
    {"key": "typing-literal-semantics", "value": "preserved", "evaluator": "evidence"}
  ],
  "invalidates": ["public-validation-observed"],
  "oracle": [
    {
      "id": "context-change-review",
      "instruction": "Review the public diff for scoped recognition, first-argument-only cast handling, retained child traversal, restoration in finally, and retention of special Literal handling. This review does not replace executing the validate Action.",
      "evidence_refs": ["PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"],
      "kind": "public_probe",
      "command": []
    }
  ],
  "read_set": ["role:python-annotation-analyzer", "role:annotation-regression-tests"],
  "write_set": ["role:python-annotation-analyzer", "role:annotation-regression-tests"],
  "source_ids": ["PyCQA/pyflakes:510:repair:76416437ef22"],
  "evidence_refs": ["PyCQA/pyflakes:510:fix", "PyCQA/pyflakes:510:regression"],
  "resource": "references/actions/repair-context.md",
  "package_id": "workflow:verified-history:3f957b40be188975fdc11a7e"
}
```

Effects describe the intended repair. They become observed facts only after current review and validation.
