from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
from typing import Any, Callable, Mapping
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


GITHUB_API_VERSION = "2022-11-28"
CLOSING_REFERENCE_RE = re.compile(
    r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+"
    r"(?:https://github\.com/[^/\s]+/[^/\s]+/issues/)?#?(\d+)"
)
GENERIC_TITLE_RE = re.compile(
    r"^(?:chore|docs?|ci|build|release|bump|format|fmt|style|revert|cleanup)\b",
    re.IGNORECASE,
)
SOURCE_SUFFIXES = frozenset(
    {
        ".c",
        ".cc",
        ".cpp",
        ".cxx",
        ".go",
        ".java",
        ".js",
        ".jsx",
        ".kt",
        ".kts",
        ".m",
        ".mm",
        ".php",
        ".py",
        ".rb",
        ".rs",
        ".sh",
        ".swift",
        ".ts",
        ".tsx",
        ".vue",
        ".zig",
    }
)
GENERATED_OR_LOCK_FILES = frozenset(
    {
        "cargo.lock",
        "package-lock.json",
        "pnpm-lock.yaml",
        "poetry.lock",
        "uv.lock",
        "yarn.lock",
    }
)


class GitHubApiError(RuntimeError):
    def __init__(self, message: str, *, status: int | None = None, url: str | None = None):
        super().__init__(message)
        self.status = status
        self.url = url


@dataclass(slots=True)
class HttpResponse:
    status: int
    headers: dict[str, str]
    body: bytes


Transport = Callable[[Request, float], HttpResponse]


@dataclass(slots=True)
class EpisodeQuality:
    score: float
    tier: str
    reasons: list[str]
    implementation_files: int
    test_files: int
    docs_files: int
    generated_files: int


