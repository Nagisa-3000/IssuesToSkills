from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
import re
import subprocess
from typing import Iterator

from .git import (
    CommitRecord,
    ISSUE_RE,
    classify_operation,
    infer_module_roles,
    infer_validation,
)


MERGE_PR_RE = re.compile(r"Merge pull request #(\d+)", re.IGNORECASE)
GENERIC_SUBJECT_RE = re.compile(
    r"^(copy|update|changes?|cleanup|misc|wip|chore|bump|release|fmt|format|style|revert)\b",
    re.IGNORECASE,
)
LOCK_OR_GENERATED = (
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "uv.lock",
    "poetry.lock",
    "Cargo.lock",
)
REUSABLE_OPERATIONS = frozenset(
    {
        "bug_fix",
        "feature_support",
        "optimization",
        "refactor",
        "validation",
    }
)


@dataclass(slots=True)
class ProfileCandidate:
    sha: str
    authored_at: str
    subject: str
    operation: str
    module_roles: list[str]
    issue_numbers: list[int]
    file_count: int
    has_test_evidence: bool
    quality_score: float
    quality_reasons: list[str]


@dataclass(slots=True)
class EpisodeCandidate:
    anchor_number: int
    commit_count: int
    implementation_commit_count: int
    test_commit_count: int
    file_count: int
    operations: list[str]
    module_roles: list[str]
    quality_score: float
    subjects: list[str]


@dataclass(slots=True)
class RepositoryProfile:
    repository: str
    revision: str
    total_commits: int
    non_merge_commits: int
    merge_commits: int
    unique_issue_references: int
    unique_merged_pr_references: int
    commits_with_issue_reference: int
    commits_with_test_evidence: int
    docs_only_commits: int
    strong_candidates: int
    medium_candidates: int
    anchored_episodes: int
    episodes_with_implementation: int
    episodes_with_test_evidence: int
    strong_episode_candidates: int
    medium_episode_candidates: int
    operation_counts: dict[str, int]
    module_role_counts: dict[str, int]
    strong_examples: list[ProfileCandidate]
    strong_episode_examples: list[EpisodeCandidate]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        return payload


