from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import time
from typing import Iterator

from ..schema import Edge, Node, NodeType, RelationType, stable_id
from ..store import CatalogStore


ISSUE_RE = re.compile(
    r"(?:(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+)?#(\d+)",
    re.IGNORECASE,
)
CONVENTIONAL_PREFIX_RE = re.compile(
    r"^(?P<kind>fix|feat|perf|refactor|test|build|ci|docs|chore)"
    r"(?:\([^)]+\))?!?:\s*",
    re.IGNORECASE,
)


@dataclass(slots=True)
class CommitRecord:
    sha: str
    parents: tuple[str, ...]
    authored_at: str
    subject: str
    body: str
    files: tuple[str, ...]
    additions: int
    deletions: int
    issue_numbers: tuple[int, ...]


@dataclass(slots=True)
class MineReport:
    repository: str
    requested_limit: int
    commits_seen: int
    commits_indexed: int
    actions_indexed: int
    skipped_merges: int
    elapsed_seconds: float

    @property
    def commits_per_second(self) -> float:
        if self.elapsed_seconds == 0:
            return 0.0
        return self.commits_indexed / self.elapsed_seconds


class GitCommitMiner:
    def __init__(self, repo_path: str | Path, repository: str):
        self.repo_path = Path(repo_path).resolve()
        self.repository = repository
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"not a git repository: {self.repo_path}")

    def mine_to_store(
        self,
        store: CatalogStore,
        *,
        limit: int = 200,
        since: str | None = None,
    ) -> MineReport:
        started = time.perf_counter()
        commits_seen = 0
        commits_indexed = 0
        actions_indexed = 0
        skipped_merges = 0

        for record in self.iter_commits(limit=limit, since=since):
            commits_seen += 1
            if len(record.parents) > 1:
                skipped_merges += 1
                continue
            commit_node, action_node, edge = self.to_nodes(record)
            with store.transaction():
                store.upsert_node(commit_node)
                store.upsert_node(action_node)
                store.upsert_edge(edge)
            commits_indexed += 1
            actions_indexed += 1

        return MineReport(
            repository=self.repository,
            requested_limit=limit,
            commits_seen=commits_seen,
            commits_indexed=commits_indexed,
            actions_indexed=actions_indexed,
            skipped_merges=skipped_merges,
            elapsed_seconds=time.perf_counter() - started,
        )

    def iter_commits(
        self,
        *,
        limit: int,
        since: str | None = None,
    ) -> Iterator[CommitRecord]:
        args = [
            "log",
            "--format=%H%x00%P%x00%aI%x00%s%x00%b%x1e",
            f"--max-count={limit}",
        ]
        if since:
            args.append(f"--since={since}")
        output = self._git(*args)
        for raw_record in output.split("\x1e"):
            if not raw_record.strip():
                continue
            fields = raw_record.strip("\n").split("\x00")
            if len(fields) < 5:
                continue
            sha, parents, authored_at, subject = fields[:4]
            body = "\x00".join(fields[4:])
            files, additions, deletions = self._change_stats(sha)
            issue_numbers = tuple(
                sorted({int(match) for match in ISSUE_RE.findall(f"{subject}\n{body}")})
            )
            yield CommitRecord(
                sha=sha,
                parents=tuple(parent for parent in parents.split() if parent),
                authored_at=authored_at,
                subject=subject.strip(),
                body=body.strip(),
                files=files,
                additions=additions,
                deletions=deletions,
                issue_numbers=issue_numbers,
            )

    def read_commit(self, sha: str) -> CommitRecord:
        output = self._git(
            "show",
            "-s",
            "--format=%H%x00%P%x00%aI%x00%s%x00%b",
            sha,
        )
        fields = output.rstrip("\n").split("\x00")
        if len(fields) < 5:
            raise ValueError(f"cannot parse commit {sha}")
        parsed_sha, parents, authored_at, subject = fields[:4]
        body = "\x00".join(fields[4:]).strip()
        files, additions, deletions = self._change_stats(parsed_sha)
        issue_numbers = tuple(
            sorted({int(match) for match in ISSUE_RE.findall(f"{subject}\n{body}")})
        )
        return CommitRecord(
            sha=parsed_sha,
            parents=tuple(parent for parent in parents.split() if parent),
            authored_at=authored_at,
            subject=subject.strip(),
            body=body,
            files=files,
            additions=additions,
            deletions=deletions,
            issue_numbers=issue_numbers,
        )

    def to_nodes(self, record: CommitRecord) -> tuple[Node, Node, Edge]:
        operation = classify_operation(record.subject)
        roles = infer_module_roles(record.files)
        normalized_title = normalize_action_title(record.subject)
        semantic_density = semantic_density_score(record)

        commit_id = stable_id("commit", self.repository, record.sha)
        action_id = stable_id("action", self.repository, record.sha, normalized_title)

        commit_node = Node(
            id=commit_id,
            node_type=NodeType.COMMIT,
            title=record.subject,
            summary=(
                f"touches {len(record.files)} files; line statistics are deferred "
                "to asynchronous enrichment"
            ),
            repository=self.repository,
            facets={
                "authored_at": record.authored_at,
                "issue_numbers": record.issue_numbers,
                "operation": operation,
                "module_roles": roles,
            },
            payload={
                "sha": record.sha,
                "parents": record.parents,
                "files": record.files,
                "body": record.body,
                "line_stats_status": "not_collected",
                "routing_terms": [operation, *roles],
            },
            provenance={
                "kind": "git_commit",
                "repository_path": str(self.repo_path),
                "revision": record.sha,
            },
            confidence=1.0,
        )
        action_node = Node(
            id=action_id,
            node_type=NodeType.ACTION,
            title=normalized_title,
            summary=(
                f"{operation.replace('_', ' ')} in {', '.join(roles[:3]) or 'code'}; "
                f"changes {len(record.files)} files"
            ),
            repository=self.repository,
            facets={
                "operation": operation,
                "module_roles": roles,
                "issue_numbers": record.issue_numbers,
                "semantic_density": semantic_density,
            },
            payload={
                "pre_state": "not yet normalized",
                "post_state": normalized_title,
                "validation": infer_validation(record.files),
                "files": record.files,
                "line_stats_status": "not_collected",
                "routing_terms": [operation, *roles, *record.issue_numbers],
                "exclusions": [],
            },
            provenance={
                "kind": "deterministic_commit_action_candidate",
                "commit_sha": record.sha,
                "extractor": "git-v1",
            },
            confidence=max(0.25, min(0.85, semantic_density)),
        )
        edge = Edge.create(
            action_id,
            commit_id,
            RelationType.EVIDENCED_BY,
            weight=1.0,
            confidence=1.0,
            evidence_ids=(commit_id,),
            provenance={"method": "deterministic", "extractor": "git-v1"},
        )
        return commit_node, action_node, edge

    def _change_stats(self, sha: str) -> tuple[tuple[str, ...], int, int]:
        names = self._git(
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-only",
            "-r",
            sha,
        )
        files = tuple(line.strip() for line in names.splitlines() if line.strip())
        return files, 0, 0

    def _git(self, *args: str) -> str:
        completed = subprocess.run(
            ["git", *args],
            cwd=self.repo_path,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return completed.stdout


def normalize_action_title(subject: str) -> str:
    title = CONVENTIONAL_PREFIX_RE.sub("", subject).strip()
    title = re.sub(r"\s*\((?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)?\s*#\d+\)\s*$", "", title)
    title = re.sub(r"\s*,?\s*(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#\d+\s*$", "", title, flags=re.IGNORECASE)
    return title or subject.strip()


def classify_operation(subject: str) -> str:
    match = CONVENTIONAL_PREFIX_RE.match(subject)
    if match:
        kind = match.group("kind").lower()
        return {
            "fix": "bug_fix",
            "feat": "feature_support",
            "perf": "optimization",
            "refactor": "refactor",
            "test": "validation",
            "build": "build_change",
            "ci": "ci_change",
            "docs": "documentation",
            "chore": "maintenance",
        }[kind]
    lowered = subject.lower()
    if any(word in lowered for word in ("fix", "prevent", "restore", "handle")):
        return "bug_fix"
    if any(word in lowered for word in ("add", "support", "introduce", "enable")):
        return "feature_support"
    if any(word in lowered for word in ("speed", "performance", "optimiz", "cache")):
        return "optimization"
    if any(word in lowered for word in ("test", "verify", "assert")):
        return "validation"
    return "change"


ROLE_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("validation", ("test", "spec", "fixture", "benchmark")),
    ("skill_system", ("skill", "prompt", "instruction")),
    ("tool_execution", ("tool", "function_call", "command")),
    ("model_provider", ("provider", "model", "openai", "anthropic", "llm")),
    ("session_state", ("session", "history", "state", "transcript", "persist")),
    ("context_management", ("context", "compress", "compact", "token")),
    ("authentication", ("auth", "oauth", "credential", "login")),
    ("interaction_surface", ("tui", "ui", "web", "desktop", "cli")),
    ("configuration", ("config", "setting", "preference")),
    ("execution_environment", ("sandbox", "shell", "exec", "terminal")),
    ("extension_system", ("plugin", "extension", "hook")),
    ("memory", ("memory", "recall")),
    ("protocol_integration", ("mcp", "acp", "lsp", "rpc", "api")),
)


def infer_module_roles(files: tuple[str, ...]) -> list[str]:
    lowered = [path.lower() for path in files]
    roles = [
        role
        for role, patterns in ROLE_PATTERNS
        if any(any(pattern in path for pattern in patterns) for path in lowered)
    ]
    return roles or ["core_runtime"]


def infer_validation(files: tuple[str, ...]) -> dict[str, object]:
    tests = [
        path
        for path in files
        if any(part in path.lower() for part in ("test", "spec", "fixture"))
    ]
    return {
        "test_files_changed": tests,
        "has_test_evidence": bool(tests),
        "status": "candidate" if tests else "unknown",
    }


def semantic_density_score(record: CommitRecord) -> float:
    score = 0.35
    if record.issue_numbers:
        score += 0.15
    if CONVENTIONAL_PREFIX_RE.match(record.subject):
        score += 0.10
    if infer_validation(record.files)["has_test_evidence"]:
        score += 0.15
    if 1 <= len(record.files) <= 12:
        score += 0.10
    if classify_operation(record.subject) not in {"change", "maintenance", "documentation"}:
        score += 0.05
    return min(score, 1.0)
