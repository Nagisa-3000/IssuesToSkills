---
name: missing-call-argument-guard
description: "Conditionally repair a Python static-analysis checker that crashes while extracting a missing call argument, preserving ordinary argument diagnostics and recognizing direct or inferred keyword arguments."
---

# Missing call argument guard

This is a focused Workflow Skill, not a cross-project Pattern. Its historical support is one verified repair.

## Activation

Activate when public evidence shows a Python static-analysis checker crashing because an argument-extraction helper raises a missing-argument exception. The checker should inspect a particular argument value, not enforce the callable's signature itself.

The supported mechanism includes:
- looking up a known positional slot and its corresponding keyword;
- handling absent arguments locally;
- trying the existing keyword-unpacking inference helper;
- returning without the specialized warning when the target argument cannot be recovered;
- distinguishing direct argument evidence from inferred keyword evidence.

Ask for clarification or run read-only probes when the exception owner, target parameter, inference helper, or diagnostic responsibilities are unknown.

Do not activate for runtime application argument handling, unrelated inference crashes, non-Python implementations, or a request to suppress ordinary missing-parameter diagnostics.

## Current probes and bindings

Before editing, record a TaskContext with the public issue, pinned base, hashed code anchors, observed facts, semantic checks, current owner bindings, observed PortValues if any, and current Oracle bindings.

Locate semantic owners rather than copying historical paths:

- `call-value-checker`: the specialized call checker and its missing-argument lookup;
- `argument-resolution-helpers`: argument extraction and keyword-unpacking inference;
- `call-checker-regression-suite`: public functional fixtures and expected diagnostic records;
- `public-test-runner`: the current repository's public test entry point.

Confirm the target parameter name, missing-argument exception type, helper behavior, diagnostic confidence semantics, and separation from ordinary signature checking. See [inspect](references/actions/inspect.md).

Checks are PASS, FAIL, or UNKNOWN. UNKNOWN prerequisites authorize probes only. A hard applicability failure rejects the repair plan.

## Operations

1. [Inspect current owners and failure](references/actions/inspect.md).
2. [Guard argument resolution](references/actions/repair.md).
3. [Add public edge-case regressions](references/actions/regressions.md).
4. [Validate repair and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) describes the sourced realization. Current ordering is determined by prerequisites, semantic dependencies, and verification closure, not merely by list order. Already satisfied operations may be omitted only if their required effects have current evidence; modifying operations retain validation.

## Validation

Bind each Oracle to a public current instruction, argv command, and evidence references. The semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Historical commands in references are evidence, not authorization to execute them unchanged.

Verify:
- an omitted argument does not crash analysis and still receives ordinary signature diagnostics;
- direct positional and correct keyword values retain the specialized diagnostic;
- an inferable unpacked keyword receives the appropriate inference confidence;
- unrelated values and wrong keywords do not produce the specialized warning;
- aliases, uninferable objects, and adjacent copy behavior remain correct.

Refresh validation observations after edits. Structural plan PASS predicts compatibility, not repair success. Stop after public validation and obtain independent hidden acceptance without importing hidden checks into guidance.

## Stop conditions and limits

Stop or narrow the task if helpers have incompatible semantics, the specialized checker owns signature enforcement, current confidence conventions differ materially, or the proposed catch would hide unrelated failures. Do not catch all exceptions or alter global inference behavior.

Historical CI/test execution is unknown. Later independent qualification supports only the supplied changed-test-file scope, not whole-project correctness or cross-project transfer. Skill functional cases are definitions and remain unexecuted.

See [episode](references/episode.md), [provenance](references/provenance.json), and the [functional definitions](evals/functional-cases.json).
