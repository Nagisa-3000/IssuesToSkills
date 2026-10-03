"""Build public pre-repair queries without importing their answer into TaskContext."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .action_contracts import utc
from .git_tree_export import exact_git_tar
from .history_census import fingerprint
from .public_snapshot import extract_public_archive, initialize_public_base
from .task_context import EvidenceAnchor, TaskContext, assert_public


def pre_repair_problem(record, repair_available_at, base_committed_at):
    """Use only dated title/body versions; discussion/repair locators stay out."""
    entries = [
        e
        for e in record["evidence"]
        if e["kind"]
        in {
            "issue_title_as_of_cutoff",
            "issue_body_as_of_cutoff",
            "issue_body_recovered_as_of_cutoff",
        }
        and utc(e["available_at"]) < utc(repair_available_at)
    ]
    bodies = [
        e for e in entries if e["kind"] != "issue_title_as_of_cutoff" and e.get("text", "").strip()
    ]
    if not bodies:
        raise ValueError("no recoverable nonempty pre-repair public issue body")
    input_at = max([base_committed_at, *(e["available_at"] for e in entries)], key=utc)
    if utc(input_at) >= utc(repair_available_at):
        raise ValueError("public base/input chronology does not precede the repair")
    problem = "\n\n".join(e["text"] for e in entries if e.get("text", "").strip())
    assert_public(problem)
    return problem, input_at, tuple(e["id"] for e in entries)


def prepare_historical_query(record, verification, request, destination):
    identity = verification["identity"]
    if (
        verification.get("verified_resolution") is not True
        or verification.get("issue_relationship_verified") is not True
        or identity["issue_id"] != record["issue_id"]
        or identity.get("fix_id") != request["metadata"]["fix_id"]
    ):
        raise ValueError("query requires an issue-linked independent causal verification")
    git = ["git", "--git-dir", request["repository_path"]]
    base = identity["base_commit"]
    base_at = subprocess.check_output([*git, "show", "-s", "--format=%cI", base], text=True).strip()
    first_repair_at = request["metadata"].get("first_possible_public_repair_at")
    if not first_repair_at:
        raise ValueError("query repair-publication chronology has not been qualified")
    problem, input_at, refs = pre_repair_problem(record, first_repair_at, base_at)
    destination = Path(destination).resolve()
    if destination.exists():
        raise ValueError("historical public query already exists; choose a new version")
    destination.mkdir(parents=True)
    raw_commit = subprocess.check_output([*git, "cat-file", "commit", base])
    assert_public(raw_commit.decode("utf-8", errors="replace"))
    tree = subprocess.check_output([*git, "rev-parse", base + "^{tree}"], text=True).strip()
    extract_public_archive(exact_git_tar(git, base), destination)
    for path in destination.rglob("*"):
        if path.is_file():
            assert_public(path.read_bytes().decode("utf-8", errors="replace"))
    initialize_public_base(destination, base, raw_commit, tree)
    task = TaskContext(
        record["issue_id"],
        record["identity"]["repository"],
        base,
        str(destination),
        problem,
        input_at,
        (EvidenceAnchor("current:issue", "public_issue", problem, base, available_at=input_at),),
        environment=("Python 3.12; isolated historical Pyflakes development runtime",),
    )
    task.verify()
    audit = {
        "pre_repair_input_refs": refs,
        "input_available_at": input_at,
        "base_committed_at": base_at,
        "base_availability_basis": "Git committer timestamp of the public main-parent control; exact publication time is not separately observable",
        "base_time_publication_limit": True,
        "repair_available_at_used_only_for_exclusion": identity["repair_available_at"],
        "first_possible_public_repair_at_used_for_input_exclusion": first_repair_at,
        "first_possible_public_repair_time_basis": request["metadata"][
            "first_possible_public_repair_time_basis"
        ],
        "verification_sha256": fingerprint(verification),
        "only_base_git_commit_exported": True,
        "comments_and_repair_content_exported": False,
        "formal_SWE_query": False,
    }
    return task, audit
