---
name: resilient-disable-bookkeeping
description: "Repair Python diagnostic configuration processing when a missing numeric-message lookup in advisory bookkeeping prevents later configured disables from taking effect."
---

# Resilient disable bookkeeping

Use this conditional Workflow when configured diagnostic disables unexpectedly stop working and current public evidence traces the interruption to numeric-ID-to-symbol lookup in advisory bookkeeping.

This is a single verified historical realization, not a cross-project Pattern. Its canonical ID is `workflow:verified-history:ef9c08f5cc5fb6362cf0902b`.

## Activation and exclusions

Activate when:
- A Python diagnostic tool accepts a list of disabled message identifiers.
- Some numeric identifiers no longer resolve in the message registry.
- Advisory tracking of numeric identifiers raises `KeyError`, interrupting processing before a later valid disable takes effect.

Clarify when the only evidence is “disabled warnings reappeared.” That symptom alone does not establish this mechanism.

Do not activate for configuration-file discovery failures, precedence conflicts, checker emission bugs, or systems whose missing-identifier policy deliberately requires rejecting the entire configuration. Do not broadly suppress exceptions in the configuration loader.

## Current probes and bindings

Start with [the probe Action](references/actions/probe.md). Locate the current semantic owners rather than assuming historical paths:
- `disable-bookkeeping`: numeric-ID advisory registration.
- `message-registry`: ID-to-symbol resolution.
- `configuration-regression`: public tests for configured message suppression.

Record a current TaskContext containing the public issue, pinned base, hashed code anchors, observed facts, owner bindings, semantic checks, and current Oracle bindings. Check that the lookup is advisory, that `KeyError` represents an unresolved identifier, and that continuing configuration processing does not bypass a separately required rejection policy.

Use PASS/FAIL/UNKNOWN checks. UNKNOWN permits probes only; a failed mechanism prerequisite rejects the repair plan.

## Operations

1. [Probe the interrupted disable path](references/actions/probe.md).
2. [Guard advisory lookup failure](references/actions/guard.md).
3. [Add a mixed-identifier regression](references/actions/regression.md).
4. [Validate repair and adjacent behavior](references/actions/validate.md).

The [historical Workflow](references/workflow.md) supplies dependencies, not a mandatory textual execution order. For causal reproduction, install the regression on the pinned base and observe its failure before applying the repair when practical. If an equivalent regression already exists, its addition can be omitted from a current plan; repair validation cannot be omitted.

Keep the exception boundary local to advisory bookkeeping. Preserve successful numeric registration and ordinary symbolic disable handling. Do not copy historical release-version changes into a current repair.

## Validation and stopping

Bind each Action oracle to a current public instruction, argv command, and evidence references. Its semantic check key is `oracle:<action_id>:<source_oracle_id>`. Render the bound commands before execution. Historical commands and paths are evidence, not current execution authority.

Verify:
- An unresolved numeric identifier in the configuration does not prevent a later valid disable.
- The diagnostic remains observable when not disabled.
- Known numeric identifiers retain their advisory registration.
- Symbolic disables and neighboring configuration tests retain their behavior.
- Unrelated exceptions are not silently swallowed.

After modifications, refresh stale observations and run the retained validation Action. Stop if the exception is not the evidenced missing-lookup `KeyError`, if the lookup is not advisory, if required configuration policy would be weakened, or if adjacent behavior fails. Structural plan PASS predicts compatibility, not repair success.

Skill evaluation definitions are [activation](evals/activation-cases.json), [applicability](evals/applicability-cases.json), and [functional](evals/functional-cases.json); all are unexecuted. Independent hidden acceptance must occur after the solver stops without changing frozen formal knowledge or checkpoints.

## Evidence and limits

See [the episode](references/episode.md), [source provenance](references/provenance.json), and the linked evidence cards. The historical commit added assertions, but historical CI execution is unknown. A later independent qualification observed one regression fail-to-pass and seventeen adjacent pass-to-pass results, limited to changed-test qualification with original-base control. It did not establish whole-project correctness, cross-project transfer, or execution of this Skill's functional cases.

For time-reconstructed use, exclude the query's own issue, fix, cluster, aliases, copied sources, and sources unavailable before the query time. This package's historical source became available on 2021-03-30, not at the later qualification time.
