---
name: positional-only-annotation-traversal
description: "Repair Python unused-import false positives caused by omitted positional-only parameter annotations in a function-signature analyzer, after confirming the current AST traversal and compatibility requirements."
---

# Positional-only annotation traversal

Use this Workflow when an imported name used in a Python positional-only parameter annotation is incorrectly reported as unused, and current inspection shows that the function-signature analyzer collects ordinary and keyword-only arguments but omits positional-only arguments.

Canonical Skill/Workflow ID: `workflow:verified-history:b95b785d6a29c4b04e9050af`.

## Activation and exclusions

Activate for a report resembling:

```python
from datetime import datetime as Foo, time as Bar

def x(a: Foo, /, *, b: Bar):
    pass
```

The relevant symptom is an unused-import diagnostic for `Foo`, despite its annotation use.

Do not activate merely because an unused-import diagnostic mentions an annotation. Other causes—such as deferred annotation semantics, scope resolution, or unvisited return annotations—are outside this repair's demonstrated mechanism. Do not activate for a non-Python analyzer without a separately supported realization.

Clarify or probe if the runtime, AST representation, diagnostic, or responsible traversal is unknown. A supplied symptom alone does not establish applicability.

## Current probes and bindings

Before modifying code:

1. Record the public issue, pinned base revision, and hashes of inspected code anchors.
2. Locate the current semantic owners: the function-signature collector, Python-version compatibility gate, annotation regression tests, and public analyzer entry point.
3. Run or inspect a public reproduction on a runtime that supports positional-only syntax.
4. Determine whether positional-only parameter names and annotations are omitted while ordinary and keyword-only parameters are collected.
5. Bind current test and reproduction commands explicitly. Historical paths and commands are not current bindings.

Use [Inspect signature collection](references/actions/inspect.md). UNKNOWN prerequisites permit inspection only; a contrary mechanism finding rejects this Workflow.

## Operations

- [Inspect signature collection](references/actions/inspect.md) establishes current applicability.
- [Include positional-only annotations](references/actions/repair.md) edits the collector and adds a focused regression.
- [Validate annotation traversal](references/actions/validate.md) checks the repair, adjacent behavior, and runtime compatibility.

The [historical Workflow](references/workflow.md) records dependency requirements. A current task may omit an operation only when its effect is already established by fresh public evidence. Do not infer successful execution from a structurally compatible plan.

## Validation and stopping

On a positional-only-capable Python runtime, the focused regression must produce no unused-import diagnostic for an imported name used only in a positional-only annotation. Also check the mixed positional-only/keyword-only reproduction and relevant adjacent annotation tests.

Preserve ordinary and keyword-only annotation handling, parameter binding, defaults handling, and compatibility with older supported runtimes. A version guard must prevent access to AST fields absent on those runtimes; syntax-specific tests must be skipped or otherwise isolated appropriately.

Stop and reassess if:

- the current collector already processes positional-only annotations;
- the failure comes from a different annotation mechanism;
- owner bindings are ambiguous;
- a required public check cannot be run;
- adjacent tests regress; or
- supported-runtime compatibility is unresolved.

An unavailable check is UNKNOWN, not PASS.

## Evidence and limits

This is a single-repair Workflow, not a cross-project Pattern. Its evidence consists of the original report, the merged implementation, and the regression assertion in [the episode](references/episode.md).

The historical regression is an assertion present at the repair commit, not evidence of a historical test execution. A later qualification attestation reports one fail-to-pass and 24 pass-to-pass outcomes **only within changed test files**. Whole-project regression and cross-project transfer were not tested. That later attestation is provenance, not knowledge backdated before the cutoff.

Evaluation definitions are [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json); all remain `not_executed`.

For current use, retain observed PortValues and tri-state semantic checks. Map each source oracle to a current public instruction, argv command, and evidence references under `oracle:<action_id>:<source_oracle_id>`. Execute the bound commands, refresh observations invalidated by edits, and obtain independent hidden acceptance only after the solver stops. Hidden tests do not supply guidance. Freeze formal knowledge and checkpoints during evaluation.
