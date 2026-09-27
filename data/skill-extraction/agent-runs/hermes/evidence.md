# Hermes compaction/context-pressure extraction: evidence ledger

**Run scope.** This run reads only the local Git history and working tree of `/home/chenyujia/tritonToLlvm/hermes-agent`. It deliberately writes its output under `arex-skill-graph/data/skill-extraction/agent-runs/hermes/` and does not edit existing `data/skill-extraction/cases/` or `synthesis/` artifacts. The four selected changes are related by a concrete mechanism—keeping compaction pressure and retained context below a model/provider capacity envelope—but are kept as separate Cases.

## Repository provenance

- Repository: `/home/chenyujia/tritonToLlvm/hermes-agent`
- Evidence was read from parent and child trees with `git show <parent>..<commit> -- <path>` and from the post-change call sites/tests.
- Selected commits (full hashes):
  - `623b21bf24ea3f2f2c2d90de3ae872b8a0a000c4` (parent `065946d84f9ce31b7eb51380c9641c5038f291c4`), 2026-06-22: output reservation in compaction threshold.
  - `4252aecc2ed88dc69e9b0f60af796612f1feeada` (parent `a42aee9585dd8d3a4bfb329a0db44ba6cbe3a294`), 2026-08-16 author / 2026-08-31 commit: cap floor-trigger near minimum context windows.
  - `b7803a1763558f3125834282cf17810ab2b4aa73` (parent `25d88ad0c44ccf0dcf8228f184b5a495c16b9f9f`), 2026-09-21: cap protected tail and its soft ceiling as a fraction of the context window.
  - `af0be164c1d287ebc742d1b8376d82e5fb42fda5` (parent `9a18c8de43cf7e513c4d402b5003fd1c4e7f3082`), 2026-09-19: unify trigger derivation for installation and switch-guard preview.

## Evidence units

### EU-623-D1 — reservation arithmetic (implementation diff)

`agent/context_compressor.py`, class `ContextCompressor`:

- Before: `_compute_threshold_tokens(context_length, threshold_percent)` computed percentage/floor from the nominal window.
- After: it accepts `max_tokens`, computes `effective_window = context_length - (max_tokens or 0)`, and applies the small-window guard and threshold arithmetic to that effective input budget. The implementation explicitly treats `None` as provider-default/no known reservation.
- `_coerce_max_tokens(value)` converts only a positive integer-like reservation into an internal reservation; `None`, non-positive, and malformed values become no reservation. The exact coercion behavior is tested, not inferred from the commit title.
- The guard for a non-positive effective window returns a positive safe behavior rather than allowing a non-positive threshold.

### EU-623-D2 — construction and reconfiguration call sites

- `agent/agent_init.py`, `init_agent`: passes `agent.max_tokens` when constructing `ContextCompressor`.
- `agent/context_compressor.py`, `ContextCompressor.update_model`: accepts an optional new `max_tokens`, preserves the existing reservation when omitted, and recomputes the derived threshold after model/context changes.

### EU-623-T — numeric and malformed-input oracle

`tests/agent/test_context_compressor.py` adds/maintains tests including:

- `test_max_tokens_reservation_lowers_threshold`: `200000, 0.50, 65536` gives effective budget `134464` and threshold `67232`; no reservation remains `100000`.
- `test_max_tokens_reservation_with_small_window_floors`: reservation interacts with the minimum-context floor.
- `test_max_tokens_exceeding_window_falls_back_to_full`: pathological reservation does not produce a non-positive threshold.
- `test_max_tokens_coercion_treats_non_int_as_no_reservation`: `None`, `0`, negative, and `"nope"` are safe; `65536` is retained; a `MagicMock` forwarded from a parent does not crash construction.

### EU-4252-D — floor binding at a near-minimum window

`agent/context_compressor.py`, `_compute_threshold_tokens`:

- Before: the `MINIMUM_CONTEXT_LENGTH` floor was reduced to the 85% trigger only when the floor met/exceeded the effective window. At `context_length=65536`, a 50% configured threshold was floored to `64000` (97.7%), leaving too little output room.
- After: computes `pct_value`, `floored`, and `trigger_cap = int(effective_window * _MIN_CTX_TRIGGER_RATIO)`. If the floor is the binding term and exceeds the cap, it caps the floor at 85% of the effective budget. An explicit configured percentage above 85% is preserved as user intent. The existing `floored >= effective_window` branch remains a separate final guard.