class RepositoryProfiler:
    def __init__(self, repo_path: str | Path, repository: str):
        self.repo_path = Path(repo_path).resolve()
        self.repository = repository
        if not (self.repo_path / ".git").exists():
            raise ValueError(f"not a git repository: {self.repo_path}")

    def profile(
        self,
        *,
        ref: str = "HEAD",
        max_count: int | None = None,
        example_limit: int = 30,
    ) -> RepositoryProfile:
        total = 0
        non_merge = 0
        merges = 0
        issue_numbers: set[int] = set()
        merged_pr_numbers: set[int] = set()
        with_issue = 0
        with_test = 0
        docs_only = 0
        strong = 0
        medium = 0
        operations: Counter[str] = Counter()
        roles: Counter[str] = Counter()
        candidates: list[ProfileCandidate] = []
        episode_groups: dict[int, list[tuple[CommitRecord, str, list[str]]]] = {}

        for record in self.iter_commits(ref=ref, max_count=max_count):
            total += 1
            merge_prs = {int(value) for value in MERGE_PR_RE.findall(record.subject)}
            merged_pr_numbers.update(merge_prs)
            if len(record.parents) > 1:
                merges += 1
                continue
            non_merge += 1
            operation = classify_operation(record.subject)
            operations[operation] += 1
            module_roles = infer_module_roles(record.files)
            roles.update(module_roles)
            issue_numbers.update(record.issue_numbers)
            if record.issue_numbers:
                with_issue += 1
                for issue_number in record.issue_numbers:
                    episode_groups.setdefault(issue_number, []).append(
                        (record, operation, module_roles)
                    )
            has_tests = bool(infer_validation(record.files)["has_test_evidence"])
            if has_tests:
                with_test += 1
            is_docs_only = bool(record.files) and all(
                _is_documentation(path) for path in record.files
            )
            if is_docs_only:
                docs_only += 1

            score, reasons = quality_score(
                record,
                operation=operation,
                module_roles=module_roles,
                has_tests=has_tests,
                docs_only=is_docs_only,
            )
            if score >= 0.70:
                strong += 1
            if score >= 0.55:
                medium += 1
                candidates.append(
                    ProfileCandidate(
                        sha=record.sha,
                        authored_at=record.authored_at,
                        subject=record.subject,
                        operation=operation,
                        module_roles=module_roles,
                        issue_numbers=list(record.issue_numbers),
                        file_count=len(record.files),
                        has_test_evidence=has_tests,
                        quality_score=score,
                        quality_reasons=reasons,
                    )
                )

        candidates.sort(
            key=lambda candidate: (
                candidate.quality_score,
                candidate.has_test_evidence,
                bool(candidate.issue_numbers),
                -candidate.file_count,
            ),
            reverse=True,
        )
        episode_candidates = [
            build_episode_candidate(anchor_number, entries)
            for anchor_number, entries in episode_groups.items()
        ]
        episode_candidates.sort(
            key=lambda candidate: (
                candidate.quality_score,
                candidate.test_commit_count,
                candidate.implementation_commit_count,
                -candidate.commit_count,
            ),
            reverse=True,
        )
        episodes_with_implementation = sum(
            candidate.implementation_commit_count > 0
            for candidate in episode_candidates
        )
        episodes_with_test_evidence = sum(
            candidate.test_commit_count > 0 for candidate in episode_candidates
        )
        strong_episode_candidates = sum(
            candidate.quality_score >= 0.75
            and candidate.implementation_commit_count > 0
            and candidate.test_commit_count > 0
            for candidate in episode_candidates
        )
        medium_episode_candidates = sum(
            candidate.quality_score >= 0.60
            and candidate.implementation_commit_count > 0
            for candidate in episode_candidates
        )
        return RepositoryProfile(
            repository=self.repository,
            revision=self._git("rev-parse", ref).strip(),
            total_commits=total,
            non_merge_commits=non_merge,
            merge_commits=merges,
            unique_issue_references=len(issue_numbers),
            unique_merged_pr_references=len(merged_pr_numbers),
            commits_with_issue_reference=with_issue,
            commits_with_test_evidence=with_test,
            docs_only_commits=docs_only,
            strong_candidates=strong,
            medium_candidates=medium,
            anchored_episodes=len(episode_candidates),
            episodes_with_implementation=episodes_with_implementation,
            episodes_with_test_evidence=episodes_with_test_evidence,
            strong_episode_candidates=strong_episode_candidates,
            medium_episode_candidates=medium_episode_candidates,
            operation_counts=dict(operations.most_common()),
            module_role_counts=dict(roles.most_common()),
            strong_examples=candidates[:example_limit],
            strong_episode_examples=[
                candidate
                for candidate in episode_candidates
                if candidate.quality_score >= 0.75
                and candidate.implementation_commit_count > 0
                and candidate.test_commit_count > 0
            ][:example_limit],
        )

    def iter_commits(
        self,
        *,
        ref: str,
        max_count: int | None,
    ) -> Iterator[CommitRecord]:
        args = [
            "log",
            ref,
            "--format=%x1e%H%x00%P%x00%aI%x00%s%x00%b",
            "--name-only",
            "--no-renames",
        ]
        if max_count is not None:
            args.append(f"--max-count={max_count}")
        output = self._git(*args)
        for raw in output.split("\x1e"):
            raw = raw.strip("\n")
            if not raw:
                continue
            header, _, paths_text = raw.partition("\n")
            fields = header.split("\x00")
            if len(fields) < 5:
                continue
            sha, parents, authored_at, subject = fields[:4]
            body = "\x00".join(fields[4:])
            files = tuple(
                line.strip()
                for line in paths_text.splitlines()
                if line.strip()
            )
            refs = tuple(
                sorted({int(match) for match in ISSUE_RE.findall(f"{subject}\n{body}")})
            )
            yield CommitRecord(
                sha=sha,
                parents=tuple(parent for parent in parents.split() if parent),
                authored_at=authored_at,
                subject=subject.strip(),
                body=body.strip(),
                files=files,
                additions=0,
                deletions=0,
                issue_numbers=refs,
            )

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


