# Evidence: Pi coding-agent compaction budgets and request-boundary timing

## Scope and provenance

Repository: `/home/chenyujia/tritonToLlvm/pi-agent`.

Verified commits:

- `46bde88a1cd752966aa2a357d292e83aff98b132` — `feat(coding-agent): support per-model compaction token budgets`
- `56700d42ed65a94a80af7376adb19a9298065164` — `fix(coding-agent): compact before post-tool model requests (#8782)`
- `a6f720e6caf1cf429e382011156c015fa204c512` — `fix(coding-agent): count custom messages in compaction budget`
- `75ac0cb0e637f752e4a4395f00e5094609c6527d` — `fix(coding-agent): stabilize auto-compaction threshold test`

Relevant implementation/test areas include:

- `packages/coding-agent/src/core/agent-session.ts`
- `packages/coding-agent/src/core/settings-manager.ts`
- `packages/coding-agent/test/settings-manager-compaction.test.ts`
- `packages/coding-agent/test/agent-session-compaction-model-overrides.test.ts`
- `packages/coding-agent/test/suite/agent-session-compaction.test.ts`

## Alignment decision

Pi is an important adjacent comparison, but it is not treated as a direct realization of the Hermes/DeepSeek residual-output-reservation Pattern without further code evidence. The commits establish three reusable mechanisms:

1. per-model compaction policy resolution and propagation;
2. placing the pressure check before a real next provider request, not after a terminating tool result;
3. counting all context-visible session entries, including custom messages, in budget measurement.

The first mechanism aligns with the propagation candidate. The second and third are distinct candidates. The repository evidence does not by itself establish the same residual-capacity formula as Hermes and DeepSeek.

## Case Actions

- `CA1`: resolve model-specific `reserveTokens` and `keepRecentTokens` with exact provider/model precedence and safe-integer validation.
- `CA2`: apply resolved policy consistently to manual compaction, automatic threshold checks, overflow recovery, extension-visible preparation, and model switching.
- `CA3`: schedule automatic compaction at the boundary immediately before a real next model request, while avoiding compaction after terminating tool results.
- `CA4`: measure budget from the complete context-visible session representation rather than only ordinary message entries.
- `CA5`: stabilize tests by deriving thresholds from the selected model and active settings rather than hard-coded constants.

## Negative/adjacent classification

- `CA1` and `CA2` are candidates for `replay-policy-parameter-across-reconfiguration` and `resolve-model-specific-policy-with-fallback`.
- `CA3` is a separate request-boundary timing Atomic.
- `CA4` is a separate complete-context-accounting Atomic.
- `CA5` is validation hygiene, not a production Atomic.

Pi is therefore included in the synthesis as a partial alignment and as a source of rejected false merges, not as proof of residual-budget arithmetic.
