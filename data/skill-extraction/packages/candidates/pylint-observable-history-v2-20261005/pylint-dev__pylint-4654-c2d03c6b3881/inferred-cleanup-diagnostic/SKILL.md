---
name: inferred-cleanup-diagnostic
description: "Repair a Python resource-management diagnostic false positive for resource-producing calls directly passed to an inferred standard-library ExitStack.enter_context method."
---

# Inferred cleanup diagnostic

## Activation and exclusions

Activate when a Python static-analysis checker warns about a resource-producing call directly passed to standard-library `ExitStack.enter_context`, and public current evidence confirms the immediate parent-call structure and inferred callable identity.

This Skill changes the checker, not application resource management. It recognizes a narrowly supported cleanup-registering parent call rather than proving general resource lifetimes.

Clarify when the warning location, AST relationship, or inferred callable identity is unknown. Do not activate for:
- Bare resource allocation merely located inside an `ExitStack` block.
- Arbitrary methods whose attribute spelling is `enter_context`.
- Custom wrappers, indirect registration, async cleanup, or ancestor-based lifetime analysis.
- Blanket diagnostic suppression.
- A checkout where the supported exception already works.

## Current probes

Use [Inspect](references/actions/inspect.md) to locate the current resource-diagnostic owner, AST call representation, safe-inference utility, and public diagnostic-test owner. Bind semantic roles rather than copying historical file paths.

Record a TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, semantic checks, real bindings, observed PortValues, and current Oracle bindings. Confirm:
1. The warning concerns the resource-producing call.
2. Its immediate parent is a call to the registration method.
3. Safe inference identifies a supported standard-library implementation.
4. The current warning gate lacks the relevant exemption.
5. Public adjacent controls exist or can be bound.

Use PASS/FAIL/UNKNOWN checks. Unknown prerequisites authorize probes only; hard failures reject the modifying plan. Predicate labels alone do not establish semantic compatibility.

## Operations and dependencies

1. [Inspect current diagnostic and inference](references/actions/inspect.md).
2. [Repair the narrow exemption and add a regression](references/actions/repair.md).
3. [Validate target and adjacent behavior](references/actions/validate.md).

The [Workflow](references/workflow.md) records the historical mechanism and dependencies. Current ordering follows ports, prerequisites, semantic evidence, and validation requirements, not historical list position. Already satisfied operations may be omitted only when their effects and bindings have current evidence; validation remains required after any modifying operation.

Historical paths and assertions are in the [episode](references/episode.md).

## Validation and stopping

Bind every current Oracle to its Action ID and source Oracle ID, with a public current instruction, argv command, and evidence references. Its TaskContext semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render bound commands before execution. Empty commands in the historical contracts require current binding; they do not authorize execution.

After editing, refresh stale observations. Run the public target regression and adjacent controls. Confirm that unmanaged allocation still warns, ordinary `with` usage remains exempt, and failed inference or unsupported parent structure does not grant the new exemption.

Stop if APIs cannot be safely bound, identity or parent structure differs from the supported mechanism, the regression cannot distinguish broken from corrected behavior, or adjacent behavior regresses. Do not invent adapters or broaden recognized identities without separate evidence. Structural plan PASS predicts compatibility, not repair success.

After the solver stops, obtain independent hidden acceptance where applicable. Never use hidden tests or gold-derived commands as guidance. Do not publish the current task plan as newly verified historical knowledge during formal evaluation. Formal knowledge and checkpoints remain frozen.

## Evidence and limits

This is one focused Workflow supported by one repair, not a Pattern or a claim of cross-project transfer. See the [report](references/evidence/body.md), [implementation](references/evidence/fix.md), [regression](references/evidence/regression.md), [title](references/evidence/title.md), and [provenance](references/provenance.json).

Historical CI/test execution is unknown. The committed regression is an assertion available at the historical revision, not proof of historical execution.

The supplied later independent qualification includes original-base, base-with-regression, and historical-fixed controls with consistent runtime identity. It establishes one regression-added fail-to-pass result and 17 original-to-fixed pass-to-pass results within its changed-test-files scope. It does not establish whole-project correctness, cross-project transfer, or execution of this Skill's evals. All authored eval suites are `not_executed`.

Time-reconstructed catalogs must exclude the current query's own issue, fix, cluster, aliases, copied sources, and any discovery source unavailable strictly before query time.
