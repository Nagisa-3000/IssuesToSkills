# Validate bare-name repair

Run current public checks against edited anchors without editing implementation or assertions. Shadowing probes are current obligations, not new historical assertions. Any-match coverage is companion coverage; historical replay cannot discharge this Action.

```arex-contract-v4
{
  "id":"local_template:verified-history:d71b0a6aec2f31b154ddf521:434:validate",
  "intent":"Observe corrected recognition and preserved boundaries.",
  "mechanism":"Execute positive regressions and first-binding preservation probes.",
  "semantic_role":"recognition-validation",
  "owner_role":"annotation-regression-suite",
  "operation":"Execute bound class and multiple-decorator checks, annotation suite and preservation probes without edits; record argv, exit status, diagnostics, edited hashes and unresolved checks.",
  "kind":"validate",
  "inputs":[{"name":"bare-change","semantic_role":"bare-name-change","artifact_kind":"code-and-test-diff","language":"Python","scope":"current-pyflakes-bare-overload","phase":"post-edit","state":"awaiting-validation","optional":false}],
  "outputs":[{"name":"bare-results","semantic_role":"bare-name-results","artifact_kind":"public-check-record","language":"Python","scope":"current-pyflakes-bare-overload","phase":"post-validation","state":"outcomes-recorded","optional":false}],
  "preconditions":[{"key":"repair-present","value":true,"evaluator":"evidence"},{"key":"regression-present","value":true,"evaluator":"evidence"},{"key":"current-public-oracles-bound","value":true,"evaluator":"evidence"}],
  "effects":[{"key":"public-validation-observed","value":true,"evaluator":"evidence"},{"key":"required-public-checks-pass","value":true,"evaluator":"evidence"}],
  "preserves":[
    {"key":"first-binding-shadowing-preserved","value":true,"evaluator":"evidence"},
    {"key":"recognition-boundaries-preserved","value":true,"evaluator":"evidence"},
    {"key":"ordinary-diagnostics-preserved","value":true,"evaluator":"evidence"}
  ],
  "oracle":[
    {"id":"run-bare-regressions","instruction":"Execute current class-contained and multiple-decorator overload assertions and annotation suite. Require zero unexpected diagnostics for valid overload sequences. Record argv, exit status and actual outcomes.","evidence_refs":["PyCQA/pyflakes:434:regression"],"kind":"repository_test","command":[]},
    {"id":"run-bare-boundaries","instruction":"Execute ordinary unused-redefinition, nearer non-typing shadowing, qualified recognition and function-node probes. Require ordinary diagnostics, rejection at a nearer nonmatching binding without outer fallback, and qualified/node behavior matching baseline. Record every check; FAIL or UNKNOWN prevents required-public-checks-pass.","evidence_refs":["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:434:regression"],"kind":"public_probe","command":[]}
  ],
  "validation_for":["local_template:verified-history:d71b0a6aec2f31b154ddf521:434:repair"],
  "source_ids":["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "evidence_refs":["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:434:regression"],
  "read_set":["role:overload-recognition-and-redefinition-gate","role:scope-stack-and-import-bindings","role:annotation-regression-suite"],
  "write_set":[],
  "resource":"references/actions/434-validate.md",
  "package_id":"local_template:verified-history:d71b0a6aec2f31b154ddf521"
}
```

Recording execution does not establish success. Every required check must pass; further edits require revalidation.
