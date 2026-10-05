---
name: classvar-annotation-shape-safety
description: "Repair Python AST ClassVar recognition when an annotation discriminator assumes a Name node and crashes or misclassifies qualified Attribute forms."
---

# ClassVar annotation shape safety

## Activation and exclusions

Activate when a Python AST naming checker fails while recognizing class-variable annotations, and current evidence shows that a qualified annotation such as `typing.ClassVar[int]` supplies an Attribute where the discriminator assumes a Name. Qualified unsubscripted forms may also expose the same recognition gap.

An exception mentioning `.name` alone is insufficient. Request the public traceback, annotation example, and current code, or perform the inspection operation first.

Exclude runtime typing errors, arbitrary import-alias inference, qualifier identity resolution, unrelated AST attributes, and non-Python node representations. This workflow recognizes the syntactic spelling `ClassVar`; it does not prove that an arbitrary qualifier refers to the typing module.

## Current probes

[Inspect](references/actions/inspect.md) the current semantic owners:
- `annotation-classifier`: decides whether an assignment has a ClassVar annotation;
- `class-constant-naming-consumer`: uses that decision for naming classification;
- `annotation-naming-regressions`: public fixtures and diagnostic expectations.

Record a TaskContext containing the public issue, pinned base, hashed code anchors, real owner bindings, observed AST shapes, semantic checks, observed PortValues, and current public oracle bindings. Historical paths in the [episode](references/episode.md) are not current bindings.

Prerequisites and checks are PASS, FAIL, or UNKNOWN. UNKNOWN authorizes probes only. A hard mechanism mismatch rejects the repair; structural PASS predicts compatibility, not repair success.

## Operations

1. [Inspect the discriminator and AST shapes](references/actions/inspect.md).
2. When the mechanism is confirmed, [normalize and guard recognition and add regressions](references/actions/repair.md).
3. [Validate shape safety and naming diagnostics](references/actions/validate.md).

The [historical workflow](references/workflow.md) records the single source-supported realization. A current DAG may omit already satisfied operations only on current evidence. Every retained modifying operation must retain its explicit validation.

Before execution, map each `action_id` and `source_oracle_id` to a current public instruction, argv command, and evidence references. Record the semantic check as `oracle:<action_id>:<source_oracle_id>` and render the bound commands. Empty source command arrays require current binding; historical commands do not authorize execution.

## Validation and stopping

Check direct and qualified ClassVar, with and without subscripts. Require correct class-constant diagnostics as well as absence of exceptions. Preserve direct recognition and adjacent naming behavior. Probe non-annotated assignments and unsupported or non-ClassVar shapes for safe false results.

Stop if the current node API or classifier semantics differ, public checks cannot be bound, or validation fails. Do not catch AttributeError broadly or weaken diagnostic expectations. Any subsequent edit makes the validation observation stale and requires another validation.

## Evidence and limits

See the [episode and qualification audit](references/episode.md), [implementation](references/evidence/fix.md), [regression assertions](references/evidence/regression.md), and [provenance](references/provenance.json).

This is a Workflow, not a cross-project Pattern. Historical CI execution is unknown. Later independent qualification supports only the selected changed-test-file checks with original-base control; whole-project regression and cross-project transfer remain untested. This Skill's functional cases are definitions and remain `not_executed`.

During formal evaluation, freeze knowledge and checkpoints. Do not publish current task plans as newly verified history. Earlier-query admission excludes the query's own issue, fix, cluster, aliases, copied sources, and inputs unavailable before the query. Independent hidden acceptance occurs only after the solver stops.
