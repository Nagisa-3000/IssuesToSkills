from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Iterator

from .github import CLOSING_REFERENCE_RE, EpisodeQuality, score_episode


MERGE_PULL_RE = re.compile(
    r"\bMerge\s+(?:pull request|PR)\s+#(\d+)\b",
    re.IGNORECASE,
)


MODULE_FAMILY_TERMS: dict[str, tuple[str, ...]] = {
    "session_lifecycle": (
        "session",
        "conversation",
        "fork session",
        "branch session",
    ),
    "session_persistence": (
        "session persistence",
        "session-persistence",
        "session store",
        "session log",
        "session history",
        "persist",
        "persisted",
        "persistence",
        "resume",
        "checkpoint",
        "conversation history",
        "event log",
    ),
    "context_compaction": (
        "compact",
        "compaction",
        "context window",
        "summar",
        "token budget",
        "truncate context",
    ),
    "tool_execution": (
        "tool call",
        "tool execution",
        "tool-result",
        "tool_result",
        "/tools/",
        "tool-",
        "tool_",
        "approval",
        "cancellation",
        "cancel tool",
        "output truncation",
    ),
    "model_provider_adapter": (
        "llm",
        "model provider",
        "provider adapter",
        "anthropic",
        "openai",
        "gemini",
        "bedrock",
        "ollama",
    ),
    "auth_credentials": (
        "oauth",
        "credential",
        "authentication",
        "api key",
        "secret store",
    ),
    "extension_plugin_loading": (
        "plugin",
        "extension",
        "bundle loading",
        "registry lifecycle",
        "hot reload",
    ),
    "skill_prompt_discovery": (
        "skill",
        "system prompt",
        "prompt discovery",
        "instructions",
    ),
    "mcp_acp_rpc": (
        "mcp",
        "acp",
        "json-rpc",
        "jsonrpc",
        "rpc server",
    ),
    "tui_cli": (
        "tui",
        "cli",
        "terminal ui",
        "command line",
        "slash command",
    ),
    "configuration": (
        "config",
        "configuration",
        "settings",
        "environment variable",
        "precedence",
    ),
    "sandbox_shell": (
        "sandbox",
        "shell",
        "bash",
        "subprocess",
        "terminal",
        "pty",
    ),
    "ui_surface": (
        "user interface",
        "ui",
        "web",
        "sidebar",
        "desktop",
        "electron",
        "dashboard",
    ),
}


SYNC_OR_MAINTENANCE_TITLE_RE = re.compile(
    r"(?:\b(?:merge|sync|integrat(?:e|es|ed|ing)|rebase)\b.{0,28}\b(?:main|master|trunk|upstream|latest)\b"
    r"|\b(?:dependency|dependencies|deps)\s+bump\b"
    r"|^\s*(?:chore|style|ci|docs|release)(?:\([^)]*\))?\s*:)",
    re.IGNORECASE,
)


@dataclass(slots=True)
class MergeRecord:
    sha: str
    parents: tuple[str, ...]
    authored_at: str
    subject: str
    body: str
    number: int


