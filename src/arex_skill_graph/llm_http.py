"""Small OpenAI-compatible HTTP transport used by the extraction runner.

The transport is deliberately provider-neutral and does not contain Skill
semantics. It records request/response metadata for auditability while keeping
credentials out of persisted artifacts.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .direct_skill_extraction import safe_text


@dataclass(frozen=True, slots=True)
class OpenAICompatibleConfig:
    api_key: str = field(repr=False)
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

    def complete(
        self, *, system: str, user: str, response_schema: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        prompt = "Return one JSON object only. It must conform to this schema:\n" + json.dumps(
            response_schema, ensure_ascii=False, sort_keys=True
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
        envelope = self._request(body)
        result = self._extract_content(envelope)
        if safe_text(json.dumps(result), [self.config.api_key]) != json.dumps(result):
            raise ValueError("credential-like value detected; response was not recorded")
        self.transcripts.append(
            {
                "system": safe_text(system, [self.config.api_key]),
                "user": safe_text(user, [self.config.api_key]),
                "response_schema": dict(response_schema),
                "response": dict(result),
                "response_id": envelope.get("id"),
                "usage": envelope.get("usage"),
            }
        )
        return result

    def complete_text(self, *, system: str, user: str) -> str:
        """Direct Skill file transport: no JSON schema or JSON response format."""
        body = {
            "model": self.config.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "temperature": 0,
            "max_tokens": self.config.max_output_tokens,
        }
        envelope = self._request(body)
        choices = envelope.get("choices") or []
        if not choices or choices[0].get("finish_reason") == "length":
            raise ValueError("LLM returned no complete Skill response")
        result = choices[0].get("message", {}).get("content")
        if not isinstance(result, str) or not result.strip():
            raise ValueError("LLM returned no Skill file content")
        if safe_text(result, [self.config.api_key]) != result:
            raise ValueError("credential-like value detected; response was not recorded")
        self.transcripts.append(
            {
                "system": safe_text(system, [self.config.api_key]),
                "user": safe_text(user, [self.config.api_key]),
                "response": result,
                "output_contract": "direct-skill-files-v1",
                "response_id": envelope.get("id"),
                "usage": envelope.get("usage"),
            }
        )
        return result

    def _request(self, body: Mapping[str, Any]) -> Mapping[str, Any]:
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
                    if safe_text(raw, [self.config.api_key]) != raw:
                        raise ValueError("credential-like value in service response")
                    envelope = json.loads(raw)
                if not isinstance(envelope, Mapping):
                    raise TypeError("LLM service response must be an object")
                if envelope.get("error"):
                    raise ValueError("LLM endpoint reported an error")
                if body.get("response_format") == {"type": "json_object"}:
                    self._extract_content(envelope)
                self.calls.append(
                    {
                        "model": self.config.model,
                        "endpoint": safe_text(endpoint, [self.config.api_key]),
                        "attempt": attempt + 1,
                        "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                        "usage": envelope.get("usage"),
                        "response_id": envelope.get("id"),
                    }
                )
                return envelope
            except (
                HTTPError,
                URLError,
                TimeoutError,
                json.JSONDecodeError,
                ValueError,
                TypeError,
            ) as error:
                last_error = error
                if attempt >= self.config.retries:
                    break
                time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(
            f"LLM request failed after {self.config.retries + 1} attempts ({type(last_error).__name__})"
        ) from None

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
            raise TypeError("LLM response has no textual message content")
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
            raise TypeError("LLM JSON response must be an object")
        return value
