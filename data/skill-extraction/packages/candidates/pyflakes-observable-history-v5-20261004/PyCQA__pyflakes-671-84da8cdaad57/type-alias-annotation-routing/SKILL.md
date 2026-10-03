---
name: type-alias-annotation-routing
description: "Repair a Python static analyzer that treats an explicit TypeAlias initializer as an ordinary value and consequently misses names inside a quoted type expression."
---

# Type-alias annotation routing

## Activation

Use this workflow when a Python static analyzer reports an imported type as unused even though it appears inside the quoted initializer of an explicitly annotated `TypeAlias` assignment.

A characteristic public reproduction is:

```python
from os import PathLike
from typing_extensions import TypeAlias

PathLikeStr: TypeAlias = "PathLike[str]"
```

The supplied historical report contrasted this failure with working quoted function annotations. This is a focused, single-repair workflow, not evidence of a general cross-project pattern.

## Exclusions and clarification

Do not activate solely because an arbitrary string mentions an imported name. Ordinary string values must not automatically become type expressions.

Clarify or probe when:

- The declaration's marker has not been resolved to the typing `TypeAlias` construct.
- The affected analyzer uses a different AST or type-alias representation.
- It is unknown whether annotation handling already parses and resolves quoted type expressions.
- The failure involves a newer type-alias statement rather than an annotated assignment.

Do not treat an unrelated object named `TypeAlias` as sufficient evidence of applicability. Reuse the current analyzer's typing-aware recognition mechanism; do not substitute spelling-only recognition.

## Current probes and bindings

Before editing, record the public issue, pinned base revision, hashed code anchors, real semantic-owner bindings, observed facts, PortValues, and current oracle bindings. Historical paths are documented only in [the episode](references/episode.md).

Resolve these semantic owners in the current checkout:

- `annotated-assignment-dispatch`: the handler that processes target, annotation, and optional initializer.
- `typing-marker-recognition`: the scope-aware helper that identifies typing constructs.
- `annotation-processing`: the existing annotation/forward-reference processing path.
- `type-annotation-regressions`: the public regression suite covering annotation name usage.

Use [inspect routing](references/actions/inspect.md) to establish applicability. Unknown prerequisites permit probes, not edits. A hard semantic mismatch rejects this workflow.

## Operations

The [historical workflow](references/workflow.md) links:

1. [Inspect routing and reproduce](references/actions/inspect.md).
2. [Route TypeAlias initializers and add regressions](references/actions/repair.md).
3. [Validate routing and preserved behavior](references/actions/validate.md).

The repair changes only the treatment of a present initializer when its annotation is recognized as `TypeAlias`. It sends that initializer through the existing annotation path, leaving ordinary initializer handling and no-initializer behavior intact.

The regression work belongs to the same modifying Action as the implementation change; its explicit validation Action remains mandatory.

## Validation and stop conditions

Bind each source oracle to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Historical snippets and commands are evidence, not authorization to execute an unadapted command.

Check:

- Quoted and unquoted explicit aliases use their imported type names.
- Both module and class-body aliases behave correctly.
- A declaration without an initializer does not consume an otherwise unused type import.
- Non-TypeAlias annotated values retain ordinary value handling.
- The original quoted-function-annotation behavior remains intact.

Use PASS/FAIL/UNKNOWN for current checks. Structural PASS predicts compatibility only, not repair success. After editing, refresh invalidated observations and execute the public checks. Stop on an unresolved typing-marker binding, a failing preservation check, or an unavailable validation oracle. Do not claim completion on UNKNOWN validation.

Independent hidden acceptance is obtained only after the solver stops; hidden tests and gold-derived commands must never enter this guidance. Formal knowledge and checkpoints remain frozen during evaluation.

## Evidence and limits

See [the evidence cards](references/episode.md#evidence) and [provenance](references/provenance.json). The historical regression additions are assertions available at the fix commit; the supplied core evidence does not establish their execution at that historical time.

A later qualification attestation reports one fail-to-pass and 51 pass-to-pass cases, scoped to changed test files with original-base control. It is contemporary provenance, not pre-cutoff learned content. Whole-project regression and cross-project transfer remain untested.

The [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites are definitions only and are `not_executed`.
