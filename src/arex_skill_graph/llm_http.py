"""Small OpenAI-compatible HTTP transport used by the extraction runner.

The transport is deliberately provider-neutral and does not contain Skill
semantics. It records request/response metadata for auditability while keeping
credentials out of persisted artifacts.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import time
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True, slots=True)
class OpenAICompatibleConfig:
    api_key: str
    base_url: str
    model: str
    timeout_seconds: float = 180.0
    max_output_tokens: int = 5000
    retries: int = 2


class OpenAICompatibleTransport:
    """Implement ``LLMTransport.complete`` over ``/chat/completions``."""

    def __init__(self, config: OpenAICompatibleConfig):
        if not config.api_key:
            raise ValueError("api_key is required")
        self.config = config
        self.calls: list[dict[str, Any]] = []
        self.transcripts: list[dict[str, Any]] = []

    def complete(self, *, system: str, user: str, response_schema: Mapping[str, Any]) -> Mapping[str, Any]:
        prompt = (
            "Return one JSON object only. It must conform to this schema:\n"
            + json.dumps(response_schema, ensure_ascii=False, sort_keys=True)
        )
        body = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user + "\n\n" + prompt},
            ],
            "temperature": 0,
            "max_tokens": self.config.max_output_tokens,
            "response_format": {"type": "json_object"},
        }
        endpoint = self.config.base_url.rstrip("/") + "/chat/completions"
        request = Request(
            endpoint,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + self.config.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        started = time.perf_counter()
        last_error: Exception | None = None
        for attempt in range(self.config.retries + 1):
            try:
                with urlopen(request, timeout=self.config.timeout_seconds) as response:
                    raw = response.read().decode("utf-8")
                    envelope = json.loads(raw)
                result = self._extract_content(envelope)
                self.calls.append({
                    "model": self.config.model,
                    "endpoint": endpoint,
                    "attempt": attempt + 1,
                    "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                    "usage": envelope.get("usage"),
                    "response_id": envelope.get("id"),
                })
                self.transcripts.append({
                    "system": system,
                    "user": user,
                    "response_schema": dict(response_schema),
                    "response": dict(result),
                    "response_id": envelope.get("id"),
                    "usage": envelope.get("usage"),
                })
                return result
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, ValueError) as error:
                last_error = error
                if attempt >= self.config.retries:
                    break
                time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(f"LLM request failed after {self.config.retries + 1} attempts: {last_error}") from last_error

    @staticmethod
    def _extract_content(envelope: Mapping[str, Any]) -> Mapping[str, Any]:
        if envelope.get("error"):
            raise ValueError(str(envelope["error"]))
        choices = envelope.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("LLM response has no choices")
        message = choices[0].get("message", {})
        content = message.get("content") if isinstance(message, Mapping) else None
        if not isinstance(content, str):
            raise ValueError("LLM response has no textual message content")
        text = content.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        value = json.loads(text)
        if not isinstance(value, Mapping):
            raise ValueError("LLM JSON response must be an object")
        return value

