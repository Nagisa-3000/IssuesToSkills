# Primary realization: bare overload names

Pyflakes typing-helper recognition must search lexical scopes from nearest to farthest, stop at the first binding, and test that binding's supported import provenance rather than requiring a current-scope binding or a literal module receiver spelling.

This realization uses imported-symbol identity `typing.overload`. Any-match scanning is a conditional companion, not another source. Shadowing termination is visible in code, but dedicated new shadowing assertions and historical execution are not supplied.

```arex-workflow-v4
{
  "id":"local_template:verified-history:d71b0a6aec2f31b154ddf521:realization:434",
  "goal":"Recognize enclosing typing.overload imports without bypassing shadowing or broadly suppressing redefinition diagnostics.",
  "mechanism":"Pyflakes typing-helper recognition must search lexical scopes from nearest to farthest, stop at the first binding, and test that binding's supported import provenance rather than requiring a current-scope binding or a literal module receiver spelling.",
  "action_ids":["local_template:verified-history:d71b0a6aec2f31b154ddf521:434:inspect","local_template:verified-history:d71b0a6aec2f31b154ddf521:434:repair","local_template:verified-history:d71b0a6aec2f31b154ddf521:434:validate"],
  "source_ids":["PyCQA/pyflakes:434:repair:232cb1d27ee1"],
  "required_effects":[
    {"key":"repair-present","value":true,"evaluator":"evidence"},
    {"key":"regression-present","value":true,"evaluator":"evidence"},
    {"key":"public-validation-observed","value":true,"evaluator":"evidence"},
    {"key":"required-public-checks-pass","value":true,"evaluator":"evidence"}
  ],
  "invariants":[
    {"key":"first-binding-shadowing-preserved","value":true,"evaluator":"evidence"},
    {"key":"recognition-boundaries-preserved","value":true,"evaluator":"evidence"},
    {"key":"ordinary-diagnostics-preserved","value":true,"evaluator":"evidence"}
  ],
  "dependencies":[
    {"before":"local_template:verified-history:d71b0a6aec2f31b154ddf521:434:inspect","after":"local_template:verified-history:d71b0a6aec2f31b154ddf521:434:repair","reason":"Establish scope semantics, imported-symbol identity and causal applicability before editing.","evidence_refs":["PyCQA/pyflakes:434:body","PyCQA/pyflakes:434:fix"]},
    {"before":"local_template:verified-history:d71b0a6aec2f31b154ddf521:434:repair","after":"local_template:verified-history:d71b0a6aec2f31b154ddf521:434:validate","reason":"Edited recognition and assertions require fresh execution.","evidence_refs":["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:434:regression"]}
  ]
}
```

Actions realize `recognition-discovery`, `binding-recognition-repair` and `recognition-validation`, respectively. Dependencies express semantic obligations, not historical execution order.