@dataclass(slots=True)
class LocalPullEpisode:
    repository: str
    number: int
    title: str
    merge_sha: str
    base_sha: str
    head_sha: str
    merged_at: str
    commits: list[dict[str, Any]]
    files: list[dict[str, Any]]
    linked_issue_numbers: list[int]
    quality: EpisodeQuality
    provenance: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LocalEpisodeCandidate:
    repository: str
    number: int
    title: str
    merge_sha: str
    merged_at: str
    commit_count: int
    file_count: int
    linked_issue_numbers: list[int]
    module_families: list[str]
    selection_score: float
    selection_tier: str
    review_flags: list[str]
    merge_commit_count: int
    top_level_areas: list[str]
    commit_subjects: list[str]
    file_sample: list[str]
    quality: EpisodeQuality

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LocalEpisodeProfile:
    repository: str
    repository_path: str
    ref: str
    total_merge_commits: int
    matched_pr_merges: int
    extracted_episodes: int
    failed_episodes: int
    skipped_too_large: int
    duplicate_pr_numbers: int
    tier_counts: dict[str, int]
    selection_tier_counts: dict[str, int]
    module_family_counts: dict[str, int]
    commit_count_total: int
    file_count_total: int
    candidates: list[LocalEpisodeCandidate]
    family_candidates: dict[str, list[LocalEpisodeCandidate]]
    errors: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EpisodeTooLargeError(ValueError):
    def __init__(self, number: int, commit_count: int, max_commits: int):
        self.number = number
        self.commit_count = commit_count
        self.max_commits = max_commits
        super().__init__(
            f"PR #{number} contains {commit_count} commits, "
            f"exceeding max_commits={max_commits}"
        )


