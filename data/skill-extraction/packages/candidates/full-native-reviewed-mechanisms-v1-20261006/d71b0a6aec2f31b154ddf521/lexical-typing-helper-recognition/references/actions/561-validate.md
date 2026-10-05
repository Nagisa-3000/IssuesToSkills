# Validate module receiver repair

Run fresh checks without editing. Record a relevant original Literal reproduction separately; overload does not prove every direct-import alias case. Shadowing probes are current obligations, not new historical assertions. Historical replay is not current execution.

```arex-contract-v4
{
  "id":"local_template:verified-history:d71b0a6aec2f31b154ddf521:561:validate",
  "intent":"Observe supported alias correctness and preserved binding boundaries.",
  "mechanism":"Execute module alias regression and adjacent public binding probes.",
  "semantic_role":"recognition-validation",
  "owner_role":"annotation-regression-suite",
  "operation":"Execute bound alias regression, annotation suite and preservation probes without edits; record argv, exit status, diagnostics, edited hashes and unresolved checks.",
  "kind":"validate",
  "inputs":[{"name":"receiver-change","semantic_role":"receiver-change","artifact_kind":"code-and-test-diff","language":"Python","scope":"current-pyflakes-module-receiver","phase":"post-edit","state":"awaiting-validation","optional":false}],
  "outputs":[{"name":"receiver-results","semantic_role":"receiver-results","artifact_kind":"public-check-record","language":"Python","scope":"current-pyflakes-module-receiver","phase":"post-validation","state":"outcomes-recorded","optional":false}],
  "preconditions":[{"key":"repair-present","value":true,"evaluator":"evidence"},{"key":"regression-present","value":true,"evaluator":"evidence"},{"key":"current-public-oracles-bound","value":true,"evaluator":"evidence"}],
  "effects":[{"key":"public-validation-observed","value":true,"evaluator":"evidence"},{"key":"required-public-checks-pass","value":true,"evaluator":"evidence"}],
  "preserves":[
    {"key":"first-binding-shadowing-preserved","value":true,"evaluator":"evidence"},
    {"key":"recognition-boundaries-preserved","value":true,"evaluator":"evidence"},
    {"key":"ordinary-diagnostics-preserved","value":true,"evaluator":"evidence"}
  ],
  "oracle":[
    {"id":"run-receiver-regression","instruction":"Execute current aliased overload regression and annotation suite. Require zero unexpected diagnostics for supported alias sequences. Record actual argv, exit status and outcomes without inferring every Literal claim.","evidence_refs":["PyCQA/pyflakes:561:regression"],"kind":"repository_test","command":[]},
    {"id":"run-receiver-boundaries","instruction":"Execute supported unaliased, direct-name, shadowing, unsupported-module, absent, non-simple receiver, attribute-matcher and ordinary redefinition probes. Require rejection of nonmatching or absent bindings without outer fallback and preservation of baseline recognition and diagnostics. FAIL or UNKNOWN prevents required-public-checks-pass.","evidence_refs":["PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],"kind":"public_probe","command":[]}
  ],
  "validation_for":["local_template:verified-history:d71b0a6aec2f31b154ddf521:561:repair"],
  "source_ids":["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs":["PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],
  "read_set":["role:typing-helper-detector","role:lexical-import-binding-model","role:annotation-regression-suite"],
  "write_set":[],
  "resource":"references/actions/561-validate.md",
  "package_id":"local_template:verified-history:d71b0a6aec2f31b154ddf521"
}
```

Recording outcomes alone is not success. All required checks must pass; revalidate after further edits.
