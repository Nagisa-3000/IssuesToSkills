from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
from typing import Any, Iterable

from ..schema import Edge, Node, NodeType, RelationType, stable_id
from ..store import CatalogStore
from .git import GitCommitMiner, classify_operation, infer_module_roles


@dataclass(slots=True)
class WorkflowBuildReport:
    labels_seen: int
    labels_skipped: int
    action_only_labels: int
    filtered_commits: int
    workflows_built: int
    workflow_steps_built: int
    actions_indexed: int
    commits_indexed: int
    validations_built: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ReviewedWorkflowBuilder:
    """Build deterministic Workflow baselines from human-reviewed episodes.

    The builder deliberately does not claim semantic abstraction. It preserves
    the manual keep/filter/split decisions, creates one step per retained
    commit-level Action, and records validation and ordering evidence so an
    offline semantic normalizer can later merge or rewrite the provisional
    steps without losing provenance.
    """

    def __init__(self, manifest_root: str | Path, labels_path: str | Path):
        self.manifest_root = Path(manifest_root).resolve()
        self.labels_path = Path(labels_path).resolve()

    def build_to_store(self, store: CatalogStore) -> WorkflowBuildReport:
        labels = self._read_labels()
        manifests = self._manifest_index()
        labels_skipped = 0
        action_only_labels = 0
        filtered_commits = 0
        workflow_ids: set[str] = set()
        workflow_step_ids: set[str] = set()
        action_ids: set[str] = set()
        commit_ids: set[str] = set()
        validation_ids: set[str] = set()

        for label in labels:
            repository = _required_text(label, "repository")
            number = int(label["number"])
            verdict = _required_text(label, "verdict")
            if verdict not in {
                "usable",
                "usable_after_filter",
                "split_required",
                "action_only",
                "defer_domain_specific",
                "reject",
            }:
                raise ValueError(
                    f"unsupported review verdict {verdict!r} for "
                    f"{repository} PR #{number}"
                )
            if verdict in {"defer_domain_specific", "reject"}:
                labels_skipped += 1
                continue
            manifest_entry = manifests.get((repository, number))
            if manifest_entry is None:
                raise KeyError(f"missing manifest for {repository} PR #{number}")
            manifest_path, episode = manifest_entry
            repo_path = Path(
                _required_text(episode.get("provenance", {}), "repository_path")
            )
            miner = GitCommitMiner(repo_path, repository)
            retained, removed = _filter_commits(episode.get("commits", []), label)
            filtered_commits += removed

            if verdict == "action_only":
                action_only_labels += 1
                for commit in retained:
                    commit_node, action_node, evidence_edge = miner.to_nodes(
                        miner.read_commit(_required_text(commit, "sha"))
                    )
                    with store.transaction():
                        store.upsert_node(commit_node)
                        store.upsert_node(action_node)
                        store.upsert_edge(evidence_edge)
                    commit_ids.add(commit_node.id)
                    action_ids.add(action_node.id)
                continue

            groups = _workflow_groups(retained, label)
            for group_name, group_commits in groups:
                if not group_commits:
                    raise ValueError(
                        f"empty workflow group {group_name!r} for {repository} PR #{number}"
                    )
                built = self._build_workflow(
                    store,
                    miner,
                    episode,
                    manifest_path,
                    label,
                    group_name,
                    group_commits,
                )
                workflow_ids.add(built[0])
                workflow_step_ids.update(built[1])
                action_ids.update(built[2])
                commit_ids.update(built[3])
                validation_ids.update(built[4])

        return WorkflowBuildReport(
            labels_seen=len(labels),
            labels_skipped=labels_skipped,
            action_only_labels=action_only_labels,
            filtered_commits=filtered_commits,
            workflows_built=len(workflow_ids),
            workflow_steps_built=len(workflow_step_ids),
            actions_indexed=len(action_ids),
            commits_indexed=len(commit_ids),
            validations_built=len(validation_ids),
        )

    def _build_workflow(
        self,
        store: CatalogStore,
        miner: GitCommitMiner,
        episode: dict[str, Any],
        manifest_path: Path,
        label: dict[str, Any],
        group_name: str,
        group_commits: list[dict[str, Any]],
    ) -> tuple[str, set[str], set[str], set[str], set[str]]:
        repository = _required_text(label, "repository")
        number = int(label["number"])
        domain = _required_text(label, "domain")
        verdict = _required_text(label, "verdict")
        merge_sha = _required_text(episode, "merge_sha")
        title = _required_text(episode, "title")
        workflow_title = title if group_name == "main" else group_name.replace("-", " ")
        workflow_id = stable_id(
            "workflow",
            repository,
            str(number),
            merge_sha,
            group_name,
        )
        confidence = {
            "usable": 0.90,
            "usable_after_filter": 0.82,
            "split_required": 0.78,
        }.get(verdict, 0.70)
        workflow = Node(
            id=workflow_id,
            node_type=NodeType.WORKFLOW,
            title=workflow_title,
            summary=(
                f"Reviewed merged-PR workflow in {domain}; "
                f"{len(group_commits)} retained commit actions"
            ),
            repository=repository,
            lifecycle="reviewed",
            confidence=confidence,
            facets={
                "domain": domain,
                "anchor_kind": "pull_request",
                "anchor_number": number,
                "merged_at": episode.get("merged_at"),
                "review_verdict": verdict,
                "cross_repository_potential": label.get(
                    "cross_repository_potential", "unknown"
                ),
            },
            payload={
                "anchor": {
                    "kind": "pull_request",
                    "repository": repository,
                    "number": number,
                    "merge_sha": merge_sha,
                },
                "goal": workflow_title,
                "entry_state": "requires offline semantic normalization",
                "exit_state": title,
                "decision_points": [],
                "repair_loops": [],
                "unresolved_or_deferred": [],
                "routing_terms": [domain, workflow_title, "reviewed workflow"],
                "review_notes": label.get("notes", ""),
            },
            provenance={
                "kind": "reviewed_local_merge_episode",
                "manifest_path": str(manifest_path),
                "labels_path": str(self.labels_path),
                "extractor": "reviewed-workflow-v1",
            },
        )

        nodes: list[Node] = [workflow]
        edges: list[Edge] = []
        step_ids: set[str] = set()
        action_ids: set[str] = set()
        commit_ids: set[str] = set()
        validation_ids: set[str] = set()
        ordered_actions: list[tuple[Node, str]] = []
        test_files: set[str] = set()

        for order, commit in enumerate(group_commits):
            record = miner.read_commit(_required_text(commit, "sha"))
            commit_node, action_node, evidence_edge = miner.to_nodes(record)
            role = _step_role(record.subject, classify_operation(record.subject), order)
            step_id = stable_id("workflow_step", workflow_id, action_node.id)
            step = Node(
                id=step_id,
                node_type=NodeType.WORKFLOW_STEP,
                title=action_node.title,
                summary=f"{role} step: {action_node.summary}",
                repository=repository,
                lifecycle="reviewed",
                confidence=min(confidence, action_node.confidence),
                facets={
                    "domain": domain,
                    "role": role,
                    "order": order,
                    "operation": action_node.facets.get("operation"),
                    "module_roles": action_node.facets.get("module_roles", []),
                },
                payload={
                    "goal": action_node.title,
                    "input_state": "requires offline semantic normalization",
                    "output_state": action_node.payload.get("post_state"),
                    "branch_condition": None,
                    "validation": action_node.payload.get("validation", {}),
                    "routing_terms": [
                        domain,
                        role,
                        *action_node.facets.get("module_roles", []),
                    ],
                },
                provenance={
                    "kind": "reviewed_commit_step_baseline",
                    "workflow_id": workflow_id,
                    "commit_sha": record.sha,
                    "extractor": "reviewed-workflow-v1",
                },
            )
            nodes.extend([commit_node, action_node, step])
            edges.extend(
                [
                    evidence_edge,
                    Edge.create(
                        workflow_id,
                        step_id,
                        RelationType.HAS_STEP,
                        confidence=confidence,
                        evidence_ids=(commit_node.id,),
                        provenance={"method": "reviewed_episode_order"},
                    ),
                    Edge.create(
                        step_id,
                        action_node.id,
                        RelationType.EXECUTED_BY,
                        confidence=confidence,
                        evidence_ids=(commit_node.id,),
                        provenance={"method": "reviewed_episode_order"},
                    ),
                    Edge.create(
                        step_id,
                        commit_node.id,
                        RelationType.EVIDENCED_BY,
                        confidence=1.0,
                        evidence_ids=(commit_node.id,),
                        provenance={"method": "git_commit"},
                    ),
                ]
            )
            if ordered_actions:
                previous = ordered_actions[-1][0]
                edges.append(
                    Edge.create(
                        previous.id,
                        action_node.id,
                        RelationType.PRECEDES,
                        confidence=0.70,
                        evidence_ids=(previous.provenance["commit_sha"], record.sha),
                        provenance={"method": "reviewed_commit_order"},
                    )
                )
            prior_implementation = next(
                (
                    prior
                    for prior, prior_role in reversed(ordered_actions)
                    if prior_role in {"implement", "repair", "integrate"}
                ),
                None,
            )
            if role == "validate" and prior_implementation is not None:
                edges.append(
                    Edge.create(
                        action_node.id,
                        prior_implementation.id,
                        RelationType.VALIDATES,
                        confidence=0.75,
                        evidence_ids=(commit_node.id,),
                        provenance={"method": "reviewed_commit_role"},
                    )
                )
            if role == "repair" and prior_implementation is not None:
                edges.append(
                    Edge.create(
                        action_node.id,
                        prior_implementation.id,
                        RelationType.REPAIRS,
                        confidence=0.70,
                        evidence_ids=(commit_node.id,),
                        provenance={"method": "reviewed_commit_role"},
                    )
                )
            ordered_actions.append((action_node, role))
            test_files.update(
                path
                for path in record.files
                if any(marker in path.lower() for marker in ("test", "spec", "fixture"))
            )
            step_ids.add(step_id)
            action_ids.add(action_node.id)
            commit_ids.add(commit_node.id)

        if test_files:
            validation_id = stable_id("validation", workflow_id, "changed-tests")
            validation = Node(
                id=validation_id,
                node_type=NodeType.VALIDATION,
                title=f"Regression evidence for {workflow_title}",
                summary=f"{len(test_files)} changed test or fixture files",
                repository=repository,
                lifecycle="reviewed",
                confidence=0.75,
                facets={"domain": domain, "validation_kind": "regression"},
                payload={
                    "test_files": sorted(test_files),
                    "command": None,
                    "expected_result": "tests pass",
                    "status": "candidate",
                    "routing_terms": [domain, "regression", "validation"],
                },
                provenance={
                    "kind": "changed_test_evidence",
                    "workflow_id": workflow_id,
                    "extractor": "reviewed-workflow-v1",
                },
            )
            nodes.append(validation)
            edges.append(
                Edge.create(
                    validation_id,
                    workflow_id,
                    RelationType.VERIFIES,
                    confidence=0.75,
                    evidence_ids=tuple(sorted(commit_ids)),
                    provenance={"method": "changed_test_paths"},
                )
            )
            validation_ids.add(validation_id)

        with store.transaction():
            store.upsert_nodes(nodes)
            for edge in edges:
                store.upsert_edge(edge)
        return workflow_id, step_ids, action_ids, commit_ids, validation_ids

    def _read_labels(self) -> list[dict[str, Any]]:
        payload = json.loads(self.labels_path.read_text(encoding="utf-8"))
        labels = payload.get("labels") if isinstance(payload, dict) else None
        if not isinstance(labels, list):
            raise ValueError("review labels must contain a labels array")
        return [label for label in labels if isinstance(label, dict)]

    def _manifest_index(self) -> dict[tuple[str, int], tuple[Path, dict[str, Any]]]:
        result: dict[tuple[str, int], tuple[Path, dict[str, Any]]] = {}
        for path in self.manifest_root.rglob("pr-*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                continue
            repository = payload.get("repository")
            number = payload.get("number")
            if not isinstance(repository, str) or not isinstance(number, int):
                continue
            key = (repository, number)
            if key in result:
                raise ValueError(f"duplicate manifest for {repository} PR #{number}")
            result[key] = (path, payload)
        return result


def _filter_commits(
    commits: Iterable[dict[str, Any]],
    label: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    patterns = [
        re.compile(str(pattern), re.IGNORECASE)
        for pattern in label.get("drop_subject_patterns", [])
    ]
    requested = label.get("retained_commit_shas")
    retained_sha_set: set[str] | None = None
    if requested is not None:
        if not isinstance(requested, list) or not all(
            isinstance(sha, str) and sha for sha in requested
        ):
            raise ValueError("retained_commit_shas must be a non-empty string list")
        retained_sha_set = set(requested)
    retained: list[dict[str, Any]] = []
    removed = 0
    seen_shas: set[str] = set()
    for commit in commits:
        sha = _required_text(commit, "sha")
        seen_shas.add(sha)
        subject = str(commit.get("subject") or "")
        parents = commit.get("parents", [])
        if (
            retained_sha_set is not None
            and sha not in retained_sha_set
        ) or len(parents) > 1 or any(pattern.search(subject) for pattern in patterns):
            removed += 1
            continue
        retained.append(commit)
    if retained_sha_set is not None:
        unknown = sorted(retained_sha_set - seen_shas)
        if unknown:
            raise ValueError(f"retained_commit_shas not present in episode: {unknown}")
    return retained, removed


def _workflow_groups(
    commits: list[dict[str, Any]],
    label: dict[str, Any],
) -> list[tuple[str, list[dict[str, Any]]]]:
    if label.get("verdict") != "split_required":
        return [("main", commits)]
    groups = label.get("workflow_groups")
    if not isinstance(groups, list) or not groups:
        raise ValueError("split_required label needs workflow_groups")
    assigned: set[str] = set()
    result: list[tuple[str, list[dict[str, Any]]]] = []
    for group in groups:
        if not isinstance(group, dict):
            continue
        name = _required_text(group, "name")
        patterns = [
            re.compile(str(pattern), re.IGNORECASE)
            for pattern in group.get("subject_patterns", [])
        ]
        selected = [
            commit
            for commit in commits
            if any(pattern.search(str(commit.get("subject") or "")) for pattern in patterns)
        ]
        assigned.update(_required_text(commit, "sha") for commit in selected)
        result.append((name, selected))
    unassigned = [
        _required_text(commit, "sha")
        for commit in commits
        if _required_text(commit, "sha") not in assigned
    ]
    if unassigned:
        raise ValueError(f"split workflow leaves unassigned commits: {unassigned}")
    return result


def _step_role(subject: str, operation: str, order: int) -> str:
    lowered = subject.lower()
    if operation == "validation" or lowered.startswith(("test", "ci:")):
        return "validate"
    if operation in {"documentation", "build_change", "ci_change", "maintenance"}:
        return "release"
    if order > 0 and (
        operation == "bug_fix" or lowered.startswith(("review:", "fix("))
    ):
        return "repair"
    if operation == "refactor":
        return "integrate"
    return "implement"


def _required_text(value: dict[str, Any], key: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result:
        raise ValueError(f"missing required string field {key!r}")
    return result
