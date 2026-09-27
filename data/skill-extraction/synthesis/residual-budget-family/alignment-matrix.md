# Cross-case alignment matrix: shared-capacity and compaction families

## Decision key

- **direct**: the case demonstrates the same causal mechanism and a compatible oracle.
- **partial**: the case supports one Atomic in the family but not the whole Pattern.
- **adjacent**: useful neighboring mechanism; do not merge without new evidence.
- **rejected**: superficial lexical overlap only.

| Candidate mechanism | Hermes | DeepSeek | Pi | Aider | Promotion decision |
|---|---|---|---|---|---|
| Derive pressure from residual capacity after mandatory output reservation | direct | direct | not established | not established | Promote as reviewed Atomic candidate; Pattern remains provisional |
| Normalize optional reservation/capacity inputs | direct | direct through resolver validation | partial via safe integer settings | partial via input-limit handling | Promote as shared supporting Atomic after review |
| Propagate active capacity policy across model/runtime reconfiguration | direct | direct through routed policy resolution | direct | partial | Promote as reviewed Atomic candidate |
| Add pressure headroom and reuse it for summary output default | not evidenced | direct | not evidenced | not evidenced | Keep DeepSeek-specific Atomic candidate |
| Place pressure check immediately before a real next request | not evidenced | not evidenced | direct | not evidenced | Separate Pi Atomic |
| Account for all context-visible artifacts in budget measurement | not evidenced | not evidenced | direct | partial | Separate accounting Atomic |
| Select history that fits a summarizer input budget | not evidenced | not evidenced | not evidenced | direct | Adjacent Aider family |
| Preserve original context on summary failure | partial fallback behavior only | partial/adjacent | not evidenced | direct | Recovery Atomic, not residual-budget Pattern |

## Cross-case conclusion

The strongest validated family is narrower than “all compaction.” It is:

> **Residual-Budget Invariant:** when upstream work and a mandatory downstream reservation share one finite capacity, derive admission/pressure policy from the residual budget and replay the policy whenever the active capacity envelope changes.

Hermes and DeepSeek are direct realizations. Pi supports the propagation subproblem but is deliberately not counted as a third residual-arithmetic realization. Aider is a neighboring budget-aware summarization family.
