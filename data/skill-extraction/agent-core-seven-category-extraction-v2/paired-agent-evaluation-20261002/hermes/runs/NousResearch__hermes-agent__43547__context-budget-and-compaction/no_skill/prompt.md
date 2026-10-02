You are solving a held-out implementation task in repository NousResearch/hermes-agent.
The workspace is a synthetic snapshot based on the pre-change parent and has no future Git history. The original solution commit is not available. Work only in this workspace; do not search external services or other repositories. Do not edit the visible regression tests. Inspect the current code, implement the behavior, and run focused tests before finishing.

# Problem family
context budget and compaction

# Issue/task
Context compaction trigger ignores the output-token reservation (custom-provider default max_tokens=65536 halves the usable input budget)

## Summary

The context-compaction trigger compares estimated input tokens against `context_length × compression.threshold`, but the request that actually goes to the provider reserves `max_tokens` **out of that same window**. When `max_tokens` is large, the *effective input budget* (`context_length − max_tokens`) can sit at or below the compaction trigger — so sessions hit a hard provider 400 before proactive compaction ever fires, and the recovery path can't save them.

This is not hypothetical with default settings: for `provider: custom` (vLLM / llama.cpp / LM Studio / Ollama-compatible endpoints), the provider profile defaults `max_tokens` to **65536** when the user hasn't set `model.max_tokens` (`plugins/model-providers/custom/__init__.py` — the deliberate floor added for Ollama's `num_predict=128`, #39281). Against a 131072-token model, that default silently halves the usable input budget.

## Real incident (2026-06-10, Hermes Agent v0.16.0 / upstream a72bb037)

Setup: vLLM 0.22 serving gemma4 with `--max-model-len 131072`; no `model.max_tokens` in config.yaml; `compression.threshold: 0.5`.

- Effective input budget: 131072 − 65536 (profile default) = **65,536 tokens**
- Compaction trigger: 0.5 × 131072 = est. **65,536 tokens** — i.e. *exactly at* the wall
- Aggravator: the rough estimator (`estimate_messages_tokens_rough`, ~chars/4) reported **~43K** when the provider tokenized the same prompt as **≥65,537** (system prompt + tool schemas + chat template + thinking history; ~1.5× undercount) — so by the estimator's reckoning the session was at 33% of the window when it was at 100% of the real input budget.

```
⚠️  API call failed (attempt 1/3): BadRequestError [HTTP 400]
   📝 Error: HTTP 400: This model's maximum context length is 131072 tokens. However, you
   requested 65536 output tokens and your prompt contains at least 65537 input tokens, for a
   total of at least 131073 tokens. Please reduce the length of the input prompt or the number
   of requested output tokens.
   ⏱️  Elapsed: 0.09s  Context: 28 msgs, ~43,089 tokens
⚠️  Context length exceeded, but provider did not report a max context length; keeping context_length at 131,072 tokens and compressing.
🗜️ Context too large (~43,089 tokens) — compressing (1/3)...
🗜️ Compressed 27 → 20 messages, retrying...
   [same 400 again — the retry still requests 65536 output tokens]
❌ Context length exceeded and cannot compress further.
```

The compression retries can't converge: each pass frees a small amount of input while the request keeps reserving the same 65,536 output tokens. (A second, narrower bug made this worse — `parse_available_output_tokens_from_error` doesn't recognize vLLM's token-based phrasing, so the output-cap repair path never engaged. That part is fixed separately in the linked PR.)

## Proposal

Make the input-budget math reservation-aware:

1. **Compaction trigger:** compare estimated input against `(context_length − resolved_output_cap) × threshold` instead of `context_length × threshold`, where `resolved_output_cap` is the same value the transport will put in the request (user `model.max_tokens`, else the provider profile's `default_max_tokens`, else 0).
2. **Pre-flight check:** same substitution anywhere the estimate is compared to `context_length`.
3. Possibly cap the custom-profile default at something like `min(65536, context_length // 4)` once a context length is known — the 65536 floor makes sense for Ollama's tiny `num_predict` default, but it shouldn't consume half of a 131K window.

(1) and (2) are mechanical; (3) is a design question for maintainers since it touches the #39281 fix. Happy to implement whichever shape you prefer — flagging the design first rather than dropping an opinionated PR.

---

I had Claude Fable 5 do this work - this issue was written by the model after it diagnosed the incident live on my own Hermes deployment (custom vLLM endpoint on local hardware). The numbers and logs above are from the real session. As with my previous PRs, my goal is to push Fable to be a useful open-source contributor - if the maintainers find the diagnosis sound, that's the signal I'm looking for.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


# Visible regression tests retained for this evaluation
- tests/agent/test_context_compressor.py

# Validation commands
- `./.venv/bin/pytest -q 'tests/agent/test_context_compressor.py'`
- `git diff --check HEAD`

# Arm
no_skill

Solve the task from the repository and visible tests without any retrieved Skill context.