### EU-4252-T — partitioned policy oracle

`tests/agent/test_context_compressor.py::TestCompress` includes `test_threshold_floor_capped_at_85_percent_of_window`, asserting:

- `65536, 0.50` becomes `int(65536 * 0.85) == 55705`;
- `70000, 0.50` becomes `59500`;
- `100000, 0.50` remains `64000` because the floor is at/below the cap;
- `372000, 0.90` remains `334800`, proving explicit high user intent is not silently capped.

### EU-B780-D — retained-tail capacity binding

`agent/context_compressor.py` and `hermes_cli/config_defaults.py`:

- Before: lean tail budget was `max(10K, min(25K, 2.5% of window))`; the boundary walk and pressure demotion used `1.5 * token_budget` without knowing the window. On 8K/16K windows the protected tail could consume most or more than the request.
- After: defines `TAIL_MAX_CONTEXT_FRACTION = 0.20`; tail budget (both tail modes) is first clamped to 20% of `context_length`, and `_tail_soft_ceiling` applies the same context-relative ceiling to both the pressure-demotion path and the boundary walk. Required recent anchors and atomic tool groups are explicit exceptions and can still overrun the soft ceiling.
- The change is therefore not “always retain 20%”; it is “optional retained material cannot use an unbounded fixed floor on small windows, while correctness-required anchors remain admissible.”

### EU-B780-T — unit plus end-to-end behavioral oracle

`tests/agent/test_compression_small_ctx_threshold_floor.py::TestTailBudgetProportionality` adds:

- `test_tail_budget_never_exceeds_window_share`: for 8192, 16384, and 32768, `tail_token_budget <= ctx * TAIL_MAX_CONTEXT_FRACTION`; 131072 keeps the old 10K lean floor.
- `test_small_window_compress_leaves_a_real_middle`: builds a 12-tool-turn transcript, runs `_compress_window`, checks the tail is near the 20% share (allowing one atomic turn overrun) and that a substantial middle remains compressible.

### EU-AF0-D — one pure trigger derivation seam

`agent/context_compressor.py`:

- Before: `preview_threshold_tokens` reimplemented model-threshold resolution, effective percentage, threshold calculation, and token cap; `update_model` separately repeated the same chain.
- After: `_derive_trigger(model, context_length, provider)` returns `(base_percent, effective_percent, threshold_tokens)` and is the only place for that model/window trigger chain. `preview_threshold_tokens` returns its third value; `update_model` assigns all three values from the same helper. The auxiliary summarizer ceiling stays outside because it is runtime-specific, not model-specific.

### EU-AF0-B — caller and presentation boundaries

- `tests/hermes_cli/test_context_switch_guard.py::test_cap_lowers_the_switch_warning_threshold_below_the_ratio` checks that a switch warning quotes the same lower cap the compressor will install.
- `agent/agent_init.py::_emit_compression_summary` names `(capped at ...)` only when the cap actually binds, avoiding a false claim on windows where the ratio is lower.
- `tools/delegate_tool.py` and `hermes_cli/config_defaults.py` receive the corresponding wording/cap propagation changes in this commit; they do not own trigger arithmetic.

## Why these four belong to one candidate family

Each change repairs a different failure mode of the same operational invariant: a compaction system must make pressure/retention decisions against the **effective capacity envelope**, not a nominal or duplicated capacity. The evidence supports a provisional family around capacity-aware pressure policy. It does **not** prove that every compaction change in Hermes is one Skill: provider-overflow recovery, stale-generation races, summary refusal handling, and message-accounting changes were searched but excluded from this run because their causal mechanisms are different.

## Evidence limits

- The selected evidence is all from one repository. It supports Atomic candidates and a provisional within-repository Pattern, but cannot by itself validate cross-harness transfer.
- The commit bodies are used only as navigation/context. The claims above are grounded in before/after code, call sites, and named tests.
- No token-saving or latency number is asserted beyond the deterministic values explicitly asserted in tests or documented probe comments. No LLM-generated judgment is treated as an oracle.
