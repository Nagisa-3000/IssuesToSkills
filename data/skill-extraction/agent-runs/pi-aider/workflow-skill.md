# Workflow candidate: bounded-context pressure with safe continuation

**Status:** candidate. This is a semantic workflow DAG, not a commit timeline. It has two repository-local realizations and a partial cross-repository correspondence.

## Goal

When context pressure threatens a subsequent model operation, make the capacity policy explicit, measure the complete relevant input, select a safe retained boundary, perform the pressure action only at the correct continuation seam, and recover without silently destroying usable context.

## Inputs and produced state

- **Inputs:** active model/provider identity (when applicable), nominal input budget, pressure policy, context/session entries, continuation/termination state, and a failure policy.
- **Produced state:** validated resolved budget, measured pressure, safe retained boundary, either a compacted/fitted context or an unchanged original context, and an observable validation signal.

## DAG steps

### S1. Identify the real capacity owner (mandatory)

Determine which operation owns the relevant limit: a provider-facing session context (Pi) or a summarizer/history input budget (Aider). Do not infer that two numeric settings are interchangeable.

- Uses: A1/A5 as applicable.
- Produces: named capacity, measurement projection, and parameter provenance.
- Validation: implementation caller graph names the consumer of the budget.
- Failure: if the capacity owner is ambiguous, keep the candidate adjacent and do not merge it into the cross-repository pattern.

### S2. Resolve and validate policy (mandatory)

Resolve ordinary settings and exact model/provider overrides, or derive and accept an explicit history budget. Reject invalid values explicitly.

- Pi: `SettingsManager.getCompactionSettings(activeModel)`.
- Aider: `Model.__init__` plus `Coder.create` into `ChatSummary`.
- Produces: one inspectable policy value/object.
- Validation: precedence, invalid-value, and explicit-override tests.

### S3. Measure the complete relevant input (mandatory)

Use the same context-visible projection used by the operation that will consume the result.

- Pi: include custom/session entries before `findCutPoint`.
- Aider: tokenize the messages supplied to `ChatSummary`.
- Produces: measured pressure and candidate retained region.
- Failure: if the projection omits input visible to the consumer, stop; do not proceed to selection.

### S4. Select a safe retained boundary (mandatory)

Choose a boundary that preserves the consumer’s required structural invariants.

- Pi: latest valid assistant/tool-call boundary for oversized trailing tool results.
- Aider: fitting older prefix plus recent tail; preserve message-role constraints and recursively recheck summary+tail.
- Produces: `firstKeptEntry`/turn prefix or summary prefix/tail.
- Validation: exact cut-point or smaller-result oracle.

### S5. Gate the pressure operation at the correct seam (conditional)

For a provider-facing loop, perform compaction immediately before a real next request and skip terminal tool outcomes. For background history summarization, start only when the history exceeds its configured limit.

- Pi: required for request-boundary semantics.
- Aider: conditional history-summary worker; not equivalent to Pi request gating.
- Produces: compacted/fitted context ready for the next operation.
- Failure: if the operation will not be consumed (terminal turn), skip it.

### S6. Recover non-destructively (conditional)

If the pressure operation fails, keep the original usable context and emit an observable warning/event; retry only through a known fallback path.

- Pi variant: preserve a valid session boundary for oversized tails and use overflow/cancellation recovery paths.
- Aider variant: keep `done_messages`, warn on `ValueError`, and try the next summarizer model when configured.
- Validation: failure injection should assert original context identity/content plus an observable signal. Aider’s exact coder-switch warning injection is still a validation gap in this run.

## Repository-local realizations

- **Pi direct workflow:** S2 → S3 → S4 → S5, with S6 as the oversized-tail/overflow branch. The `#8133`, `#8782/#6879`, `#9740`, and `#6326` evidence units support this graph.
- **Aider adjacent workflow:** S2 → S3 → S4, with S6 as summary failure/fallback. The four reviewed commits support this graph, but no Pi-style terminating-provider-request branch is present.

## Guards and non-goals

- Do not turn a commit sequence into a DAG edge solely because one commit came later.
- Do not equate `reserveTokens` with `max_chat_history_tokens`.
- Do not claim a shared residual-output-reservation invariant without code showing downstream output reservation charged against the same capacity.
- Do not claim successful LLM output, latency, or token numbers beyond checked-in test fixtures/oracles.
- Do not run a compaction/summarization operation after a terminal action that will not issue another model request.

## Validation ladder

1. **Static provenance:** commit SHA, issue/PR marker where present, path, symbol, caller, and test file.
2. **Local oracle reading:** inspect assertions, including negative termination and fallback cases.
3. **Schema/JSON checks:** parse `cases.json`, verify unique IDs and DAG references, reject cycles.
4. **Held-out transfer (not done):** apply the abstract workflow to a new bounded-context implementation without using its target patch as the oracle.

The workflow therefore remains a candidate with strong repository-local evidence and partial cross-repository alignment.
