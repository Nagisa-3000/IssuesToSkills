#!/usr/bin/env python3
"""Materialize the user-supplied six-harness agent-core issue table.

The table is a source-of-truth seed list, not evidence that every issue has a
usable implementation resolution.  This builder keeps the exact issue rows,
assigns a deterministic leave-one-repository-out holdout per category, and
leaves commit/PR verification to the later evidence-enrichment gate.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CHECKOUTS = {
    "earendil-works/pi": "/home/chenyujia/tritonToLlvm/pi-agent",
    "Aider-AI/aider": "/home/chenyujia/tritonToLlvm/aider-agent",
    "NousResearch/hermes-agent": "/home/chenyujia/tritonToLlvm/hermes-agent",
    "openai/codex": "/home/chenyujia/tritonToLlvm/codex-agent",
    "google-gemini/gemini-cli": "/home/chenyujia/tritonToLlvm/gemini-cli",
    "QwenLM/qwen-code": "/home/chenyujia/tritonToLlvm/qwen-code",
}


# One untouched repository per category gives a genuine cross-project
# transfer holdout while still using all six repositories in the training
# catalog across the seven categories.
HOLDOUT_REPOSITORY = {
    "provider-interface-adaptation": "earendil-works/pi",
    "credential-resolution-and-authentication": "Aider-AI/aider",
    "context-budget-and-compaction": "NousResearch/hermes-agent",
    "state-continuity-and-resume": "openai/codex",
    "structured-tool-contract-integrity": "google-gemini/gemini-cli",
    "effect-control-and-isolation": "QwenLM/qwen-code",
    "failure-recovery-and-streaming": "earendil-works/pi",
}


# (canonical problem class, repository, issue number, table note)
TABLE: tuple[tuple[str, str, int, str], ...] = (
    ("provider-interface-adaptation", "earendil-works/pi", 5823, "provider/model selection ignores provider"),
    ("provider-interface-adaptation", "Aider-AI/aider", 2765, "cannot configure an OpenRouter provider"),
    ("provider-interface-adaptation", "NousResearch/hermes-agent", 121359, "fallback base_url is ignored"),
    ("provider-interface-adaptation", "openai/codex", 41095, "follow-up for a custom OpenAI-compatible provider lacks model"),
    ("provider-interface-adaptation", "google-gemini/gemini-cli", 15430, "GOOGLE_GEMINI_BASE_URL is ignored"),
    ("provider-interface-adaptation", "QwenLM/qwen-code", 9452, "switching Responses model/endpoint breaks saved session"),

    ("credential-resolution-and-authentication", "earendil-works/pi", 9245, "--api-key and auth.json precedence is wrong"),
    ("credential-resolution-and-authentication", "Aider-AI/aider", 750, "API key does not work"),
    ("credential-resolution-and-authentication", "NousResearch/hermes-agent", 289, "OPENAI_API_KEY precedence selects the wrong credential"),
    ("credential-resolution-and-authentication", "openai/codex", 48299, "ChatGPT login succeeds but stale sk-svcac credential returns 401"),
    ("credential-resolution-and-authentication", "google-gemini/gemini-cli", 28337, "OAuth credential is saved but login is repeatedly requested"),
    ("credential-resolution-and-authentication", "QwenLM/qwen-code", 9016, "Vertex AI ADC authentication failure"),

    ("context-budget-and-compaction", "earendil-works/pi", 10075, "user-turn boundary unexpectedly loses about 100k provider context"),
    ("context-budget-and-compaction", "Aider-AI/aider", 3493, "maximum chat-history token limit is ineffective"),
    ("context-budget-and-compaction", "NousResearch/hermes-agent", 43547, "compaction does not reserve output-token space"),
    ("context-budget-and-compaction", "openai/codex", 16281, "automatic compaction fails near the context limit"),
    ("context-budget-and-compaction", "google-gemini/gemini-cli", 27738, "large tool output is not bounded and permanently stalls the session"),
    ("context-budget-and-compaction", "QwenLM/qwen-code", 11894, "wrong model token-limit mapping breaks long-session compaction"),

    ("state-continuity-and-resume", "earendil-works/pi", 10121, "truncated assistant/tool call is replayed incorrectly and resume creates an empty session"),
    ("state-continuity-and-resume", "Aider-AI/aider", 2979, "restoring chat history fails during history summarization"),
    ("state-continuity-and-resume", "NousResearch/hermes-agent", 228, "conversation_history is mutated in place and corrupts historical state"),
    ("state-continuity-and-resume", "openai/codex", 47761, "resume CWD filtering mixes in a sibling worktree session"),
    ("state-continuity-and-resume", "google-gemini/gemini-cli", 29194, "corrupt checkpoint crashes resume"),
    ("state-continuity-and-resume", "QwenLM/qwen-code", 9573, "resumed session is missing a saved tool result"),

    ("structured-tool-contract-integrity", "earendil-works/pi", 10086, "strict fields truncate or mutate streamed Mistral tool-call arguments"),
    ("structured-tool-contract-integrity", "Aider-AI/aider", 3793, "model search/replace block is executed as a shell command"),
    ("structured-tool-contract-integrity", "NousResearch/hermes-agent", 123832, "repairing a tool-call prefix corrupts its arguments"),
    ("structured-tool-contract-integrity", "openai/codex", 46195, "tool call reaches the provider without output and the thread stalls"),
    ("structured-tool-contract-integrity", "google-gemini/gemini-cli", 29308, "unprotected JSON.parse on tool-call arguments terminates sendStream"),
    ("structured-tool-contract-integrity", "QwenLM/qwen-code", 4695, "identical tool call is sent repeatedly without a circuit breaker"),

    ("effect-control-and-isolation", "earendil-works/pi", 9936, "bash child inherits /dev/tty and hangs the agent session"),
    ("effect-control-and-isolation", "Aider-AI/aider", 3009, "command execution repeatedly asks for confirmation"),
    ("effect-control-and-isolation", "NousResearch/hermes-agent", 232, "dangerous-command check can be bypassed with a newline"),
    ("effect-control-and-isolation", "openai/codex", 42184, "Windows sandbox root deny still permits reads outside reopened roots"),
    ("effect-control-and-isolation", "google-gemini/gemini-cli", 26004, "YOLO/non-interactive mode waits for approval and silently stops plan execution"),
    ("effect-control-and-isolation", "QwenLM/qwen-code", 10859, "shell guard incorrectly blocks a git command outside the session directory"),

    ("failure-recovery-and-streaming", "earendil-works/pi", 9735, "proxy premature stream ending is not recognized, so no retry occurs"),
    ("failure-recovery-and-streaming", "Aider-AI/aider", 3648, "LiteLLM APIConnectionError chunk parsing fails"),
    ("failure-recovery-and-streaming", "NousResearch/hermes-agent", 121320, "stream closes before message_stop and persists a truncated answer without retry"),
    ("failure-recovery-and-streaming", "openai/codex", 39988, "CLI turn remains working after a tool call stops emitting events"),
    ("failure-recovery-and-streaming", "google-gemini/gemini-cli", 29264, "interrupted turn poisons context and enters an infinite loop"),
    ("failure-recovery-and-streaming", "QwenLM/qwen-code", 7832, "socket close in YOLO mode is not retried"),
)


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for ordinal, (category, repository, issue, note) in enumerate(TABLE, 1):
        key = (repository, issue)
        if key in seen:
            raise ValueError(f"duplicate table issue: {repository}#{issue}")
        seen.add(key)
        holdout = HOLDOUT_REPOSITORY[category] == repository
        rows.append({
            "case_id": f"{repository.replace('/', '__')}__{issue}__{category}",
            "repository": repository,
            "issue": issue,
            "issue_url": f"https://github.com/{repository}/issues/{issue}",
            "checkout": CHECKOUTS[repository],
            "category": category,
            "table_ordinal": ordinal,
            "table_note": note,
            "source": "user_supplied_agent_core_issue_table",
            "role": "holdout_candidate" if holdout else "train_candidate",
            "split": "holdout_candidate" if holdout else "train_candidate",
            "holdout_reason": (
                "leave-one-repository-out category transfer test"
                if holdout else None
            ),
            "evidence_status": "pending_issue_pr_commit_enrichment",
        })
        if category == "credential-resolution-and-authentication" and repository == "NousResearch/hermes-agent" and issue == 289:
            rows[-1]["preferred_resolution_pr"] = 295
        if category == "credential-resolution-and-authentication" and repository == "QwenLM/qwen-code" and issue == 9016:
            rows[-1]["preferred_resolution_pr"] = 9017
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = build_rows()
    categories = sorted({row["category"] for row in rows})
    repositories = sorted({row["repository"] for row in rows})
    payload = {
        "schema_version": "agent-core-function-issue-table-v1",
        "source": "user_supplied_agent_core_issue_table",
        "categories": categories,
        "repositories": repositories,
        "split_policy": {
            "type": "leave_one_repository_out_per_category",
            "holdout_repositories": HOLDOUT_REPOSITORY,
            "train_count": sum(row["role"] == "train_candidate" for row in rows),
            "holdout_count": sum(row["role"] == "holdout_candidate" for row in rows),
        },
        "cases": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    train = [row for row in rows if row["role"] == "train_candidate"]
    holdout = [row for row in rows if row["role"] == "holdout_candidate"]
    args.output.with_name(args.output.stem + "-train.json").write_text(
        json.dumps(train, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.output.with_name(args.output.stem + "-holdout.json").write_text(
        json.dumps(holdout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "cases": len(rows),
        "categories": len(categories),
        "repositories": len(repositories),
        "train": len(train),
        "holdout": len(holdout),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
