---
name: inferred-staticmethod-diagnostics
description: "Repair false method-argument diagnostics when a Python decorator resolves to builtins.staticmethod under an alias or a wrapper, while preserving ordinary method diagnostics."
---

# Inferred staticmethod diagnostics

## Activation

Activate when a Python static-analysis checker reports a missing receiver or missing method argument on a class function decorated through an alias of `staticmethod`, or through a decorator whose inferred result is a static method.

This is a conditional, single-history Workflow, not a cross-project Pattern. The supported mechanism is a local checker correction: consult inferred decorator identity before falling through to ordinary method-argument checks.

Clarify when the diagnostic is known but the decorator's inferred identity is not. Do not activate for runtime descriptor failures, arbitrary decorator inference bugs, classmethod repairs, or unrelated signature checks.

## Current probes and bindings

Before editing:

1. Pin the current public base and locate the semantic owners:
   - `method-argument-checker`: the method receiver/argument diagnostic decision chain.
   - `decorator-identity-provider`: the API that exposes inferred decorator qualified names.
   - `method-argument-regressions`: public fixtures and expected diagnostic assertions.
2. Record hashed code anchors and current observations. Verify that the decorator identity provider exposes `builtins.staticmethod` for the affected case.
3. Reproduce the unwanted diagnostic, and inspect the ordinary instance-method and direct-staticmethod branches.
4. Establish public current Oracle bindings with instructions, argv commands and evidence references. Historical paths and commands in [the episode](references/episode.md) are context, not executable current bindings.

An unknown prerequisite authorizes investigation only. A failed identity or owner check rejects the repair plan.

## Operations

Use the contracts in dependency order:

- [Probe the decision boundary](references/actions/probe.md).
- [Repair the inferred staticmethod branch and regression fixtures](references/actions/repair.md).
- [Validate diagnostics and preservation](references/actions/validate.md).

The [historical Workflow](references/workflow.md) describes the supported realization. Current ordering follows bindings and prerequisites, not a blindly copied historical file order.

## Validation and stop conditions

Require public checks showing:

- No `no-self-argument` or `no-method-argument` for supported aliased/inferred static methods.
- Ordinary malformed instance methods still produce their expected diagnostics.
- Direct staticmethod and existing classmethod/argument behavior remain unchanged.

Keep the existing direct-staticmethod handling ahead of the inferred-staticmethod exemption. Do not globally disable diagnostics, rewrite user methods to add `self`, or infer staticmethod semantics from decorator spelling alone.

Stop if the current inference API cannot establish the qualified identity, the proposed exemption suppresses ordinary method warnings, or adjacent checks fail. Refresh validation observations after every modification. Structural compatibility is not repair success.

## Evidence and limits

See [the episode](references/episode.md), [provenance](references/provenance.json), and the packaged [title](references/evidence/title.md), [report](references/evidence/report.md), [implementation](references/evidence/implementation.md), and [regression](references/evidence/regression.md).

The committed regression assertions are historical evidence; historical CI/test execution is unknown. A later independent qualification supports only its stated scope and does not execute this Skill's evaluations. All [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json) suites remain `not_executed`.

The report's `TYPE_CHECKING` example is contextual motivation, not proof that every conditional decorator arrangement is supported. Only use this mechanism when current inference establishes staticmethod identity. No whole-project or cross-project correctness claim is made.