class LocalMergeEpisodeExtractor:
    """Recover a merged PR episode from the local Git object graph.

    This path is important for repositories that publish Git history but do not
    expose Issues or Pull Requests through the GitHub API. The merge result
    against the first parent is the authoritative file set, while commits are
    recovered from first-parent base to the second-parent PR head.
    """

    def __init__(self, repo_path: str | Path, repository: str):
        self.repo_path = Path(repo_path).resolve()
        self.repository = repository
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"not a git repository: {self.repo_path}")

    def find(self, number: int, *, ref: str = "--all") -> MergeRecord | None:
        if number <= 0:
            raise ValueError("number must be positive")
        for record in self.iter_merges(ref=ref):
            if record.number == number:
                return record
        return None

    def extract(
        self,
        number: int,
        *,
        ref: str = "--all",
        max_commits: int = 500,
    ) -> LocalPullEpisode:
        merge = self.find(number, ref=ref)
        if merge is None:
            raise KeyError(f"no merge commit found for PR #{number}")
        return self.extract_record(merge, max_commits=max_commits)

    def extract_record(
        self,
        merge: MergeRecord,
        *,
        max_commits: int = 500,
    ) -> LocalPullEpisode:
        if len(merge.parents) < 2:
            raise ValueError(f"merge commit {merge.sha} has fewer than two parents")

        base_sha, head_sha = merge.parents[:2]
        commit_range = f"{base_sha}..{head_sha}"
        commit_count = int(self._git("rev-list", "--count", commit_range).strip() or "0")
        if commit_count > max_commits:
            raise EpisodeTooLargeError(merge.number, commit_count, max_commits)
        commits = self._commit_summaries(commit_range)
        files = [
            {
                "filename": line,
                "status": "changed",
                "previous_filename": None,
                "additions": 0,
                "deletions": 0,
                "changes": 0,
                "blob_url": "",
            }
            for line in self._git(
                "diff",
                "--name-only",
                "--no-renames",
                base_sha,
                merge.sha,
            ).splitlines()
            if line
        ]
        title = _episode_title(merge, commits)
        closing_text = "\n".join(
            [merge.body, *(str(commit.get("message") or "") for commit in commits)]
        )
        linked_issue_numbers = sorted(
            {
                int(value)
                for value in CLOSING_REFERENCE_RE.findall(closing_text)
                if int(value) != merge.number
            }
        )
        quality = score_episode(
            issue={"title": title, "state": "closed"},
            pull={"merged": True},
            commits=commits,
            files=files,
            linked_issue_numbers=linked_issue_numbers,
        )
        return LocalPullEpisode(
            repository=self.repository,
            number=merge.number,
            title=title,
            merge_sha=merge.sha,
            base_sha=base_sha,
            head_sha=head_sha,
            merged_at=merge.authored_at,
            commits=commits,
            files=files,
            linked_issue_numbers=linked_issue_numbers,
            quality=quality,
            provenance={
                "kind": "local_merge_commit",
                "repository_path": str(self.repo_path),
                "merge_subject": merge.subject,
                "merge_body": merge.body,
                "file_set": "first_parent_to_merge_result",
                "commit_set": "first_parent_to_second_parent",
            },
        )

    def profile(
        self,
        *,
        ref: str = "--all",
        limit: int | None = None,
        max_commits: int = 500,
        candidate_limit: int = 200,
        family_candidate_limit: int = 20,
        min_score: float = 0.0,
        manifest_dir: str | Path | None = None,
    ) -> LocalEpisodeProfile:
        if limit is not None and limit <= 0:
            raise ValueError("limit must be positive")
        if max_commits <= 0:
            raise ValueError("max_commits must be positive")
        if candidate_limit < 0:
            raise ValueError("candidate_limit must be non-negative")
        if family_candidate_limit < 0:
            raise ValueError("family_candidate_limit must be non-negative")
        if not 0.0 <= min_score <= 1.0:
            raise ValueError("min_score must be in [0, 1]")

        total_merge_commits = int(
            self._git("rev-list", "--merges", "--count", *self._ref_args(ref)).strip()
            or "0"
        )
        matched_pr_merges = 0
        extracted: list[LocalPullEpisode] = []
        errors: list[dict[str, Any]] = []
        skipped_too_large = 0
        seen_numbers: set[int] = set()
        duplicate_pr_numbers = 0
        destination = Path(manifest_dir).resolve() if manifest_dir is not None else None

        for merge in self.iter_merges(ref=ref):
            if limit is not None and matched_pr_merges >= limit:
                break
            matched_pr_merges += 1
            if merge.number in seen_numbers:
                duplicate_pr_numbers += 1
            seen_numbers.add(merge.number)
            try:
                episode = self.extract_record(merge, max_commits=max_commits)
            except EpisodeTooLargeError as error:
                skipped_too_large += 1
                errors.append(
                    {
                        "number": merge.number,
                        "merge_sha": merge.sha,
                        "kind": "too_large",
                        "commit_count": error.commit_count,
                        "message": str(error),
                    }
                )
                continue
            except (OSError, subprocess.CalledProcessError, ValueError) as error:
                errors.append(
                    {
                        "number": merge.number,
                        "merge_sha": merge.sha,
                        "kind": "extract_error",
                        "message": str(error),
                    }
                )
                continue
            extracted.append(episode)
            if destination is not None:
                self._write_manifest(destination, episode)

        tier_counts = Counter(episode.quality.tier for episode in extracted)
        selection_tier_counts: Counter[str] = Counter()
        module_counts: Counter[str] = Counter()
        candidates: list[LocalEpisodeCandidate] = []
        for episode in extracted:
            families = infer_module_families(episode)
            module_counts.update(families)
            review = review_episode(episode, families)
            selection_tier_counts[review[1]] += 1
            if review[0] < min_score:
                continue
            candidates.append(
                LocalEpisodeCandidate(
                    repository=episode.repository,
                    number=episode.number,
                    title=episode.title,
                    merge_sha=episode.merge_sha,
                    merged_at=episode.merged_at,
                    commit_count=len(episode.commits),
                    file_count=len(episode.files),
                    linked_issue_numbers=episode.linked_issue_numbers,
                    module_families=families,
                    selection_score=review[0],
                    selection_tier=review[1],
                    review_flags=review[2],
                    merge_commit_count=review[3],
                    top_level_areas=review[4],
                    commit_subjects=[
                        str(commit.get("subject") or "")
                        for commit in episode.commits[:12]
                    ],
                    file_sample=[
                        str(item.get("filename") or "")
                        for item in episode.files[:20]
                    ],
                    quality=episode.quality,
                )
            )
        candidates.sort(
            key=lambda item: (
                item.selection_score,
                item.quality.score,
                item.quality.test_files > 0,
                item.quality.implementation_files,
                item.commit_count,
                item.merged_at,
            ),
            reverse=True,
        )
        family_candidates = {
            family: [
                candidate
                for candidate in candidates
                if family in candidate.module_families
            ][:family_candidate_limit]
            for family in MODULE_FAMILY_TERMS
        }
        family_candidates = {
            family: rows for family, rows in family_candidates.items() if rows
        }
        candidates = candidates[:candidate_limit]
        return LocalEpisodeProfile(
            repository=self.repository,
            repository_path=str(self.repo_path),
            ref=ref,
            total_merge_commits=total_merge_commits,
            matched_pr_merges=matched_pr_merges,
            extracted_episodes=len(extracted),
            failed_episodes=len(errors),
            skipped_too_large=skipped_too_large,
            duplicate_pr_numbers=duplicate_pr_numbers,
            tier_counts=dict(sorted(tier_counts.items())),
            selection_tier_counts=dict(sorted(selection_tier_counts.items())),
            module_family_counts=dict(
                sorted(module_counts.items(), key=lambda item: (-item[1], item[0]))
            ),
            commit_count_total=sum(len(episode.commits) for episode in extracted),
            file_count_total=sum(len(episode.files) for episode in extracted),
            candidates=candidates,
            family_candidates=family_candidates,
            errors=errors[:100],
        )

    def iter_merges(self, *, ref: str = "--all") -> Iterator[MergeRecord]:
        args = [
            "log",
            "--merges",
            "--format=%x1e%H%x00%P%x00%aI%x00%s%x00%b",
        ]
        args.extend(self._ref_args(ref))
        output = self._git(*args)
        for raw in output.split("\x1e"):
            raw = raw.strip("\n")
            if not raw:
                continue
            fields = raw.split("\x00")
            if len(fields) < 5:
                continue
            sha, parents, authored_at, subject = fields[:4]
            body = "\x00".join(fields[4:]).strip()
            match = MERGE_PULL_RE.search(subject)
            if match is None:
                continue
            yield MergeRecord(
                sha=sha,
                parents=tuple(parent for parent in parents.split() if parent),
                authored_at=authored_at,
                subject=subject.strip(),
                body=body,
                number=int(match.group(1)),
            )

    def _commit_summaries(self, commit_range: str) -> list[dict[str, Any]]:
        output = self._git(
            "log",
            "--reverse",
            "--topo-order",
            "--format=%x1e%H%x00%P%x00%aI%x00%s%x00%b",
            commit_range,
        )
        commits: list[dict[str, Any]] = []
        for raw in output.split("\x1e"):
            raw = raw.strip("\n")
            if not raw:
                continue
            fields = raw.split("\x00")
            if len(fields) < 5:
                raise ValueError(f"cannot parse commit record in {commit_range}")
            parsed_sha, parents, authored_at, subject = fields[:4]
            body = "\x00".join(fields[4:]).strip()
            commits.append(
                {
                    "sha": parsed_sha,
                    "parents": [parent for parent in parents.split() if parent],
                    "authored_at": authored_at,
                    "subject": subject.strip(),
                    "body": body,
                    "message": "\n\n".join(
                        part for part in (subject.strip(), body) if part
                    ),
                }
            )
        return commits

    @staticmethod
    def _ref_args(ref: str) -> list[str]:
        return ["--all"] if ref == "--all" else [ref]

    @staticmethod
    def _write_manifest(destination: Path, episode: LocalPullEpisode) -> Path:
        repository_path = Path(*episode.repository.split("/"))
        path = destination / repository_path / f"{episode.number}-{episode.merge_sha[:12]}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(episode.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return path

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


