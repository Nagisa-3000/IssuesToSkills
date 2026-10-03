---
name: annotation-only-binding-redefinition
description: "Repair false unused-name redefinition diagnostics when an annotation-only declaration is incorrectly treated as defining an already imported name."
---

# Annotation-only binding redefinition

## Activate when

A static analyzer reports an unused-name redefinition for an annotation-only declaration of an imported name, such as:

```python
from a import b, c
b: c
print(b)
```

The relevant semantic distinction is between attaching a type annotation and assigning or defining a runtime value. This Skill applies conditionally when current inspection confirms that an annotation-only binding participates incorrectly in the analyzer's redefinition decision.

## Exclusions and clarification

Do not activate for ordinary assignments, annotation-plus-assignment, genuine repeated imports or definitions, or errors in annotation syntax. Do not infer that every annotated assignment should cease defining names.

Clarify when the report lacks a reproduction or does not distinguish `name: Type` from `name: Type = value`. If the current analyzer has no corresponding annotation-only binding abstraction, probe its semantics before attempting a repair; this historical workflow does not authorize inventing an adapter.

## Current probes and bindings

1. Pin the public checkout and record the public issue and reproduction.
2. Locate the semantic owners of annotation-only bindings, redefinition decisions, and annotation regression tests. Historical paths are documented only in [the episode](references/episode.md).
3. Inspect whether the annotation-only abstraction inherits a redefinition operation that can classify it as redefining a prior import.
4. Run a public reproduction and record actual diagnostics. Check both annotation-name usage and later usage of the imported value.
5. Bind each Action port to actual current artifacts. Record hashed code anchors, observed facts, semantic checks, PortValues, and current Oracle bindings.

Prerequisites are tri-state: PASS, FAIL, or UNKNOWN. UNKNOWN authorizes inspection and probes, not editing. Hard semantic failures reject this workflow.

## Operations

- [Inspect the annotation/redefinition path](references/actions/inspect.md).
- [Repair annotation-only redefinition semantics and add the regression](references/actions/repair.md).
- [Validate target and adjacent annotation behavior](references/actions/validate.md).

The [canonical historical workflow](references/workflow.md) describes the supported dependency structure. Current plans may omit operations already satisfied by fresh observations, but must retain validation for any modifying operation.

## Validation and stopping

Bind each historical Oracle to a public current instruction, argv command, and evidence references. Store its semantic check under `oracle:<action_id>:<source_oracle_id>` and render those bound commands before execution. No executable current command is supplied by this package.

Validate that:

- the annotation-only reproduction emits no diagnostics;
- the annotation type name is still processed normally;
- subsequent use of the imported value remains recognized;
- relevant pre-existing annotation tests continue to pass;
- true value-defining statements retain their redefinition behavior.

After editing, refresh invalidated observations. A structurally compatible plan predicts compatibility only, not repair success. Stop or revise the plan if the targeted reproduction still fails, adjacent behavior regresses, or the inspected owner does not implement the required semantics. Obtain independent hidden acceptance only after the solver stops; hidden checks do not enter these instructions.

## Evidence and limits

This is a single-source Workflow, not a multi-issue Pattern. [Historical evidence](references/episode.md) establishes the report, implementation change, and added test assertion. It does not establish that a historical test command was executed.

A later qualification attestation records one fail-to-pass case and 49 pass-to-pass cases within changed test files. It is not pre-cutoff learned content, and does not establish whole-project regression safety or cross-project transfer. See [provenance](references/provenance.json).

Evaluation definitions are packaged in [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites. They are **not executed**.

During formal evaluation, keep knowledge and checkpoints frozen and do not publish a current task plan as historical knowledge. Time-reconstructed catalogs must exclude the current issue, fix, cluster, aliases, copied sources, and sources unavailable before the query input time.