@dataclass(slots=True)
class GitHubEpisode:
    repository: str
    number: int
    kind: str
    title: str
    body: str
    state: str
    state_reason: str | None
    html_url: str
    created_at: str | None
    updated_at: str | None
    closed_at: str | None
    merged: bool
    merged_at: str | None
    base_ref: str | None
    base_sha: str | None
    head_ref: str | None
    head_sha: str | None
    merge_commit_sha: str | None
    author: str | None
    author_association: str | None
    labels: list[str]
    linked_issue_numbers: list[int]
    commits: list[dict[str, Any]]
    files: list[dict[str, Any]]
    quality: EpisodeQuality
    fetched_at: str
    api_version: str = GITHUB_API_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class GitHubClient:
    """Cache-first GitHub REST client for selected Issue/PR episode verification.

    The raw API payload is cached by URL. A normal read never calls the network
    when a cached response exists. Setting refresh to true uses ETag and
    Last-Modified validators and preserves the prior payload on a 304 response.
    """

    def __init__(
        self,
        cache_root: str | Path,
        *,
        token: str | None = None,
        base_url: str = "https://api.github.com",
        timeout_seconds: float = 30.0,
        transport: Transport | None = None,
    ):
        self.cache_root = Path(cache_root)
        self.cache_root.mkdir(parents=True, exist_ok=True)
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.token = token if token is not None else os.environ.get("GITHUB_TOKEN")
        self.transport = transport or _urllib_transport

    def get_json(self, endpoint: str, *, refresh: bool = False) -> Any:
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}{endpoint}"
        cache_path = self._cache_path(url)
        cached = self._read_cache(cache_path)
        if cached is not None and not refresh:
            return cached["payload"]

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "arex-skill-graph/0.1",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if cached is not None:
            if cached.get("etag"):
                headers["If-None-Match"] = str(cached["etag"])
            if cached.get("last_modified"):
                headers["If-Modified-Since"] = str(cached["last_modified"])

        response = self.transport(
            Request(url, headers=headers, method="GET"),
            self.timeout_seconds,
        )
        if response.status == 304 and cached is not None:
            cached["validated_at"] = _utc_now()
            self._write_cache(cache_path, cached)
            return cached["payload"]
        if response.status < 200 or response.status >= 300:
            raise GitHubApiError(
                _render_api_error(url, response),
                status=response.status,
                url=url,
            )

        payload = json.loads(response.body.decode("utf-8"))
        envelope = {
            "url": url,
            "status": response.status,
            "fetched_at": _utc_now(),
            "etag": _header(response.headers, "etag"),
            "last_modified": _header(response.headers, "last-modified"),
            "rate_limit_remaining": _header(
                response.headers, "x-ratelimit-remaining"
            ),
            "rate_limit_reset": _header(response.headers, "x-ratelimit-reset"),
            "payload": payload,
        }
        self._write_cache(cache_path, envelope)
        return payload

    def get_paginated(
        self,
        endpoint: str,
        *,
        refresh: bool = False,
        per_page: int = 100,
        max_pages: int = 20,
    ) -> list[Any]:
        result: list[Any] = []
        separator = "&" if "?" in endpoint else "?"
        for page in range(1, max_pages + 1):
            query = urlencode({"per_page": per_page, "page": page})
            payload = self.get_json(
                f"{endpoint}{separator}{query}",
                refresh=refresh,
            )
            if not isinstance(payload, list):
                raise GitHubApiError(
                    f"expected a list from paginated endpoint {endpoint!r}"
                )
            result.extend(payload)
            if len(payload) < per_page:
                return result
        raise GitHubApiError(
            f"pagination exceeded max_pages={max_pages} for {endpoint!r}"
        )

    def fetch_episode(
        self,
        repository: str,
        number: int,
        *,
        refresh: bool = False,
        include_commits: bool = True,
        include_files: bool = True,
        persist_manifest: bool = True,
    ) -> GitHubEpisode:
        _validate_repository(repository)
        if number <= 0:
            raise ValueError("number must be positive")

        pull: dict[str, Any] | None = None
        try:
            issue = self.get_json(
                f"/repos/{repository}/issues/{number}",
                refresh=refresh,
            )
        except GitHubApiError as error:
            if error.status != 404:
                raise
            payload = self.get_json(
                f"/repos/{repository}/pulls/{number}",
                refresh=refresh,
            )
            if not isinstance(payload, dict):
                raise GitHubApiError("GitHub pull request response must be an object")
            issue = payload
            pull = payload
        if not isinstance(issue, dict):
            raise GitHubApiError("GitHub issue response must be an object")

        is_pull_request = pull is not None or isinstance(issue.get("pull_request"), dict)
        commits: list[dict[str, Any]] = []
        files: list[dict[str, Any]] = []
        if is_pull_request:
            if pull is None:
                payload = self.get_json(
                    f"/repos/{repository}/pulls/{number}",
                    refresh=refresh,
                )
                if not isinstance(payload, dict):
                    raise GitHubApiError(
                        "GitHub pull request response must be an object"
                    )
                pull = payload
            if include_commits:
                raw_commits = self.get_paginated(
                    f"/repos/{repository}/pulls/{number}/commits",
                    refresh=refresh,
                )
                commits = [_normalize_commit(item) for item in raw_commits]
            if include_files:
                raw_files = self.get_paginated(
                    f"/repos/{repository}/pulls/{number}/files",
                    refresh=refresh,
                )
                files = [_normalize_file(item) for item in raw_files]

        body = str(issue.get("body") or "")
        linked_issue_numbers = sorted(
            {
                int(value)
                for value in CLOSING_REFERENCE_RE.findall(body)
                if int(value) != number
            }
        )
        quality = score_episode(
            issue=issue,
            pull=pull,
            commits=commits,
            files=files,
            linked_issue_numbers=linked_issue_numbers,
        )
        episode = GitHubEpisode(
            repository=repository,
            number=number,
            kind="pull_request" if is_pull_request else "issue",
            title=str(issue.get("title") or ""),
            body=body,
            state=str(issue.get("state") or ""),
            state_reason=_optional_text(issue.get("state_reason")),
            html_url=str(issue.get("html_url") or ""),
            created_at=_optional_text(issue.get("created_at")),
            updated_at=_optional_text(issue.get("updated_at")),
            closed_at=_optional_text(issue.get("closed_at")),
            merged=bool(pull and pull.get("merged")),
            merged_at=_optional_text(pull.get("merged_at") if pull else None),
            base_ref=_nested_text(pull, "base", "ref"),
            base_sha=_nested_text(pull, "base", "sha"),
            head_ref=_nested_text(pull, "head", "ref"),
            head_sha=_nested_text(pull, "head", "sha"),
            merge_commit_sha=_optional_text(
                pull.get("merge_commit_sha") if pull else None
            ),
            author=_nested_text(issue, "user", "login"),
            author_association=_optional_text(issue.get("author_association")),
            labels=sorted(
                str(label.get("name"))
                for label in issue.get("labels", [])
                if isinstance(label, dict) and label.get("name")
            ),
            linked_issue_numbers=linked_issue_numbers,
            commits=commits,
            files=files,
            quality=quality,
            fetched_at=_utc_now(),
        )
        if persist_manifest:
            self.write_episode_manifest(episode)
        return episode

    def write_episode_manifest(self, episode: GitHubEpisode) -> Path:
        owner, name = episode.repository.split("/", 1)
        path = (
            self.cache_root
            / "episodes"
            / owner
            / name
            / f"{episode.number}.json"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(episode.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return path

    def _cache_path(self, url: str) -> Path:
        digest = sha256(url.encode("utf-8")).hexdigest()
        return self.cache_root / "http" / digest[:2] / f"{digest}.json"

    @staticmethod
    def _read_cache(path: Path) -> dict[str, Any] | None:
        if not path.exists():
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None

    @staticmethod
    def _write_cache(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


def score_episode(
    *,
    issue: Mapping[str, Any],
    pull: Mapping[str, Any] | None,
    commits: list[dict[str, Any]],
    files: list[dict[str, Any]],
    linked_issue_numbers: list[int],
) -> EpisodeQuality:
    reasons: list[str] = []
    score = 0.0
    title = str(issue.get("title") or "").strip()
    implementation_files = sum(_is_implementation_file(item["filename"]) for item in files)
    test_files = sum(_is_test_path(item["filename"]) for item in files)
    docs_files = sum(_is_documentation(item["filename"]) for item in files)
    generated_files = sum(_is_generated_or_lock(item["filename"]) for item in files)

    if pull is not None:
        if pull.get("merged"):
            score += 0.30
            reasons.append("merged pull request")
        else:
            score -= 0.35
            reasons.append("pull request is not merged")
    elif issue.get("state") == "closed":
        score += 0.10
        reasons.append("closed issue without verified implementation PR")
    else:
        score -= 0.25
        reasons.append("open issue")

    if title and not GENERIC_TITLE_RE.match(title):
        score += 0.10
        reasons.append("descriptive title")
    else:
        score -= 0.15
        reasons.append("generic maintenance title")

    if implementation_files:
        score += 0.25
        reasons.append(f"{implementation_files} implementation files")
    elif files:
        score -= 0.25
        reasons.append("no implementation file")

    if test_files:
        score += 0.20
        reasons.append(f"{test_files} test files")
    elif files:
        score -= 0.10
        reasons.append("no test file")

    if linked_issue_numbers:
        score += 0.08
        reasons.append("explicit closing issue reference")

    if commits:
        score += 0.05
        reasons.append(f"{len(commits)} PR commits")

    non_docs = len(files) - docs_files - generated_files
    if files and non_docs <= 0:
        score -= 0.25
        reasons.append("docs/generated-only change")

    normalized = max(0.0, min(1.0, score))
    tier = "strong" if normalized >= 0.75 else "medium" if normalized >= 0.55 else "weak"
    return EpisodeQuality(
        score=round(normalized, 4),
        tier=tier,
        reasons=reasons,
        implementation_files=implementation_files,
        test_files=test_files,
        docs_files=docs_files,
        generated_files=generated_files,
    )


def _normalize_commit(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    commit = value.get("commit") if isinstance(value.get("commit"), dict) else {}
    author = commit.get("author") if isinstance(commit.get("author"), dict) else {}
    return {
        "sha": str(value.get("sha") or ""),
        "message": str(commit.get("message") or ""),
        "authored_at": _optional_text(author.get("date")),
        "html_url": str(value.get("html_url") or ""),
        "parents": [
            str(parent.get("sha"))
            for parent in value.get("parents", [])
            if isinstance(parent, dict) and parent.get("sha")
        ],
    }


def _normalize_file(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return {
        "filename": str(value.get("filename") or ""),
        "status": str(value.get("status") or ""),
        "previous_filename": _optional_text(value.get("previous_filename")),
        "additions": int(value.get("additions") or 0),
        "deletions": int(value.get("deletions") or 0),
        "changes": int(value.get("changes") or 0),
        "blob_url": str(value.get("blob_url") or ""),
    }


def _is_implementation_file(filename: str) -> bool:
    path = Path(filename.lower())
    if _is_test_path(filename) or _is_documentation(filename) or _is_generated_or_lock(filename):
        return False
    return path.suffix in SOURCE_SUFFIXES


def _is_test_path(filename: str) -> bool:
    lowered = f"/{filename.lower().strip('/')}"
    name = Path(lowered).name
    return any(
        marker in lowered
        for marker in (
            "/test/",
            "/tests/",
            "/spec/",
            "/specs/",
            "/fixture/",
            "/fixtures/",
        )
    ) or any(marker in name for marker in (".test.", ".spec.", "_test.", "test_"))


def _is_documentation(filename: str) -> bool:
    lowered = filename.lower()
    suffix = Path(lowered).suffix
    return (
        suffix in {".md", ".mdx", ".rst", ".txt"}
        or lowered.startswith("docs/")
        or "/docs/" in f"/{lowered}"
        or lowered.startswith("website/")
    )


def _is_generated_or_lock(filename: str) -> bool:
    lowered = filename.lower()
    return (
        Path(lowered).name in GENERATED_OR_LOCK_FILES
        or lowered.startswith("dist/")
        or lowered.startswith("build/")
        or "/generated/" in f"/{lowered}"
    )


def _urllib_transport(request: Request, timeout: float) -> HttpResponse:
    try:
        with urlopen(request, timeout=timeout) as response:
            return HttpResponse(
                status=int(response.status),
                headers={key.lower(): value for key, value in response.headers.items()},
                body=response.read(),
            )
    except HTTPError as error:
        return HttpResponse(
            status=int(error.code),
            headers={key.lower(): value for key, value in error.headers.items()},
            body=error.read(),
        )


def _render_api_error(url: str, response: HttpResponse) -> str:
    message = response.body.decode("utf-8", errors="replace")
    try:
        payload = json.loads(message)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict) and payload.get("message"):
        message = str(payload["message"])
    remaining = _header(response.headers, "x-ratelimit-remaining")
    suffix = f"; rate-limit remaining={remaining}" if remaining is not None else ""
    return f"GitHub API {response.status} for {url}: {message}{suffix}"


def _header(headers: Mapping[str, str], name: str) -> str | None:
    lowered = name.lower()
    for key, value in headers.items():
        if key.lower() == lowered:
            return str(value)
    return None


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    rendered = str(value)
    return rendered if rendered else None


def _nested_text(value: Mapping[str, Any] | None, key: str, nested: str) -> str | None:
    if value is None:
        return None
    child = value.get(key)
    if not isinstance(child, Mapping):
        return None
    return _optional_text(child.get(nested))


def _validate_repository(repository: str) -> None:
    parts = repository.split("/")
    if (
        len(parts) != 2
        or not all(parts)
        or any(part in {".", ".."} for part in parts)
        or any("\\" in part for part in parts)
    ):
        raise ValueError("repository must have the form owner/name")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