def _episode_title(merge: MergeRecord, commits: list[dict[str, Any]]) -> str:
    for line in merge.body.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    for commit in reversed(commits):
        subject = str(commit.get("subject") or "").strip()
        if subject:
            return subject
    return merge.subject


def infer_module_families(episode: LocalPullEpisode) -> list[str]:
    semantic_text = "\n".join(
        [episode.title, *(str(commit.get("subject") or "") for commit in episode.commits)]
    ).lower()
    file_texts = [
        str(item.get("filename") or "").lower()
        for item in episode.files
        if item.get("filename")
    ]
    families: list[str] = []
    for family, terms in MODULE_FAMILY_TERMS.items():
        semantic_match = any(_contains_term(semantic_text, term) for term in terms)
        matching_files = sum(
            any(_contains_term(filename, term) for term in terms)
            for filename in file_texts
        )
        if semantic_match or matching_files >= 2:
            families.append(family)
    return families or ["other"]


def review_episode(
    episode: LocalPullEpisode,
    module_families: list[str] | None = None,
) -> tuple[float, str, list[str], int, list[str]]:
    """Compute extraction suitability separately from evidence completeness.

    `EpisodeQuality` answers whether a merged episode has implementation and
    test evidence. This score answers whether the episode is a reasonably
    bounded, semantically reviewable unit for Skill extraction. The flags are
    deliberately retained so later human review can override the heuristic.
    """

    families = module_families or infer_module_families(episode)
    commit_count = len(episode.commits)
    file_count = len(episode.files)
    merge_commit_count = sum(
        len(commit.get("parents", [])) > 1 for commit in episode.commits
    )
    top_level_areas = sorted(
        {
            _top_level_area(str(item.get("filename") or ""))
            for item in episode.files
            if item.get("filename")
        }
    )
    flags: list[str] = []
    score = episode.quality.score

    if SYNC_OR_MAINTENANCE_TITLE_RE.search(episode.title):
        score -= 0.25
        flags.append("sync_or_maintenance_title")
    if merge_commit_count:
        score -= min(0.24, 0.04 * merge_commit_count)
        flags.append("contains_branch_merge_commits")
    if commit_count > 100:
        score -= 0.30
        flags.append("very_large_commit_set")
    elif commit_count > 50:
        score -= 0.18
        flags.append("large_commit_set")
    elif commit_count > 25:
        score -= 0.08
        flags.append("moderate_commit_set")
    if file_count > 300:
        score -= 0.30
        flags.append("very_large_file_set")
    elif file_count > 150:
        score -= 0.18
        flags.append("large_file_set")
    elif file_count > 80:
        score -= 0.08
        flags.append("moderate_file_set")
    if len(families) > 6:
        score -= 0.08
        flags.append("broad_module_surface")
    core_families = set(families) - {"ui_surface", "tui_cli", "configuration"}
    if "ui_surface" in families and not core_families:
        score -= 0.05
        flags.append("ui_surface_without_core_module")
    if len(top_level_areas) > 12:
        score -= 0.06
        flags.append("broad_top_level_surface")
    if episode.quality.test_files == 0:
        flags.append("missing_test_evidence")
    if (
        episode.quality.implementation_files > 0
        and episode.quality.test_files > 0
        and 1 <= commit_count <= 20
        and file_count <= 80
        and merge_commit_count == 0
    ):
        score += 0.04
    if episode.linked_issue_numbers:
        score += 0.02

    normalized = round(max(0.0, min(1.0, score)), 4)
    tier = "preferred" if normalized >= 0.75 else "review" if normalized >= 0.55 else "reject"
    return normalized, tier, flags, merge_commit_count, top_level_areas


def _contains_term(searchable: str, term: str) -> bool:
    normalized = term.lower()
    if re.fullmatch(r"[a-z0-9_-]+", normalized):
        return re.search(
            rf"(?<![a-z0-9]){re.escape(normalized)}(?![a-z0-9])",
            searchable,
        ) is not None
    return normalized in searchable


def _top_level_area(filename: str) -> str:
    parts = [part for part in filename.strip("/").split("/") if part]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    if parts[0] in {"packages", "apps", "src", "lib", "plugins", "extensions"}:
        return "/".join(parts[:2])
    return parts[0]
