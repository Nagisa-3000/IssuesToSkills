"""GitHub GraphQL transport with memory-only authentication and suppressed errors."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .history_census import GitHubAPIError


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class GitHubHTTP:
    def __init__(self, token, *, timeout=60, opener=None):
        if not isinstance(token, str) or not token.strip():
            raise ValueError("runtime GitHub credential is required; values suppressed")
        self._token, self.timeout = token, timeout
        self._opener = opener or build_opener(_NoRedirect())
        self.calls, self.rate_limit = 0, None

    def graphql(self, query, variables):
        request = Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": variables}).encode(),
            headers={
                "Authorization": "Bearer " + self._token,
                "Content-Type": "application/json",
                "User-Agent": "AREX-historical-timeline-recovery",
            },
            method="POST",
        )
        self.calls += 1
        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                result = json.load(response)
        except HTTPError as error:
            raise GitHubAPIError(status=error.code) from None
        except (URLError, TimeoutError, ValueError, OSError):
            raise RuntimeError("public GitHub transport failed; native output suppressed") from None
        if (
            not isinstance(result, dict)
            or result.get("errors")
            or not isinstance(result.get("data"), dict)
        ):
            raise RuntimeError("public GraphQL query failed; native output suppressed")
        self.rate_limit = result["data"].get("rateLimit")
        return result["data"]
