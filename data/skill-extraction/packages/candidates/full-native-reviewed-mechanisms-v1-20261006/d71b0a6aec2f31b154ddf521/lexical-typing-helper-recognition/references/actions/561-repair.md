# Repair module receiver recognition

For a simple-name receiver inspect the first lexical binding. Accept only imported-module provenance in the existing supported set. Reject non-import, unsupported or absent bindings without bypassing shadowing. Retain direct-name recognition, receiver shape and attribute matcher.

Encode aliased overload coverage, not an all-Literal claim. Shadowing termination is code evidence, not supplied dedicated new historical test coverage.

```arex-contract-v4
{
  "id":"local_template:verified-history:d71b0a6aec2f31b154ddf521:561:repair",
  "intent":"Replace receiver spelling recognition with nearest-binding module provenance.",
  "mechanism":"Resolve the first receiver binding and test supported module import identity.",
  "semantic_role":"binding-recognition-repair",
  "owner_role":"typing-helper-detector",
  "operation":"Edit bound simple-name receiver recognition and encode supported module alias overload coverage without broadening adjacent helper branches.",
  "kind":"edit",
  "inputs":[{"name":"receiver-context","semantic_role":"receiver-context","artifact_kind":"inspection-record","language":"Python","scope":"current-pyflakes-module-receiver","phase":"pre-edit","state":"applicability-established","optional":false}],
  "outputs":[{"name":"receiver-change","semantic_role":"receiver-change","artifact_kind":"code-and-test-diff","language":"Python","scope":"current-pyflakes-module-receiver","phase":"post-edit","state":"awaiting-validation","optional":false}],
  "preconditions":[
    {"key":"applicability-established","value":true,"evaluator":"evidence"},
    {"key":"import-provenance-reliable","value":true,"evaluator":"evidence"},
    {"key":"role:typing-helper-detector","value":true,"evaluator":"symbol_exists"},
    {"key":"role:lexical-import-binding-model","value":true,"evaluator":"symbol_exists"},
    {"key":"role:annotation-regression-suite","value":true,"evaluator":"file_exists"}
  ],
  "effects":[{"key":"repair-present","value":true,"evaluator":"evidence"},{"key":"regression-present","value":true,"evaluator":"evidence"}],
  "preserves":[
    {"key":"first-binding-shadowing-preserved","value":true,"evaluator":"evidence"},
    {"key":"recognition-boundaries-preserved","value":true,"evaluator":"evidence"},
    {"key":"ordinary-diagnostics-preserved","value":true,"evaluator":"evidence"}
  ],
  "invalidates":["public-validation-observed","required-public-checks-pass"],
  "oracle":[{"id":"review-receiver-diff","instruction":"Review nearest-first search, immediate termination at the first binding, import-kind and supported full module identity checks, absence rejection and unchanged direct-name, simple-name and attribute-matcher boundaries. Verify aliased overload coverage. Reject arbitrary provider/receiver expansion or every-Literal-alias success claims. Review does not execute tests.","evidence_refs":["PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],"kind":"public_probe","command":[]}],
  "source_ids":["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs":["PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],
  "read_set":["role:typing-helper-detector","role:lexical-import-binding-model","role:annotation-regression-suite"],
  "write_set":["role:typing-helper-detector","role:annotation-regression-suite"],
  "resource":"references/actions/561-repair.md",
  "package_id":"local_template:verified-history:d71b0a6aec2f31b154ddf521"
}
```

Intended effects require current review and execution of the validation Action.
