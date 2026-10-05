# Repair bare-name recognition

Search nearest scopes first, terminate at the first binding and require imported-symbol identity `typing.overload`. Wire the scope stack into the diagnostic consumer. Preserve function-node and qualified branches and ordinary gating.

Add or retain class-contained coverage. Apply any-match only if inspection separately establishes missing scanning, retaining or adding its regression. It is a companion, not another source. Shadowing termination has code support, not dedicated new historical assertion coverage.

```arex-contract-v4
{
  "id":"local_template:verified-history:d71b0a6aec2f31b154ddf521:434:repair",
  "intent":"Correct enclosing-import recognition without broad diagnostic suppression.",
  "mechanism":"Resolve the first bare-name binding and test imported-symbol provenance.",
  "semantic_role":"binding-recognition-repair",
  "owner_role":"overload-recognition-and-redefinition-gate",
  "operation":"Edit bound recognition and scope-stack consumer wiring; encode enclosing-import coverage in the bound annotation suite and apply the any-match companion only when established as missing.",
  "kind":"edit",
  "inputs":[{"name":"bare-context","semantic_role":"bare-name-context","artifact_kind":"inspection-record","language":"Python","scope":"current-pyflakes-bare-overload","phase":"pre-edit","state":"applicability-established","optional":false}],
  "outputs":[{"name":"bare-change","semantic_role":"bare-name-change","artifact_kind":"code-and-test-diff","language":"Python","scope":"current-pyflakes-bare-overload","phase":"post-edit","state":"awaiting-validation","optional":false}],
  "preconditions":[
    {"key":"applicability-established","value":true,"evaluator":"evidence"},
    {"key":"import-provenance-reliable","value":true,"evaluator":"evidence"},
    {"key":"role:overload-recognition-and-redefinition-gate","value":true,"evaluator":"symbol_exists"},
    {"key":"role:scope-stack-and-import-bindings","value":true,"evaluator":"symbol_exists"},
    {"key":"role:annotation-regression-suite","value":true,"evaluator":"file_exists"}
  ],
  "effects":[{"key":"repair-present","value":true,"evaluator":"evidence"},{"key":"regression-present","value":true,"evaluator":"evidence"}],
  "preserves":[
    {"key":"first-binding-shadowing-preserved","value":true,"evaluator":"evidence"},
    {"key":"recognition-boundaries-preserved","value":true,"evaluator":"evidence"},
    {"key":"ordinary-diagnostics-preserved","value":true,"evaluator":"evidence"}
  ],
  "invalidates":["public-validation-observed","required-public-checks-pass"],
  "oracle":[{"id":"review-bare-diff","instruction":"Review nearest-first search, termination at the first binding including false for nonmatching identity, imported-symbol kind and typing.overload identity, scope-stack wiring, retained node/qualified branches and ordinary gating. Verify class coverage expects no unexpected diagnostics. Review any-match only as a justified companion. Diff review is not test execution.","evidence_refs":["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:434:regression"],"kind":"public_probe","command":[]}],
  "source_ids":["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs":["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:434:regression"],
  "read_set":["role:overload-recognition-and-redefinition-gate","role:scope-stack-and-import-bindings","role:annotation-regression-suite"],
  "write_set":["role:overload-recognition-and-redefinition-gate","role:annotation-regression-suite"],
  "resource":"references/actions/434-repair.md",
  "package_id":"local_template:verified-history:d71b0a6aec2f31b154ddf521"
}
```

Effects are intended postconditions; validation remains mandatory.
