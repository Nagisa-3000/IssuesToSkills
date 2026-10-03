---
name: mutually-exclusive-binding-branches
description: "Repair false-positive unused-name redefinition diagnostics when a Python static analyzer fails to recognize separate match-case bodies as mutually exclusive alternatives."
---

# Mutually exclusive binding branches

Use this Workflow when a Python static analyzer reports an unused-name redefinition for same-named definitions in **different cases of one structural pattern match**, while equivalent `if`/`else` alternatives are already handled correctly.

The repair mechanism is to extend the analyzer's existing alternative-branch classifier, not to suppress redefinition diagnostics globally.

## Activation and exclusions

Activate when public code and a reproduction indicate that:
- repeated definitions occur in different case bodies of one `match`;
- the diagnostic is caused by missing match alternatives in an existing branch classifier; and
- the current analyzer uses that classifier to distinguish mutually exclusive bindings.

Clarify or probe when the diagnostic, responsible classifier, or branch relationship is unknown. Do not activate for sequential definitions in the same case, definitions in unrelated matches, pattern-capture analysis, or a checker without an equivalent alternative-branch mechanism.

One verified repair supports this Workflow. It is not a cross-project Pattern.

## Current probes and operations

1. [Locate and inspect the alternative-branch owner](references/actions/inspect.md). Reproduce the public diagnostic and compare match cases with existing `if`/`else` handling.
2. [Extend alternatives and add a regression](references/actions/repair.md), only after current probes establish the mechanism. Locate owners by semantic role; historical file paths are reference material, not current bindings.
3. [Validate the repair and adjacent behavior](references/actions/validate.md). Every modification requires this explicit validation step.

The [canonical historical Workflow](references/workflow.md) records dependencies, not an unconditional current task script. Drop an operation only when current evidence shows it is already satisfied or inapplicable.

## Current execution requirements

Before editing, obtain a current TaskContext with the public issue, pinned base, hashed code anchors, real owner bindings, observed facts and PortValues, and tri-state semantic checks. Bind each historical oracle to a current public instruction and argv command. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`.

Render and execute the **current bound commands**; no executable command is prescribed by this historical package. UNKNOWN prerequisites permit probes only. FAIL on a mechanism prerequisite rejects this repair plan. A structural PASS indicates compatibility, not repair success.

After editing, refresh invalidated observations and run the bound public checks. Formal evaluation knowledge and checkpoints remain frozen; do not publish a current task plan as newly verified history. Independent hidden acceptance, if used by the host, occurs after the solver stops.

## Validation and stopping

Require the supplied public match regression to produce no redefinition diagnostic, verify the `if`/`else` comparison, and check that legitimate redefinition diagnostics remain intact. Review preservation of existing `if` and `try` alternative classification and supported Python-version behavior.

Stop if cases cannot be mapped to separate alternative bodies, the current mechanism differs materially, or the edit would require global suppression. Do not infer match exhaustiveness, definite assignment, or correctness of pattern captures from this repair.

## Evidence and limits

See [episode](references/episode.md), [provenance](references/provenance.json), and the packaged [implementation](references/evidence/fix.md) and [regression](references/evidence/regression.md) evidence.

The historical regression is a test assertion added at the repair commit; historical execution was not supplied. A later qualification observed one fail-to-pass and seven pass-to-pass results **in changed test files only**. Whole-project regression and cross-project transfer remain untested. All packaged eval definitions are `not_executed`.
