---
name: lexical-typing-helper-recognition
description: "Conditionally repair Pyflakes typing-helper recognition through nearest lexical bindings and supported import provenance."
---

# Lexical typing-helper recognition

Package/Pattern ID: `local_template:verified-history:d71b0a6aec2f31b154ddf521`.

Pyflakes typing-helper recognition must search lexical scopes from nearest to farthest, stop at the first binding, and test that binding's supported import provenance rather than requiring a current-scope binding or a literal module receiver spelling.

## Activation and exclusions

Activate after current public inspection establishes either an immediate-scope bare-overload lookup missing an enclosing `typing.overload` import, or receiver-spelling recognition missing an alias of an already-supported typing module.

Clarify or probe when owners, import provenance, scope order or receiver shape are unknown. Do not activate for runtime import failures, arbitrary object receivers, unsupported providers, direct-import-only Literal alias symptoms, decorator-scanning-only defects, or another cause in already binding-aware code.

## Conditional Pattern

Role IDs below exactly match the `semantic_role` of their Action alternatives.

```arex-pattern-v4
{
  "id": "local_template:verified-history:d71b0a6aec2f31b154ddf521",
  "mechanism": "Pyflakes typing-helper recognition must search lexical scopes from nearest to farthest, stop at the first binding, and test that binding's supported import provenance rather than requiring a current-scope binding or a literal module receiver spelling.",
  "roles": [
    {
      "id": "recognition-discovery",
      "effects": [{"key":"applicability-established","value":true,"evaluator":"evidence"}],
      "alternatives": ["local_template:verified-history:d71b0a6aec2f31b154ddf521:434:inspect","local_template:verified-history:d71b0a6aec2f31b154ddf521:561:inspect"],
      "evidence_refs": ["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:561:fix"],
      "required": true
    },
    {
      "id": "binding-recognition-repair",
      "effects": [{"key":"repair-present","value":true,"evaluator":"evidence"},{"key":"regression-present","value":true,"evaluator":"evidence"}],
      "alternatives": ["local_template:verified-history:d71b0a6aec2f31b154ddf521:434:repair","local_template:verified-history:d71b0a6aec2f31b154ddf521:561:repair"],
      "evidence_refs": ["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:434:regression","PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],
      "required": true
    },
    {
      "id": "recognition-validation",
      "effects": [{"key":"public-validation-observed","value":true,"evaluator":"evidence"},{"key":"required-public-checks-pass","value":true,"evaluator":"evidence"}],
      "alternatives": ["local_template:verified-history:d71b0a6aec2f31b154ddf521:434:validate","local_template:verified-history:d71b0a6aec2f31b154ddf521:561:validate"],
      "evidence_refs": ["PyCQA/pyflakes:434:regression","PyCQA/pyflakes:561:regression"],
      "required": true
    }
  ],
  "required_effects": [
    {"key":"repair-present","value":true,"evaluator":"evidence"},
    {"key":"regression-present","value":true,"evaluator":"evidence"},
    {"key":"public-validation-observed","value":true,"evaluator":"evidence"},
    {"key":"required-public-checks-pass","value":true,"evaluator":"evidence"}
  ],
  "invariants": [
    {"key":"first-binding-shadowing-preserved","value":true,"evaluator":"evidence"},
    {"key":"recognition-boundaries-preserved","value":true,"evaluator":"evidence"},
    {"key":"ordinary-diagnostics-preserved","value":true,"evaluator":"evidence"}
  ],
  "applicability": [
    {"key":"supported-defect-observed","value":true,"evaluator":"evidence"},
    {"key":"import-provenance-reliable","value":true,"evaluator":"evidence"}
  ],
  "exclusions": [
    {"key":"arbitrary-receiver-required","value":true,"evaluator":"evidence"},
    {"key":"unsupported-provider-required","value":true,"evaluator":"evidence"},
    {"key":"different-cause-established","value":true,"evaluator":"evidence"}
  ],
  "partial_order": [
    {"before":"recognition-discovery","after":"binding-recognition-repair","reason":"Establish current owners, provenance and causal applicability before editing.","evidence_refs":["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:561:fix"]},
    {"before":"binding-recognition-repair","after":"recognition-validation","reason":"Edited recognition and assertions require fresh public execution.","evidence_refs":["PyCQA/pyflakes:434:regression","PyCQA/pyflakes:561:regression"]}
  ],
  "supporting_workflow_ids": [
    "local_template:verified-history:d71b0a6aec2f31b154ddf521:realization:434",
    "local_template:verified-history:d71b0a6aec2f31b154ddf521:realization:561"
  ],
  "evidence_refs": ["PyCQA/pyflakes:434:fix","PyCQA/pyflakes:434:regression","PyCQA/pyflakes:561:fix","PyCQA/pyflakes:561:regression"],
  "cross_project": false
}
```

## Current probes and operations

Select a source-specific alternative, not a concatenation of independent histories:

- Bare names: [inspect](references/actions/434-inspect.md), [repair](references/actions/434-repair.md), [validate](references/actions/434-validate.md), [primary realization](references/workflow.md).
- Module receivers: [inspect](references/actions/561-inspect.md), [repair](references/actions/561-repair.md), [validate](references/actions/561-validate.md), [additional realization](references/realizations/561.md).

Bind the current recognizer, scope/import model, diagnostic consumer and regression suite. Historical paths in the [episode](references/episode.md) are not current bindings.

Construct a public TaskContext with pinned base, hashed anchors, observed facts, semantic checks, actual bindings, observed PortValues and current Oracle bindings. Each Oracle maps action_id/source_oracle_id to current public instruction, argv and evidence_refs; its check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty historical command arrays are placeholders, not execution authorization.

Use PASS/FAIL/UNKNOWN. UNKNOWN prerequisites permit probes only; hard failures reject the plan. Structural PASS predicts compatibility, not success. Current ordering follows compatible ports and semantic dependencies, not historical list position. Omit satisfied operations only with fresh compatible evidence. Every executed edit retains explicit validation.

## Validation and stopping

Execute positive regressions, the annotation suite and boundary probes against edited anchors. Preserve nearest-binding shadowing, ordinary diagnostics and source-specific recognition boundaries. Record argv, exit status, actual outputs and unresolved checks without changing code or assertions during validation.

An outcomes record can contain failures. Establish `required-public-checks-pass` only when every required check actually passes. FAIL or UNKNOWN prevents acceptance. Further edits invalidate prior validation. Stop if owners or reliable provenance cannot be established, shadowing would be bypassed, preservation fails, or validation cannot finish.

## Evidence limits

One-repository local_template. Shadowing termination is visible in code but no dedicated new shadowing assertion is shown. Issue 434 also changes decorator scanning to any-match; that is one shared repair component, not another independent source. Issue 561's new regression tests aliased overload, not every renamed-Literal report claim. No execution or transfer result is inferred.

Any-match is a conditional source-specific companion, not a generalized role. Historical test/CI execution is unknown. Later independent replays qualify existing artifacts only; they do not execute this Skill or establish whole-project correctness, dedicated shadowing coverage or transfer. See [provenance](references/provenance.json).

[Activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json) and [functional](evals/functional-cases.json) definitions remain `not_executed`.

Keep formal knowledge/checkpoints frozen. Do not publish current plans as historical knowledge. Independent hidden acceptance occurs after stopping and never supplies guidance. Time-reconstructed catalogs exclude own issue/fix/cluster/aliases/copies and every discovery input unavailable before query time.