def quality_score(
    record: CommitRecord,
    *,
    operation: str,
    module_roles: list[str],
    has_tests: bool,
    docs_only: bool,
) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    implementation_files = [
        path for path in record.files if _is_implementation_file(path)
    ]
    supporting_only = _is_supporting_subject(record.subject, operation)
    if operation in REUSABLE_OPERATIONS:
        score += 0.20
        reasons.append("reusable_operation")
    if record.issue_numbers:
        score += 0.20
        reasons.append("issue_or_pr_anchor")
    if has_tests:
        score += 0.10
        reasons.append("test_evidence")
    if implementation_files:
        score += 0.20
        reasons.append("implementation_change")
    if 1 <= len(record.files) <= 12:
        score += 0.15
        reasons.append("bounded_change_surface")
    elif 13 <= len(record.files) <= 25:
        score += 0.07
        reasons.append("moderate_change_surface")
    if module_roles != ["core_runtime"]:
        score += 0.10
        reasons.append("recognized_harness_module")
    if len(record.subject.split()) >= 4 and not GENERIC_SUBJECT_RE.match(record.subject):
        score += 0.10
        reasons.append("descriptive_subject")
    if record.body.strip():
        score += 0.05
        reasons.append("commit_body_evidence")
    if docs_only:
        score -= 0.40
        reasons.append("docs_only_penalty")
    if not implementation_files and has_tests:
        score -= 0.20
        reasons.append("test_only_penalty")
    if supporting_only:
        score -= 0.35
        reasons.append("supporting_commit_penalty")
    if record.files and all(
        any(path.endswith(suffix) for suffix in LOCK_OR_GENERATED)
        for path in record.files
    ):
        score -= 0.25
        reasons.append("generated_or_lockfile_penalty")
    return max(0.0, min(1.0, score)), reasons


def build_episode_candidate(
    anchor_number: int,
    entries: list[tuple[CommitRecord, str, list[str]]],
) -> EpisodeCandidate:
    all_files: set[str] = set()
    operations: set[str] = set()
    roles: set[str] = set()
    subjects: list[str] = []
    implementation_commits = 0
    test_commits = 0
    descriptive_implementation = False

    for record, operation, module_roles in entries:
        all_files.update(record.files)
        operations.add(operation)
        roles.update(module_roles)
        subjects.append(record.subject)
        implementation_files = [
            path for path in record.files if _is_implementation_file(path)
        ]
        if implementation_files and not _is_supporting_subject(record.subject, operation):
            implementation_commits += 1
            if len(record.subject.split()) >= 4:
                descriptive_implementation = True
        if infer_validation(record.files)["has_test_evidence"]:
            test_commits += 1

    score = 0.25  # The reference exists in default-branch history.
    if implementation_commits:
        score += 0.25
    if test_commits:
        score += 0.15
    if roles and roles != {"core_runtime"}:
        score += 0.10
    if 1 <= len(entries) <= 12 and 1 <= len(all_files) <= 50:
        score += 0.15
    elif len(entries) > 20 or len(all_files) > 100:
        score -= 0.20
    if descriptive_implementation:
        score += 0.10
    if not implementation_commits:
        score -= 0.35

    return EpisodeCandidate(
        anchor_number=anchor_number,
        commit_count=len(entries),
        implementation_commit_count=implementation_commits,
        test_commit_count=test_commits,
        file_count=len(all_files),
        operations=sorted(operations),
        module_roles=sorted(roles),
        quality_score=max(0.0, min(1.0, score)),
        subjects=subjects[:12],
    )


def _is_documentation(path: str) -> bool:
    lowered = path.lower()
    return (
        lowered.endswith((".md", ".mdx", ".rst", ".txt"))
        or "/docs/" in f"/{lowered}"
        or lowered.startswith("docs/")
        or lowered.startswith("website/")
    )


def _is_test_path(path: str) -> bool:
    lowered = path.lower()
    return any(
        marker in f"/{lowered}"
        for marker in (
            "/test/",
            "/tests/",
            "/spec/",
            "/specs/",
            "/fixture/",
            "/fixtures/",
            ".test.",
            ".spec.",
        )
    )


def _is_implementation_file(path: str) -> bool:
    if _is_documentation(path) or _is_test_path(path):
        return False
    name = Path(path).name
    if name in LOCK_OR_GENERATED:
        return False
    return not name.lower().startswith(("changelog", "history"))


def _is_supporting_subject(subject: str, operation: str) -> bool:
    lowered = subject.lower().strip()
    return (
        operation in {"validation", "documentation", "maintenance", "ci_change"}
        or bool(GENERIC_SUBJECT_RE.match(lowered))
        or lowered.startswith(("test:", "test(", "docs:", "docs(", "ci:", "ci("))
    )
