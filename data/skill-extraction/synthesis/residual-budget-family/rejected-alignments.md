# Rejected and adjacent alignments

## Pi: not a third residual-arithmetic proof

Per-model reserve/keep settings and policy propagation align with AT3. The reviewed commits do not establish the same provider-enforced residual-capacity formula. Timing-before-next-request and complete-context accounting are separate Atomics.

## Aider: neighboring summarizer-budget family

Aider fits history to a summarizer input limit and has graceful fallback. It does not establish a mandatory downstream output reservation charged against the same capacity. Keep separate.

## DeepSeek summary cap: not equal to request reservation

The summary `maxTokens` default derived from headroom is a separate policy. Do not conflate auxiliary summary output cap with the routed request output reservation unless the implementation proves they share the same contract.

## Commit-level decomposition: not one Skill per commit

The six DeepSeek commits and the Hermes diff are evidence for semantic Case Actions. Commit chronology is not the Workflow. A single PR can realize multiple Atomics and one Workflow.

## File/function names: not Skill identity

Class names, paths, and function names are implementation bindings only. Skill identity is defined by problem mechanism, invariants, inputs/outputs, and behavior-level oracles.
