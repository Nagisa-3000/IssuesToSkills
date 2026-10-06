"""Sealed per-original-query routes for historical Ranker supervision.

Qualification artifacts remain evaluator-only. Missing inputs, runtimes, controls
or independent review stay in the registered denominator without utility labels.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .action_contracts import utc
from .historical_replay_controls import replay_task_identity
from .history_census import fingerprint
from .original_query_evaluator import load_original_replay_authority, original_query_evaluator
from .task_context import TaskContext

SCHEMA = "original-query-supervision-registry-v1"
BINDING_FIELDS = frozenset(
    {"verification_path", "controls_dir", "independent_review_path", "dependency_root"}
)


def _file_sha(path):
    path = Path(path)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def _private(path, roots):
    resolved = Path(path).resolve()
    if any(resolved.is_relative_to(root) for root in roots):
        raise ValueError("original supervision authority overlaps an actor-visible mount")
    return resolved


def _population(queries, register, training_cutoff, main_cutoff):
    if not utc(training_cutoff) < utc(main_cutoff):
        raise ValueError("original supervision cutoffs are not ordered")
    for key, cutoff in (("training_cutoff", training_cutoff), ("main_cutoff", main_cutoff)):
        if key in register and register[key] != cutoff:
            raise ValueError("registered original supervision cutoff changed")
    if register.get("queries_sha256") != fingerprint(queries):
        raise ValueError("registered original public query population changed")
    audits = register.get("audits", [])
    identifiers = [row["query_id"] for row in audits]
    if (
        not identifiers
        or len(set(identifiers)) != len(identifiers)
        or register.get("selected_registered_targets") != len(identifiers)
    ):
        raise ValueError("original registration omits or duplicates denominator targets")
    by_id = {row["task"]["task_id"]: row for row in queries}
    if len(by_id) != len(queries) or not set(by_id).issubset(identifiers):
        raise ValueError("original query population has duplicate or unregistered inputs")
    for audit in audits:
        raw = by_id.get(audit["query_id"])
        if raw is None:
            if audit.get("base_commit") or audit.get("status", "").startswith("registered_"):
                raise ValueError("registered available original input was omitted")
            continue
        task = TaskContext.from_dict(raw["task"])
        task.verify()
        if raw.get("exposed", False) or utc(task.input_available_at) >= utc(main_cutoff):
            raise ValueError("exposed/formal original query cannot supervise the Ranker")
        if any(
            key in audit and audit[key] != value
            for key, value in (
                ("base_commit", task.base_commit),
                ("input_available_at", task.input_available_at),
            )
        ):
            raise ValueError("original query does not match its registration identity")
    return by_id, audits


def _paths(binding):
    verification = binding.get("verification_path")
    controls = binding.get("controls_dir")
    review = binding.get("independent_review_path")
    paths = []
    if verification:
        verification = Path(verification)
        paths.extend((verification, verification.with_name("historical-diff.json")))
    if controls:
        paths.extend(
            Path(controls) / (name + ".json")
            for name in (
                "cohort",
                "completion",
                "original_base",
                "base_with_regression",
                "known_repair",
            )
        )
    if review:
        review = Path(review)
        paths.extend((review, review.with_name("input.json"), review.with_name("calls.json")))
    return tuple(paths)


def _entry(raw, audit, binding, actor_roots):
    if set(binding) - BINDING_FIELDS:
        raise ValueError("unknown original supervision binding field")
    binding = {
        key: str(Path(value).resolve()) if value is not None else None
        for key, value in binding.items()
    }
    paths = tuple(_private(path, actor_roots) for path in _paths(binding))
    witnesses = {str(path): _file_sha(path) for path in paths}
    runtime = binding.get("dependency_root")
    runtime_available = bool(runtime and Path(runtime).is_dir())
    row = {
        "query_id": audit["query_id"],
        "source_status": audit["status"],
        "query_record_sha256": fingerprint(raw) if raw is not None else None,
        "binding": binding,
        "authority_files_sha256": witnesses,
        "dependency_root_available": runtime_available,
        "expected_runtime_sha256": None,
        "readiness": "original_input_unavailable",
        "supervision_allowed": False,
        "failure_label_created": False,
    }
    if raw is None:
        return row
    task = TaskContext.from_dict(raw["task"])
    row["task_identity"] = replay_task_identity(task)
    if not runtime_available:
        row["readiness"] = "runtime_missing"
        return row
    if not binding.get("verification_path") or not binding.get("controls_dir"):
        row["readiness"] = "controls_missing"
        return row
    required = _paths(
        {key: value for key, value in binding.items() if key != "independent_review_path"}
    )
    if any(_file_sha(path) is None for path in required):
        row["readiness"] = "controls_missing"
        return row
    verification = json.loads(Path(binding["verification_path"]).read_bytes())
    identity = verification.get("identity", {})
    if identity.get("issue_id") != task.task_id or identity.get("fix_id") != raw["fix_id"]:
        raise ValueError("original query native fix identity mismatch")
    cohort = json.loads((Path(binding["controls_dir"]) / "cohort.json").read_bytes())
    if cohort.get("task_identity") != replay_task_identity(task):
        raise ValueError("original controls belong to a different query snapshot")
    completion = json.loads((Path(binding["controls_dir"]) / "completion.json").read_bytes())
    if completion.get("mechanical_controls_passed") is not True:
        row["readiness"] = "controls_unqualified"
        return row
    required_fields = (
        "native_verification_file_sha256",
        "historical_diff_file_sha256",
        "production_projection",
        "raw_known_repair_file_sha256",
        "controlled_known_repair_file_sha256",
        "known_repair_adapted",
        "historical_regression_assertions_unchanged",
    )
    missing_fields = [name for name in required_fields if name not in completion]
    if missing_fields:
        row["readiness"] = "controls_authority_incomplete"
        row["missing_control_authority_fields"] = missing_fields
        return row
    review = binding.get("independent_review_path")
    review_available = bool(
        review
        and all(_file_sha(p) is not None for p in _paths({"independent_review_path": review}))
    )
    authority = load_original_replay_authority(
        task,
        binding["verification_path"],
        binding["controls_dir"],
        review if review_available else None,
    )
    runtime_hash = authority.completion.get("runtime_sha256", "")
    if not re.fullmatch(r"[0-9a-f]{64}", runtime_hash):
        raise ValueError("original control runtime hash is missing or malformed")
    row["expected_runtime_sha256"] = runtime_hash
    row["readiness"] = (
        "ready"
        if authority.independently_reviewed
        else "independent_review_rejected"
        if review_available
        else "independent_review_pending"
    )
    row["supervision_allowed"] = authority.independently_reviewed
    return row


def build_original_supervision_registry(
    queries_path, query_register_path, bindings, *, training_cutoff, main_cutoff
):
    """Bind all registered targets using exact sources and explicit policy cutoffs."""
    queries_path, query_register_path = (
        Path(queries_path).resolve(),
        Path(query_register_path).resolve(),
    )
    queries, register = (
        json.loads(queries_path.read_bytes()),
        json.loads(query_register_path.read_bytes()),
    )
    by_id, audits = _population(queries, register, training_cutoff, main_cutoff)
    if not set(bindings).issubset(row["query_id"] for row in audits):
        raise ValueError("runtime/control binding names an unregistered original query")
    actor_roots = tuple(Path(raw["task"]["root"]).resolve() for raw in queries) + tuple(
        Path(binding["dependency_root"]).resolve()
        for binding in bindings.values()
        if binding.get("dependency_root")
    )
    _private(queries_path, actor_roots)
    _private(query_register_path, actor_roots)
    payload = {
        "schema": SCHEMA,
        "queries_sha256": fingerprint(queries),
        "queries_path": str(queries_path),
        "queries_file_sha256": _file_sha(queries_path),
        "query_register_path": str(query_register_path),
        "query_register_file_sha256": _file_sha(query_register_path),
        "training_cutoff": training_cutoff,
        "main_cutoff": main_cutoff,
        "denominator_query_ids": [row["query_id"] for row in audits],
        "entries": [
            _entry(by_id.get(a["query_id"]), a, bindings.get(a["query_id"], {}), actor_roots)
            for a in audits
        ],
        "formal_SWE_runs": 0,
        "real_ranker_training_completed": False,
        "unrun_queries_are_failure_labels": False,
    }
    payload["registry_sha256"] = fingerprint(payload)
    return payload


@dataclass(frozen=True)
class OriginalSupervisionRoute:
    dependency_root: Path
    required_runtime_sha256: str
    evaluator: object


class OriginalSupervisionRegistry:
    """Recompute authority before solving and again after solver termination."""

    def __init__(self, path, queries_path, query_register_path):
        self.path = Path(path).resolve()
        self.raw_bytes = self.path.read_bytes()
        self.payload = json.loads(self.raw_bytes)
        if self.payload.get("schema") != SCHEMA or self.payload.get(
            "registry_sha256"
        ) != fingerprint(
            {key: value for key, value in self.payload.items() if key != "registry_sha256"}
        ):
            raise ValueError("original supervision registry schema or digest mismatch")
        self.queries_path, self.query_register_path = Path(queries_path), Path(query_register_path)
        self.bindings = {row["query_id"]: row["binding"] for row in self.payload["entries"]}
        self.verify_unchanged()
        self.entries = {row["query_id"]: row for row in self.payload["entries"]}
        self.assert_private_destination(self.path)

    @property
    def sha256(self):
        return self.payload["registry_sha256"]

    def verify_unchanged(self):
        if self.path.read_bytes() != self.raw_bytes:
            raise ValueError("original supervision registry changed during execution")
        current = build_original_supervision_registry(
            self.queries_path,
            self.query_register_path,
            self.bindings,
            training_cutoff=self.payload["training_cutoff"],
            main_cutoff=self.payload["main_cutoff"],
        )
        if current != self.payload:
            raise ValueError("original supervision query, registration or authority changed")

    def assert_private_destination(self, path):
        queries = json.loads(self.queries_path.read_bytes())
        roots = tuple(Path(raw["task"]["root"]).resolve() for raw in queries) + tuple(
            Path(b["dependency_root"]).resolve()
            for b in self.bindings.values()
            if b.get("dependency_root")
        )
        _private(path, roots)

    def coverage(self):
        return [
            {
                key: row[key]
                for key in (
                    "query_id",
                    "source_status",
                    "readiness",
                    "supervision_allowed",
                    "failure_label_created",
                )
            }
            for row in self.payload["entries"]
        ]

    def entry_for(self, query):
        self.verify_unchanged()
        row = self.entries[query.task.task_id]
        raw = {
            "task": query.task.to_dict(),
            "bug_cluster_id": query.bug_cluster_id,
            "fix_id": query.fix_id,
            "aliases": list(query.aliases),
            "copied_from": list(query.copied_from),
            "exposed": query.exposed,
        }
        if row["query_record_sha256"] != fingerprint(raw):
            raise ValueError("original supervised query record changed")
        return row

    def route(self, query, *, sandbox_backend="namespace-copy"):
        row = self.entry_for(query)
        if not row["supervision_allowed"]:
            return None
        binding = row["binding"]
        evaluate = original_query_evaluator(
            binding["verification_path"],
            binding["dependency_root"],
            binding["controls_dir"],
            independent_review_path=binding["independent_review_path"],
            sandbox_backend=sandbox_backend,
        )

        def checked_evaluate(task, patch):
            self.entry_for(query)
            if replay_task_identity(task) != row["task_identity"]:
                raise ValueError("original supervision evaluator received a different task")
            return evaluate(task, patch)

        return OriginalSupervisionRoute(
            Path(binding["dependency_root"]), row["expected_runtime_sha256"], checked_evaluate
        )
