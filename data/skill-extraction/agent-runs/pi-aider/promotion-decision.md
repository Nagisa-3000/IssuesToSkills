# Promotion decision: Pi/Aider bounded-context run

## Decision

- **Evidence quality:** sufficient for a candidate bundle. Every selected action has a real commit SHA; Pi issue/PR provenance is recorded where the commit metadata provides it. Aider’s reviewed commits have no issue/PR marker in the local metadata, so they are explicitly commit-only.
- **Case Actions:** accepted as repository-specific instances. They are not labeled Skills.
- **Atomic candidates:** accepted as `candidate`, not `validated`.
- **Workflow candidates:** accepted as `candidate` for Pi and Aider-local variants.
- **Cross-repository Pattern:** **not promoted**.

## Why the Pi family is causal

`46bde88` resolves model-specific compaction settings and routes them through compaction callers. `56700d42` makes the next-request boundary the point where that policy is acted on. `8bdcd449` repairs the cut-point decision for an oversized trailing tool result at that boundary. `a6f720e` supplies the complete visible-entry accounting needed before selecting the boundary. Their code paths and test oracles form a causal chain: policy → measurement/boundary → continuation action.

## Why Aider is a related but different family

Aider’s `ff41f9bd`/`64470955`/`e61857ef` chain derives and propagates a history/summarizer input budget, selects a fitting prefix plus recent tail, and rechecks the result. `5c866c67` adds preservation and warning on summarizer failure. This is a coherent budget-and-recovery family, but it lacks the reviewed Pi property that pressure is gated specifically before a real next provider request and has no demonstrated downstream output reservation charged to the same capacity.

## Cross-repository alignment matrix

| claim | decision | reason |
|---|---|---|
| Both propagate an explicit capacity/budget into a downstream context operation | partial alignment | True in code, but the owners and semantics differ: Pi runtime compaction policy versus Aider summarizer history budget. |
| Both select context under pressure while preserving a recent/safe region | partial alignment | Pi preserves session/tool boundaries; Aider preserves a recent message tail and fits the summarizer prefix. |
| Both implement request-boundary compaction | rejected | Aider’s `summarize_start` is not a termination-aware provider request boundary. |
| Aider proves residual output reservation for Pi | rejected | No reviewed Aider implementation or oracle establishes the shared-capacity/output-reservation formula. |
| Both recover without silently dropping usable context | partial alignment | Aider explicitly keeps history and warns; Pi’s selected evidence preserves a valid boundary. Failure states and recovery seams are different. |

## Promotion gates still open

1. Run an independent held-out transfer on another implementation of bounded context pressure.
2. Add a dedicated Aider test that injects the exact `Coder.create` summarizer `ValueError` path and asserts original history identity/content plus `io.tool_warning`.
3. For a cross-repository Pattern, produce implementation evidence of the same capacity owner and boundary semantics, not just similar nouns.
4. Keep a negative/adjacent record for Aider when evaluating Pi’s request-boundary Atomic.

## Validation performed for this run

- `cases.json` parsed with Python’s JSON parser.
- IDs, evidence references, realization references, workflow edge endpoints, and DAG acyclicity checked by a local validation script.
- Markdown files checked for non-empty content and required section markers.
- The repository’s existing schema/unit tests were run separately from this artifact bundle; their result is reported by the parent task. No changes outside this directory were made.
