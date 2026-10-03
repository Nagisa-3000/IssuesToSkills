---
name: async-function-scope-registration
description: "Diagnose and repair missing asynchronous-function scope registration in a Python AST analyzer when annotated argument binding escapes its intended function scope."
---

# Asynchronous-function scope registration

## Activation and exclusions

Activate for inspection when a Python AST analyzer crashes during annotated asynchronous-function argument binding and asynchronous function nodes may be absent from its node-to-scope registry. The historical public reproduction was:

```python
class foo:
    pass

async def func(foo: foo):
    pass
```

The reported exception was `AttributeError: 'Module' object has no attribute 'parent'`. That symptom alone does not establish the cause.

Clarify or probe when the reproduction, scope owner, registry representation, or supported-runtime policy is unknown. Do not apply this repair when asynchronous functions are already classified correctly, when ordinary function scope is inappropriate, or when current evidence identifies an unrelated parent-link or annotation-resolution defect.

## Operations and current probes

1. [Inspect scope classification and reproduce the failure](references/actions/inspect.md). Locate current semantic owners, inspect ordinary and asynchronous function handling, and connect the missing classification to the argument-binding path.
2. [Repair registration and add a regression](references/actions/repair.md). Use the current registry's ordinary-function representation and compatibility policy. Do not mask the terminal parent-traversal error.
3. [Validate the edit](references/actions/validate.md). Execute the public reproduction, regression, neighboring annotation tests, and an ordinary-function counterpart; review supported-runtime compatibility.

The [historical Workflow](references/workflow.md) defines dependencies and assurances. Its operation descriptions are evidence-grounded reconstructions, not a recorded historical command sequence.

## Binding and execution

Construct a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real owner bindings, observed PortValues, and current Oracle bindings. Historical paths are references, not current bindings.

Each current Oracle maps `action_id/source_oracle_id` to a public instruction, argv command, and public evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render these bound commands before execution. Empty commands in historical contracts are unbound placeholders, not executable authorization.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN authorizes probes only, not edits; a hard prerequisite failure rejects the plan. Structural PASS predicts compatibility, not repair success. Current evidence may justify omitting already satisfied operations, but every retained modifying Action retains its validation Action. Refresh stale observations after edits.

## Validation and stop conditions

Require corrected analysis of the annotated asynchronous function, without unexpected diagnostics, plus evidence that ordinary-function scope, adjacent annotation diagnostics, and supported-version import behavior remain intact. Recording outcomes alone does not prove these assurances.

Stop before editing if the missing-registration cause is not established. Stop and report failures or unknown checks if the reproduction still fails, adjacent behavior changes, or compatibility cannot be established. Do not weaken diagnostic assertions to obtain a pass.

Historical regression assertions were supplied; historical execution logs were not. The later qualification reports one fail-to-pass and eleven pass-to-pass cases **in changed test files only**. Whole-project regression and cross-project transfer are untested. This qualification is provenance, not a backdated historical event. Package eval definitions remain `not_executed`.

During formal evaluation, keep knowledge and checkpoints frozen, do not publish a current task plan as verified historical knowledge, and obtain independent hidden acceptance only after the solver stops. Hidden checks never become execution guidance. Time-reconstructed catalogs exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before query input time.

## Resources

- [Historical episode](references/episode.md)
- [Workflow](references/workflow.md)
- Evidence: [title](references/evidence/title.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression](references/evidence/regression.md)
- [Provenance](references/provenance.json)
- Evals: [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), [functional](evals/functional-cases.json)
