"""Shared budget for retrieval, model reasoning, resources, probes and repair."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field, replace, is_dataclass
from typing import Callable


class BudgetExceeded(RuntimeError):
    pass


@dataclass(frozen=True)
class BudgetCaps:
    model_tokens: int = 300_000
    model_calls: int = 60
    tool_calls: int = 120
    history_tokens: int = 6000
    approved_root_packages: int = 2
    seconds: float = 1800
    workflow_candidates: int = 8
    parent_workflows: int = 2
    beam_width: int = 4
    composed_plans: int = 4
    probes_per_round: int = 2
    review_rounds: int = 3

    def __post_init__(self):
        if any(value <= 0 for value in asdict(self).values()):
            raise ValueError("budget caps must be positive")


@dataclass
class BudgetLedger:
    caps: BudgetCaps = field(default_factory=BudgetCaps)
    clock: Callable[[], float] = time.monotonic
    model_tokens: int = 0
    model_calls: int = 0
    tool_calls: int = 0
    history_tokens: int = 0
    approved_roots: set[str] = field(default_factory=set)
    events: list[dict] = field(default_factory=list)
    rounds: int = 0
    token_counter: Callable[[str], int] | None = None
    tokenizer_name: str = "utf8_upper_bound"

    def __post_init__(self):
        self.started = self.clock()

    def check_time(self):
        if self.clock() - self.started > self.caps.seconds:
            raise BudgetExceeded("shared wall-clock budget exhausted")

    def charge(self, kind: str, amount: int, reason: str):
        if (
            kind not in {"model_tokens", "model_calls", "tool_calls", "history_tokens"}
            or amount < 0
        ):
            raise ValueError("invalid budget charge")
        total = getattr(self, kind) + amount
        # Failed/over-cap requests remain in the accounting log.
        setattr(self, kind, total)
        self.events.append({"kind": kind, "amount": amount, "reason": reason})
        self.check_time()
        if total > getattr(self.caps, kind):
            raise BudgetExceeded(f"shared {kind} budget exhausted")

    def history(self, content: str, reason: str):
        # UTF-8 bytes upper-bound common text-token counts; never silently undercount.
        count = self.token_counter(content) if self.token_counter else len(content.encode())
        self.charge("history_tokens", count, reason)

    def approve_root(self, package_id: str):
        self.check_time()
        if package_id not in self.approved_roots:
            if len(self.approved_roots) >= self.caps.approved_root_packages:
                raise BudgetExceeded("approved root-package budget exhausted")
            self.approved_roots.add(package_id)

    def next_round(self):
        self.check_time()
        self.rounds += 1
        if self.rounds > self.caps.review_rounds:
            raise BudgetExceeded("retrieval/review rounds exhausted")

    def solver_view(self):
        """Report actual balance before the next request without replaying events."""
        used = {
            kind: getattr(self, kind)
            for kind in ("model_tokens", "model_calls", "tool_calls", "history_tokens")
        }
        used.update(
            approved_root_packages=len(self.approved_roots),
            review_rounds=self.rounds,
            seconds=self.clock() - self.started,
        )
        return {
            "caps": {kind: getattr(self.caps, kind) for kind in used},
            "used": used,
            "remaining": {
                kind: max(0, getattr(self.caps, kind) - amount) for kind, amount in used.items()
            },
            "accounting": "Balance before current request; shared cap and conservative request preflight remain enforced. "
            "Provider usage is charged when available, UTF-8 upper bound otherwise.",
        }

    def snapshot(self):
        return {
            "caps": asdict(self.caps),
            "model_tokens": self.model_tokens,
            "model_calls": self.model_calls,
            "tool_calls": self.tool_calls,
            "history_tokens": self.history_tokens,
            "approved_roots": sorted(self.approved_roots),
            "rounds": self.rounds,
            "elapsed_seconds": self.clock() - self.started,
            "token_accounting": "provider usage when available, conservative UTF-8 bound otherwise",
            "history_tokenizer": self.tokenizer_name,
            "events": list(self.events),
        }


class BudgetedTransport:
    """All adaptive model calls share one ledger; retries must be disabled upstream."""

    def __init__(self, transport, ledger: BudgetLedger, output_reserve: int = 4000):
        self.transport, self.ledger = transport, ledger
        self.output_reserve = max(
            output_reserve,
            getattr(getattr(transport, "config", None), "max_output_tokens", output_reserve),
        )
        config = getattr(transport, "config", None)
        if config is not None and getattr(config, "retries", 0):
            raise ValueError("adaptive transport requires retries=0 for common accounting")

    def complete(self, *, system, user, response_schema):
        self.ledger.charge("model_calls", 1, "adaptive model request")
        prompt = system + user + json.dumps(response_schema)
        reserve = len(prompt.encode()) + self.output_reserve
        self.ledger.check_time()
        if self.ledger.model_tokens + reserve > self.ledger.caps.model_tokens:
            raise BudgetExceeded("model request cannot fit remaining token budget")
        original_config = getattr(self.transport, "config", None)
        if (
            original_config is not None
            and is_dataclass(original_config)
            and hasattr(original_config, "timeout_seconds")
        ):
            remaining = max(
                0.001, self.ledger.caps.seconds - (self.ledger.clock() - self.ledger.started)
            )
            self.transport.config = replace(
                original_config, timeout_seconds=min(original_config.timeout_seconds, remaining)
            )
        try:
            result = self.transport.complete(
                system=system, user=user, response_schema=response_schema
            )
        except Exception:
            self.ledger.charge("model_tokens", reserve, "failed model request conservative bound")
            raise
        finally:
            if original_config is not None:
                self.transport.config = original_config
        usage = (getattr(self.transport, "calls", []) or [{}])[-1].get("usage") or {}
        total = usage.get("total_tokens")
        if not isinstance(total, int) or total < 0:
            total = len(prompt.encode()) + len(json.dumps(result).encode())
        self.ledger.charge("model_tokens", total, "adaptive model request")
        return result


class BudgetedEncoder:
    """Meter online neural embedding queries alongside solver and ranker calls."""

    def __init__(self, encoder, ledger):
        self.encoder, self.ledger = encoder, ledger
        self.model_version, self.dimensions = encoder.model_version, encoder.dimensions

    def descriptor(self):
        return self.encoder.descriptor()

    def encode(self, texts):
        if self.encoder.descriptor()["kind"] == "feature-hash":
            return self.encoder.encode(texts)
        self.ledger.charge("model_calls", 1, "online neural retrieval embedding")
        estimate = sum(len(value.encode()) for value in texts)
        if self.ledger.model_tokens + estimate > self.ledger.caps.model_tokens:
            raise BudgetExceeded("query encoding cannot fit shared model-token budget")
        before = getattr(self.encoder, "tokens_processed", 0)
        try:
            vectors = self.encoder.encode(texts)
        except Exception:
            self.ledger.charge(
                "model_tokens", estimate, "failed neural embedding conservative bound"
            )
            raise
        tokens = getattr(self.encoder, "tokens_processed", before) - before
        self.ledger.charge(
            "model_tokens", tokens or estimate, "online neural embedding encoded tokens"
        )
        return vectors
