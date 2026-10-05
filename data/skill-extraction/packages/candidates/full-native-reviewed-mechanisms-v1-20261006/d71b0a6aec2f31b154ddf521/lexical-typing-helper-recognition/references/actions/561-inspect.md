# Inspect module receiver recognition

Inspect module receivers separately from directly imported helpers. The new historical assertion is aliased overload, not every Literal alias claim. Dedicated new shadowing assertions are not supplied.

```arex-contract-v4
{
  "id":"local_template:verified-history:d71b0a6aec2f31b154ddf521:561:inspect",
  "intent":"Establish module-alias applicability and bind current owners.",
  "mechanism":"Inspect receiver spelling dispatch and nearest-binding module provenance.",
  "semantic_role":"recognition-discovery",
  "owner_role":"typing-helper-detector",
  "operation":"Read current detector, lexical import model and annotation suite; run supported module alias and boundary probes without editing; record hashes, causal failure, provenance and baselines.",
  "kind":"probe",
  "inputs":[],
  "outputs":[{"name":"receiver-context","semantic_role":"receiver-context","artifact_kind":"inspection-record","language":"Python","scope":"current-pyflakes-module-receiver","phase":"pre-edit","state":"applicability-established","optional":false}],
  "preconditions":[],
  "effects":[
    {"key":"applicability-established","value":true,"evaluator":"evidence"},
    {"key":"supported-defect-observed","value":true,"evaluator":"evidence"},
    {"key":"import-provenance-reliable","value":true,"evaluator":"evidence"}
  ],
  "preserves":[
    {"key":"first-binding-shadowing-preserved","value":true,"evaluator":"evidence"},
    {"key":"recognition-boundaries-preserved","value":true,"evaluator":"evidence"},
    {"key":"ordinary-diagnostics-preserved","value":true,"evaluator":"evidence"}
  ],
  "oracle":[{"id":"inspect-receiver","instruction":"Record hashed owners, scope order, import-kind and module identity fields. Execute supported alias overload reproduction and confirm receiver spelling is causal. Record unaliased/direct-name, unsupported, absent, shadowing, receiver-shape, attribute matcher and ordinary diagnostic baselines. Verify no edits. UNKNOWN provenance or a direct-import-only cause does not establish applicability.","evidence_refs":["PyCQA/pyflakes:561:body","PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],"kind":"public_probe","command":[]}],
  "source_ids":["PyCQA/pyflakes:561:repair:13cad915e6b1"],
  "evidence_refs":["PyCQA/pyflakes:561:body","PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],
  "read_set":["role:typing-helper-detector","role:lexical-import-binding-model","role:annotation-regression-suite"],
  "write_set":[],
  "resource":"references/actions/561-inspect.md",
  "package_id":"local_template:verified-history:d71b0a6aec2f31b154ddf521"
}
```

Expected effects are not observations. Unresolved prerequisites permit inspection only.
