---
name: annotation-only-redefinition
description: "Repair false unused-name redefinition diagnostics when a Python annotation without a value is treated as a new definition of an imported name."
---

# Annotation-only redefinition

## Activate when

A Python static analyzer reports an unused-name redefinition at an annotation-only statement such as `item: Type`, although the name was imported earlier and is used afterward. The candidate mechanism is that an annotation binding inherits ordinary name-redefinition behavior.

This is a conditional repair workflow, not a rule to suppress all redefinition diagnostics.

## Exclusions and clarification

- Do not activate for an assignment with a value, such as `item: Type = replacement`, without separate evidence.
- Do not activate for a real second import, assignment, or function definition that replaces an unused binding.
- If the report does not distinguish annotation-only syntax from assignment, request a minimal public reproduction or inspect the AST.
- If the current analyzer has no equivalent annotation binding or redefinition predicate, stop rather than invent an adapter.
- Non-Python analyzers and unrelated annotation diagnostics are outside the demonstrated scope.

## Current probes and bindings

Use [the owner probe](references/actions/probe.md) to locate the current semantic owners:

1. The annotation-only binding representation.
2. The predicate determining whether a new binding redefines an earlier one.
3. Public annotation regression tests and their supported runner.

Record the pinned public base, hashed code anchors, observed diagnostic, semantic checks, actual bindings, PortValues, and public Oracle bindings in the current TaskContext. Historical paths in [the episode](references/episode.md) are references, not current bindings.

Prerequisites are tri-state: PASS permits the relevant operation, UNKNOWN permits probes only, and FAIL rejects the repair plan. A name match alone does not establish semantic compatibility.

## Operations

Follow [the historical workflow](references/workflow.md), adapting only after current evidence confirms the same mechanism:

- [Probe the annotation-only redefinition path](references/actions/probe.md).
- [Make annotation-only bindings non-redefining](references/actions/edit.md).
- [Add a public import/annotation/use regression](references/actions/regression.md).
- [Validate both modifications and adjacent behavior](references/actions/validate.md).

Already-satisfied operations may be omitted from a current plan, but every retained modification must retain its validation closure. Current ordering follows actual ports and prerequisites, not merely the historical list.

## Validation and stopping

Bind each Oracle to a public current instruction, argv command, and evidence references. Record its check under `oracle:<action_id>:<source_oracle_id>` and render those bound commands before execution. No historical command authorizes current execution.

Verify that an import followed by an annotation-only statement and use emits no false redefinition diagnostic. Run the relevant annotation tests and check that ordinary value-bearing definitions still receive their existing redefinition treatment. Refresh stale validation observations after edits.

Stop if the diagnostic cannot be reproduced, the owner differs semantically, the change alters ordinary binding behavior, or public validation fails. Structural compatibility does not establish repair success. Independent hidden acceptance belongs after the solver stops, not in this Skill's guidance.

## Evidence and limits

The historical implementation added `Annotation.redefines(self, other)` returning `False`; the regression asserted no diagnostics for an imported name annotated and then used. See [implementation evidence](references/evidence/fix.md) and [regression evidence](references/evidence/regression.md).

Historical tests are supplied assertions, not evidence of historical execution. A later qualification attestation reports one fail-to-pass and 49 pass-to-pass results in changed test files only. It is not pre-cutoff learned content; whole-project regression and cross-project transfer remain untested. [Provenance](references/provenance.json) records that distinction. All packaged eval definitions are `not_executed`.
