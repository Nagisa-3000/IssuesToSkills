---
name: assignment-definition-redefinition
description: "Repair a Python static analyzer that misses an unused assignment overwritten by a same-name function or class definition, when its binding model and diagnostic policy support definition-to-assignment redefinition."
---

# Assignment hidden by a definition

Use this conditional Workflow when a Python static analyzer fails to report an unused assignment that is subsequently overwritten by a same-name definition. The historical motivating report concerned a class attribute hidden by a method; the actual repair operated on the analyzer's shared definition-binding abstraction.

## Activation conditions

Activate when current public evidence shows all of the following:

- An assignment creates a binding, and a later function or class definition creates a binding with the same name.
- The analyzer has an unused-redefinition diagnostic but misses this collision.
- The binding model represents definitions and assignments separately and has a directional redefinition predicate or equivalent semantic owner.
- Existing policy, rather than a new blanket ban on assignment, is intended to determine whether the collision is reportable.

If the binding model or diagnostic policy is unknown, inspect it first. A matching issue description alone does not establish applicability.

## Exclusions

Do not apply this repair to ordinary assignment followed by assignment, runtime attribute writes, or an unrelated undefined-name diagnostic. Do not infer that every class attribute reassignment must be rejected. Do not transfer the implementation to a different language or an incompatible binding model without separately supported evidence.

The source regression explicitly covers assignment followed by a function definition. Class-definition behavior follows the shared implementation owner but has no dedicated regression assertion in the supplied evidence.

## Current probes and operations

1. [Inspect the binding collision](references/actions/inspect.md): locate current semantic owners, reproduce the missed diagnostic, and inspect existing redefinition behavior.
2. [Extend definition-side recognition and add a regression](references/actions/repair.md): preserve the inherited rule and additionally recognize a same-name assignment as redefined by a definition.
3. [Validate the repair](references/actions/validate.md): run the public regression and adjacent checks using commands bound to the current checkout.

The historical mechanism and dependencies are in [the Workflow](references/workflow.md). The motivating report, implementation, and historical assertions are summarized in [the episode](references/episode.md).

## Binding and validation discipline

Before editing, create a current TaskContext with the public issue, pinned base, hashed code anchors, real owner bindings, observed facts, semantic checks, and observed PortValues. Bind each oracle to a current public instruction and argv command; record its check as `oracle:<action_id>:<source_oracle_id>`. Render those bound commands before executing them.

Historical resource locations are not current bindings. Unknown prerequisites authorize inspection only. A hard semantic mismatch rejects this Workflow. Structural compatibility does not establish repair success.

After editing, invalidate earlier diagnostic observations, refresh code anchors, and execute the public checks. Validate both the newly recognized collision and adjacent behavior: existing definition redefinitions, different-name bindings, and ordinary assignment rebinding. Check the motivating class-body example separately. Interpret policy-sensitive examples using the current analyzer's existing unused-binding and scope rules, not a blanket duplicate-name prohibition.

Stop if the semantic owner cannot be located, the analyzer deliberately permits this collision, the inherited predicate cannot be preserved, or adjacent checks regress. Missing executable test infrastructure leaves validation UNKNOWN rather than successful.

## Evidence and limits

This is one focused, single-repair Workflow, not a cross-project Pattern. [Provenance](references/provenance.json) records the authoritative source and the later qualification attestation. The qualification covered changed test files only: one fail-to-pass case and 127 pass-to-pass cases. Whole-project regression and cross-project transfer were not tested.

Historical test code is evidence of assertions available at the repair commit, not proof of historical test execution. Package [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with status `not_executed`.

During formal evaluation, keep this knowledge and its checkpoints frozen. Do not publish a current task plan as newly verified historical knowledge. Time-reconstructed catalogs must exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query time. Obtain independent hidden acceptance only after the solver stops; hidden tests do not supply commands or guidance here.
