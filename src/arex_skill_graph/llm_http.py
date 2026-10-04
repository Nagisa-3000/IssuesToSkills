"""Small OpenAI-compatible HTTP transport used by the extraction runner.

The transport is deliberately provider-neutral and does not contain Skill
semantics. It records request/response metadata for auditability while keeping
credentials out of persisted artifacts.
"""

from __future__ import annotations

import base64
import json
import subprocess
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
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
    http_backend: str = "native"
    stream_responses: bool = False


class OpenAICompatibleTransport:
    """Implement ``LLMTransport.complete`` over ``/chat/completions``."""

    def __init__(self, config: OpenAICompatibleConfig):
        if not config.api_key:
            raise ValueError("api_key is required")
        if config.http_backend not in {"native", "windows_pipe"}:
            raise ValueError("unknown HTTP backend")
        endpoint = urlsplit(config.base_url)
        if (
            endpoint.scheme not in {"https", "http"}
            or not endpoint.hostname
            or endpoint.username
            or endpoint.password
            or endpoint.query
            or endpoint.fragment
        ):
            raise ValueError("configure a credential-free HTTP service base URL")
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
        if self.config.stream_responses:
            body = {**body, "stream": True, "stream_options": {"include_usage": True}}
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
            attempt_started = time.perf_counter()
            envelope = None
            try:
                if self.config.http_backend == "windows_pipe":
                    raw = self._windows_request(endpoint, body)
                else:
                    with urlopen(request, timeout=self.config.timeout_seconds) as response:
                        raw = response.read().decode("utf-8")
                if safe_text(raw, [self.config.api_key]) != raw:
                    raise ValueError("credential-like value in service response")
                envelope = (
                    completion_from_sse(raw)
                    if self.config.stream_responses and not raw.lstrip().startswith("{")
                    else json.loads(raw)
                )
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
                        "successful": True,
                        "elapsed_ms": round((time.perf_counter() - attempt_started) * 1000, 2),
                        "request_elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                        "usage": envelope.get("usage"),
                        "response_id": envelope.get("id"),
                        "stream_requested": self.config.stream_responses,
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
                OSError,
            ) as error:
                last_error = error
                self.calls.append(
                    {
                        "model": self.config.model,
                        "endpoint": safe_text(endpoint, [self.config.api_key]),
                        "attempt": attempt + 1,
                        "successful": False,
                        "elapsed_ms": round((time.perf_counter() - attempt_started) * 1000, 2),
                        "request_elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                        "http_status": error.code if isinstance(error, HTTPError) else None,
                        "error_type": type(error).__name__,
                        "usage": envelope.get("usage") if isinstance(envelope, Mapping) else None,
                    }
                )
                if attempt >= self.config.retries:
                    break
                time.sleep(1.5 * (attempt + 1))
        raise RuntimeError(
            f"LLM request failed after {self.config.retries + 1} attempts ({type(last_error).__name__})"
        ) from None

    def _windows_request(self, endpoint, body):
        parsed = urlsplit(endpoint)
        if parsed.scheme != "https" or parsed.username or parsed.password:
            raise ValueError("HTTP bridge requires a credential-free HTTPS endpoint")
        helper = Path(__file__).with_name("windows_http_bridge.ps1")
        encoded = base64.b64encode(helper.read_text().encode("utf-16le")).decode()
        try:
            result = subprocess.run(
                [
                    "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-EncodedCommand",
                    encoded,
                ],
                input=json.dumps(
                    {
                        "endpoint": endpoint,
                        "credential": self.config.api_key,
                        "body": body,
                        "timeout_seconds": self.config.timeout_seconds,
                    },
                    ensure_ascii=False,
                ),
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.config.timeout_seconds + 15,
                check=False,
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError("Windows HTTP pipe timed out; values suppressed") from None
        try:
            wrapper = json.loads(result.stdout.lstrip("\ufeff"))
        except (ValueError, TypeError):
            raise URLError("Windows HTTP pipe failed; native output suppressed") from None
        if (
            result.returncode
            or not isinstance(wrapper, Mapping)
            or type(wrapper.get("status")) is not int
            or not 100 <= wrapper["status"] <= 599
            or not isinstance(wrapper.get("body"), str)
        ):
            raise URLError("Windows HTTP pipe failed; native output suppressed")
        if wrapper["status"] >= 400:
            raise HTTPError(endpoint, wrapper["status"], "provider request failed", {}, None)
        return wrapper["body"]

    @staticmethod
    def _extract_content(envelope: Mapping[str, Any]) -> Mapping[str, Any]:
        if envelope.get("error"):
            raise ValueError(str(envelope["error"]))
        choices = envelope.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("LLM response has no choices")
        if choices[0].get("finish_reason") == "length":
            raise ValueError("LLM returned an incomplete JSON response")
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


def completion_from_sse(raw: str) -> Mapping[str, Any]:
    """Assemble a complete text response; partial streams never become Skills."""
    fragments, usage, response_id, finish, done = [], None, None, None, False
    for line in raw.splitlines():
        if not line.strip() or line.startswith((":", "event:", "id:", "retry:")):
            continue
        if not line.startswith("data:") or done:
            raise ValueError("invalid completion event stream")
        data = line[5:].strip()
        if data == "[DONE]":
            done = True
            continue
        event = json.loads(data)
        if not isinstance(event, Mapping) or event.get("error"):
            raise ValueError("completion stream reported an error")
        if event.get("id"):
            if response_id is not None and response_id != event["id"]:
                raise ValueError("completion stream changed response identity")
            response_id = event["id"]
        if event.get("usage") is not None:
            usage = event["usage"]
        for choice in event.get("choices", []):
            if choice.get("index", 0) != 0:
                raise ValueError("completion stream contains multiple choices")
            content = choice.get("delta", {}).get("content")
            if content is not None:
                if not isinstance(content, str) or finish is not None:
                    raise ValueError("invalid text fragment in completion stream")
                fragments.append(content)
            if choice.get("finish_reason") is not None:
                if finish is not None:
                    raise ValueError("completion stream ended a choice twice")
                finish = choice["finish_reason"]
    if not done or finish is None:
        raise ValueError("incomplete completion stream; no response was recorded")
    return {
        "id": response_id,
        "choices": [
            {"index": 0, "message": {"content": "".join(fragments)}, "finish_reason": finish}
        ],
        "usage": usage,
    }
