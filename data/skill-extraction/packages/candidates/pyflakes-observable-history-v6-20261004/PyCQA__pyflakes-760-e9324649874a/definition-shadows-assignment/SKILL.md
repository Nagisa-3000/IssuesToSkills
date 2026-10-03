---
name: definition-shadows-assignment
description: "Repair a Python static checker's missed unused-name redefinition when a function or class definition replaces a same-name assignment, while preserving existing redefinition rules."
---

# Definition shadows assignment

This conditional Workflow Skill is grounded in one verified historical repair. Its canonical ID is `workflow:verified-history:ee79eebf2283561900232caf`.

## Activate when

- A Python static checker reports unused definition-over-definition redefinitions but misses a definition that replaces a same-name assignment.
- The current binding model distinguishes assignments from function/class definitions and delegates redefinition classification through a binding predicate.
- The requested behavior is compatible with the checker's existing unused-binding diagnostic policy.

The historical report concerned a class attribute hidden by a method. The supplied regression also covers a module-level assignment hidden by a function. Do **not** restrict the proposed correction to class bodies merely because the original report used a class example.

## Exclusions and clarification

Do not activate for ordinary assignment-to-assignment rebinding alone, runtime attribute lookup, inherited attribute collisions, or a request to ban every class-body reassignment.

Clarify if the current symptom is ambiguous or the current checker has a different diagnostic policy. Stop if there is no compatible binding abstraction, if current tests show the earlier binding is intentionally exempt, or if a broader language adapter would be required. This Skill does not supply an adapter or cross-project verification.

## Current probes and bindings

Use the [locate-and-probe Action](references/actions/locate-and-probe.md) to locate these semantic owners in the current public checkout:

- `binding-redefinition-owner`: definition binding and its existing redefinition predicate.
- `assignment-binding-owner`: assignment binding representation.
- `unused-redefinition-tests-owner`: public diagnostic regression tests.

Establish current public reproductions for assignment → same-name definition and definition → same-name definition. Inspect ordinary rebinding and exemptions before editing. Record the pinned base, hashed anchors, owner bindings, observed facts, and current oracle commands in the TaskContext.

Unknown prerequisites authorize read/probe work only. A failed compatibility prerequisite rejects the edit plan. Historical paths and commands are not current bindings.

## Operations

1. [Locate owners and establish applicability](references/actions/locate-and-probe.md).
2. [Extend definition redefinition and add regression coverage](references/actions/extend-and-cover.md), only after applicability is established.
3. [Validate the candidate and adjacent behavior](references/actions/validate.md), retaining validation for the modifying Action.

The [canonical Workflow](references/workflow.md) declares dependencies and required assurances. Ordering follows current dependencies, not merely historical list position.

## Validation and stop conditions

Bind each oracle to public current instructions and argv commands. Render those commands before execution; historical examples do not authorize execution against a different checkout. Oracle semantic checks use `oracle:<action_id>:<source_oracle_id>` and have PASS, FAIL, or UNKNOWN status.

Require:
- The assignment → same-name definition public regression emits the intended unused-redefinition diagnostic.
- Existing superclass redefinition rules remain effective.
- Ordinary assignment → assignment rebinding is not turned into a blanket redefinition error.
- Public tests selected for the affected binding and diagnostic logic pass.

After an edit, refresh stale validation observations. A structurally compatible plan is not evidence of repair success. Stop on failed adjacent checks; revise or report the incompatibility rather than broadening the rule without evidence. Independent hidden acceptance belongs after the solver stops, not in these public oracle commands.

## Evidence and limits

See the [episode](references/episode.md), [report](references/evidence/body.md), [implementation](references/evidence/fix.md), and [regression assertion](references/evidence/regression.md).

The historical implementation extends a shared definition-binding predicate, not a class-only duplicate-attribute scan. The historical test is an assertion present at the repair commit; supplied historical evidence does not establish that a test command ran then.

A later qualification attestation reports one fail-to-pass and 127 pass-to-pass cases for changed test files with original-base control. Whole-project regression and cross-project transfer remain untested. That attestation is recorded in [provenance](references/provenance.json), not backdated into historical evidence.

All [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions with `status: not_executed`.
