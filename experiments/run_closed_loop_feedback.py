#!/usr/bin/env python3
"""Run a small, auditable closed-loop feedback experiment on a skill catalog.

The script intentionally does not modify the admission or extraction runners. It
restores ``SkillRecord`` objects from the admission registry in SQLite (or an
optional JSON snapshot), rebuilds the serving projection, and then executes:

    retrieval -> LLM applicability judge -> successful use
    retrieval -> LLM applicability judge -> failed use -> LLM failure review

The failure review is applied by ``ClosedLoopEngine``, which may create a
revision or quarantine/deprecate a skill. The script writes a redacted JSON
artifact containing usage, incident, lifecycle, graph, HNSW, retrieval, and
transport evidence. The API key is accepted only as a process argument and is
never placed in an output artifact.

An offline smoke run is available with ``--offline``; it uses a deterministic
local transport and never opens a network connection.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from arex_skill_graph.admission import SkillCandidateRetriever
from arex_skill_graph.closed_loop import (
    ClosedLoopEngine,
    FeedbackResult,
    RetrievalUse,
)
from arex_skill_graph.hnsw import HNSWUnavailable
from arex_skill_graph.lifecycle import (
    FailureKind,
    LifecycleManager,
    SkillLevel,
    SkillRecord,
    SkillStatus,
    UsageResult,
    UsageStats,
)
from arex_skill_graph.llm_governance import GovernanceContext, LLMGovernanceAdapter
from arex_skill_graph.llm_http import (
    OpenAICompatibleConfig,
    OpenAICompatibleTransport,
)
from arex_skill_graph.retrieval import SkillRetriever
from arex_skill_graph.schema import NodeType, RelationType
from arex_skill_graph.store import CatalogStore

DEFAULT_BASE_URL = "https://llm.rvnpu.cn/v1"
DEFAULT_MODEL = "openai/gpt-5.6-sol"
TERMINAL_STATUSES = {
    SkillStatus.QUARANTINED.value,
    SkillStatus.DEPRECATED.value,
    SkillStatus.RETIRED.value,
    SkillStatus.MERGED.value,
    SkillStatus.SUPERSEDED.value,
}


class OfflineTransport:
    """Deterministic transport used only by the explicit ``--offline`` smoke."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.transcripts: list[dict[str, Any]] = []

    def complete(
        self, *, system: str, user: str, response_schema: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        payload = json.loads(user)
        operation = str(payload.get("operation"))
        body = payload.get("payload", {})
        if operation == "judge_retrieval_use":
            candidates = body.get("candidates", [])
            selected = candidates[0].get("skill_id") if candidates else None
            result: Mapping[str, Any] = {
                "selected_skill_id": selected,
                "applicable": selected is not None,
                "confidence": 1.0 if selected is not None else 0.0,
                "rationale": "offline smoke selected the first retrieved candidate for a controlled test",
                "missing_preconditions": [],
            }
        elif operation == "failure_review":
            skill = body.get("skill", {})
            result = {
                "failure_class": "skill_logic_failure",
                "root_cause": "offline smoke injected a deterministic stale-policy failure",
                "recommended_status": "active",
                "revision": {
                    "title": f"{skill.get('title', 'skill')} (revised offline smoke)",
                    "summary": f"{skill.get('summary', 'revised behavior')} with a corrected failure guard",
                    "payload": {"offline_smoke_revision": True},
                },
            }
        else:
            raise ValueError(f"offline transport does not implement {operation!r}")
        self.calls.append({"operation": operation, "attempt": 1, "offline": True})
        self.transcripts.append({
            "system": system,
            "user": user,
            "response_schema": dict(response_schema),
            "response": dict(result),
            "offline": True,
        })
        return result


class ReviewPolicyTransport:
    """Delegate LLM calls and optionally guarantee a mutation for the pilot.

    ``fallback_action=quarantine`` is a local experiment policy, not a semantic
    classifier. It is used only when the provider returns an operationally
    non-mutating review (for example ``active`` with no revision), so the run
    still demonstrates a real persisted governance transition. The original
    provider review and the applied fallback are both recorded in the artifact.
    """

    def __init__(self, delegate: Any, fallback_action: str = "quarantine") -> None:
        self.delegate = delegate
        self.fallback_action = fallback_action
        self.fallbacks: list[dict[str, Any]] = []

    @property
    def calls(self) -> list[dict[str, Any]]:
        return self.delegate.calls

    @property
    def transcripts(self) -> list[dict[str, Any]]:
        return self.delegate.transcripts

    def complete(
        self, *, system: str, user: str, response_schema: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        result = dict(self.delegate.complete(
            system=system, user=user, response_schema=response_schema
        ))
        payload: Mapping[str, Any] = {}
        try:
            payload = json.loads(user)
        except (TypeError, json.JSONDecodeError):
            pass
        if payload.get("operation") != "failure_review" or self.fallback_action == "none":
            return result
        revision = result.get("revision")
        status = str(result.get("recommended_status", "")).strip().lower()
        # A direct retirement recommendation is not executable for the active
        # record in this one-incident run: the lifecycle API requires a prior
        # quarantine/deprecation and detached parents. Let the fallback policy
        # turn that recommendation into a safe one-step quarantine instead.
        mutates = isinstance(revision, Mapping) or status in {
            "quarantined", "quarantine", "deprecated", "deprecate"
        }
        if mutates:
            return result
        rationale = str(result.get("root_cause") or result.get("rationale") or "provider review")
        if self.fallback_action == "quarantine":
            result["recommended_status"] = "quarantined"
            result["root_cause"] = rationale + "; pilot fallback policy quarantined the failed skill"
            result["revision"] = None
        elif self.fallback_action == "revision":
            skill = payload.get("payload", {}).get("skill", {})
            result["recommended_status"] = "active"
            result["revision"] = {
                "title": f"{skill.get('title', 'skill')} (reviewed revision)",
                "summary": str(skill.get("summary", "")) + "; corrected after failure review",
                "payload": {"review_fallback": True},
            }
        else:
            raise ValueError(f"unsupported fallback action: {self.fallback_action}")
        self.fallbacks.append({
            "operation": "failure_review",
            "action": self.fallback_action,
            "provider_result": dict(self.delegate.transcripts[-1]["response"]),
        })
        return result


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _as_string_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes)):
        return (str(value),)
    return tuple(str(item) for item in value)


def _as_string_set(value: Any) -> set[str]:
    return set(_as_string_tuple(value))


def skill_record_from_json(value: Mapping[str, Any]) -> SkillRecord:
    """Restore a ``SkillRecord`` without re-running admission semantics."""
    usage_value = value.get("usage") or {}
    if not isinstance(usage_value, Mapping):
        usage_value = {}
    usage = UsageStats(
        attempts=int(usage_value.get("attempts", 0)),
        successes=int(usage_value.get("successes", 0)),
        failures=int(usage_value.get("failures", 0)),
        not_applicable=int(usage_value.get("not_applicable", 0)),
        independent_failure_contexts=_as_string_set(
            usage_value.get("independent_failure_contexts", ())
        ),
        failure_by_kind={
            str(key): int(item)
            for key, item in dict(usage_value.get("failure_by_kind", {})).items()
        },
        last_used_at=usage_value.get("last_used_at"),
        last_failure_at=usage_value.get("last_failure_at"),
    )
    return SkillRecord(
        skill_id=str(value["skill_id"]),
        level=SkillLevel(str(value["level"])),
        title=str(value.get("title", value["skill_id"])),
        summary=str(value.get("summary", "")),
        version=int(value.get("version", 1)),
        status=SkillStatus(str(value.get("status", SkillStatus.CANDIDATE.value))),
        canonical_id=(str(value["canonical_id"]) if value.get("canonical_id") is not None else None),
        aliases=_as_string_set(value.get("aliases")),
        supersedes=_as_string_set(value.get("supersedes")),
        merged_from=_as_string_set(value.get("merged_from")),
        parent_ids=_as_string_set(value.get("parent_ids")),
        evidence_ids=_as_string_set(value.get("evidence_ids")),
        preconditions=_as_string_tuple(value.get("preconditions")),
        exclusions=_as_string_tuple(value.get("exclusions")),
        failure_modes=_as_string_tuple(value.get("failure_modes")),
        payload=dict(value.get("payload") or {}),
        usage=usage,
        created_at=str(value.get("created_at") or _utc_now()),
        updated_at=str(value.get("updated_at") or _utc_now()),
        quarantine_reason=(
            str(value["quarantine_reason"])
            if value.get("quarantine_reason") is not None else None
        ),
    )


def _records_from_json(path: Path) -> list[SkillRecord]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        values = raw
    elif isinstance(raw, Mapping):
        values = raw.get("skills") or raw.get("records") or raw.get("skill_records")
        if values is None and "skill_id" in raw:
            values = [raw]
    else:
        values = None
    if not isinstance(values, list):
        raise TypeError(f"{path} does not contain a SkillRecord array")
    records: list[SkillRecord] = []
    for item in values:
        if isinstance(item, Mapping) and "skill" in item and isinstance(item["skill"], Mapping):
            item = item["skill"]
        if isinstance(item, Mapping) and "skill_id" in item:
            records.append(skill_record_from_json(item))
    if not records:
        raise ValueError(f"{path} contains no SkillRecord objects")
    return records


def _records_from_nodes(store: CatalogStore) -> list[SkillRecord]:
    """Best-effort graph-snapshot fallback for catalogs without skill_versions."""
    nodes = store.list_nodes(node_types=[NodeType.ATOMIC, NodeType.WORKFLOW, NodeType.PATTERN])
    records: list[SkillRecord] = []
    for node in nodes:
        facets = dict(node.facets)
        payload = dict(node.payload)
        parent_ids = {
            edge.source_id
            for edge, _, direction in store.neighbors(
                node.id, relations=(RelationType.CONTAINS,), direction="in"
            )
            if direction == "in"
        }
        records.append(SkillRecord(
            skill_id=node.id,
            level=SkillLevel(node.node_type.value),
            title=node.title,
            summary=node.summary,
            version=int(node.version) if str(node.version).isdigit() else 1,
            status=SkillStatus(node.lifecycle) if node.lifecycle else SkillStatus.CANDIDATE,
            canonical_id=payload.get("canonical_id"),
            parent_ids=parent_ids,
            preconditions=_as_string_tuple(facets.get("preconditions")),
            exclusions=_as_string_tuple(facets.get("exclusions")),
            failure_modes=_as_string_tuple(facets.get("failure_modes")),
            payload=payload,
        ))
    return records


def load_admitted_records(store: CatalogStore, snapshot: Path | None = None) -> tuple[list[SkillRecord], str]:
    """Load records from an explicit snapshot, SQLite admission registry, or graph."""
    if snapshot is not None:
        return _records_from_json(snapshot), f"json:{snapshot}"
    values = store.load_skill_json()
    if values:
        return [skill_record_from_json(item) for item in values], "sqlite:skill_versions"
    values = _records_from_nodes(store)
    if values:
        return values, "sqlite:nodes-graph-fallback"
    return [], "none"


def restore_manager(records: Iterable[SkillRecord]) -> LifecycleManager:
    manager = LifecycleManager()
    for record in records:
        if record.skill_id in manager.skills:
            raise ValueError(f"duplicate admitted skill id: {record.skill_id}")
        # Loading is a snapshot operation, so terminal historical versions are
        # retained rather than passed through add_candidate's admission gate.
        manager.skills[record.skill_id] = record
    return manager


def _node_types_for(level: SkillLevel) -> tuple[NodeType, ...]:
    return (NodeType(level.value),)


def _hit_json(hit: Any) -> dict[str, Any]:
    return {
        "skill_id": hit.node.id,
        "node_type": hit.node.node_type.value,
        "title": hit.node.title,
        "summary": hit.node.summary,
        "score": hit.score,
        "sources": dict(hit.sources),
        "trace": list(hit.trace),
        "lifecycle": hit.node.lifecycle,
    }


def _use_json(use: RetrievalUse | None) -> dict[str, Any] | None:
    if use is None:
        return None
    return {
        "query": use.query,
        "task_id": use.task_id,
        "selected_skill_id": use.selected_skill_id,
        "judge": dict(use.judge),
        "search": {
            "seed_count": use.response.seed_count,
            "expanded_count": use.response.expanded_count,
            "unresolved": list(use.response.unresolved),
            "hits": [_hit_json(hit) for hit in use.response.hits],
        },
        "usage_event": (
            {
                "event_id": use.usage_event.event_id,
                "skill_id": use.usage_event.skill_id,
                "skill_version": use.usage_event.skill_version,
                "task_id": use.usage_event.task_id,
                "result": use.usage_event.result.value,
                "failure_kind": (
                    use.usage_event.failure_kind.value
                    if use.usage_event.failure_kind else None
                ),
                "independent_context_id": use.usage_event.independent_context_id,
                "validation_passed": use.usage_event.validation_passed,
                "token_cost": use.usage_event.token_cost,
                "notes": use.usage_event.notes,
                "occurred_at": use.usage_event.occurred_at,
            }
            if use.usage_event else None
        ),
    }


def _feedback_json(feedback: FeedbackResult | None) -> dict[str, Any] | None:
    if feedback is None:
        return None
    return {
        "affected_skill_id": feedback.affected_skill_id,
        "revision_id": feedback.revision_id,
        "resulting_status": (
            feedback.resulting_status.value if feedback.resulting_status else None
        ),
        "incident": {
            "incident_id": feedback.incident.incident_id,
            "skill_id": feedback.incident.skill_id,
            "task_id": feedback.incident.task_id,
            "kind": feedback.incident.kind.value,
            "independent_context_id": feedback.incident.independent_context_id,
            "severity": feedback.incident.severity,
            "evidence_ids": list(feedback.incident.evidence_ids),
            "root_cause": feedback.incident.root_cause,
            "occurred_at": feedback.incident.occurred_at,
        },
        "health": asdict(feedback.health),
        "review": dict(feedback.review),
    }


def _query_rows(store: CatalogStore, sql: str, params: Sequence[Any] = ()) -> list[dict[str, Any]]:
    return [dict(row) for row in store.connection.execute(sql, params).fetchall()]


def _graph_evidence(store: CatalogStore) -> dict[str, Any]:
    return {
        "stats": store.stats(),
        "contains_edges": _query_rows(
            store,
            "SELECT id, source_id, target_id, relation, weight, confidence, evidence_json, provenance_json "
            "FROM edges WHERE relation = ? ORDER BY source_id, target_id",
            (RelationType.CONTAINS.value,),
        ),
        "lifecycle_relations": _query_rows(
            store,
            "SELECT skill_id, event_type, payload_json, occurred_at "
            "FROM skill_lifecycle_events ORDER BY event_id",
        ),
    }


def _runtime_evidence(store: CatalogStore) -> dict[str, Any]:
    return {
        "usage_events": _query_rows(
            store,
            "SELECT event_id, skill_id, occurred_at, payload_json "
            "FROM skill_usage_events ORDER BY occurred_at, event_id",
        ),
        "failure_incidents": _query_rows(
            store,
            "SELECT incident_id, skill_id, occurred_at, payload_json "
            "FROM skill_failure_incidents ORDER BY occurred_at, incident_id",
        ),
        "skill_versions": _query_rows(
            store,
            "SELECT skill_id, canonical_id, level, version, status, updated_at "
            "FROM skill_versions ORDER BY canonical_id, version, skill_id",
        ),
    }


def _build_hnsw(store: CatalogStore, path: Path) -> dict[str, Any]:
    try:
        store.build_hnsw_index(path, embedding_kind="routing", model_version="hash-v1")
    except (HNSWUnavailable, ValueError, OSError) as exc:
        return {
            "requested": True,
            "available": False,
            "path": str(path),
            "error_type": type(exc).__name__,
            "error": str(exc),
            "metadata": None,
        }
    metadata_path = path.with_name(path.name + ".meta.json")
    metadata = None
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    return {
        "requested": True,
        "available": True,
        "path": str(path),
        "metadata_path": str(metadata_path),
        "metadata": metadata,
        "size_bytes": path.stat().st_size if path.exists() else None,
    }


def _choose_seed(records: Sequence[SkillRecord], requested_id: str | None) -> SkillRecord:
    if requested_id:
        for record in records:
            if record.skill_id == requested_id:
                if record.status is not SkillStatus.ACTIVE:
                    raise ValueError(f"--skill-id must name an active record: {requested_id}")
                return record
        raise ValueError(f"skill id not found in admission records: {requested_id}")
    active = [record for record in records if record.status is SkillStatus.ACTIVE]
    if not active:
        raise ValueError("the catalog contains no active SkillRecord to exercise")
    return min(active, key=lambda item: (item.level.value, item.skill_id))


def run_experiment(args: argparse.Namespace) -> dict[str, Any]:
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ") + "-" + uuid.uuid4().hex[:8]
    hnsw_path = args.hnsw_path or output / "skill-catalog.hnsw"
    if not args.offline and not args.api_key:
        raise ValueError("--api-key is required unless --offline is used")

    if args.offline:
        transport_base: Any = OfflineTransport()
    else:
        transport_base = OpenAICompatibleTransport(OpenAICompatibleConfig(
            api_key=args.api_key,
            base_url=args.base_url,
            model=args.model,
            timeout_seconds=args.timeout_seconds,
            max_output_tokens=args.max_output_tokens,
            retries=args.retries,
        ))
    transport = ReviewPolicyTransport(transport_base, fallback_action=args.fallback_action)

    with CatalogStore(args.db) as store:
        store.initialize()
        records, record_source = load_admitted_records(store, args.snapshot)
        if not records:
            raise ValueError(
                "no admitted SkillRecord found; provide --snapshot or a catalog with "
                "skill_versions/nodes"
            )
        manager = restore_manager(records)
        seed = _choose_seed(records, args.skill_id)

        candidate_index = SkillCandidateRetriever(store)
        for record in manager.skills.values():
            candidate_index.index(record)
        # Persist the restored snapshot and current parent projection before
        # creating the HNSW cache, so the cache and graph evidence share a base.
        store.persist_lifecycle_manager(manager)
        hnsw = _build_hnsw(store, hnsw_path)
        vector_backend = "hnsw" if hnsw["available"] else "exact"
        engine_hnsw_path = str(hnsw_path) if hnsw["available"] else None

        governance = LLMGovernanceAdapter(
            transport,
            GovernanceContext(
                repository="admitted-skill-catalog",
                model=args.model if not args.offline else "offline-smoke",
                prompt_version="closed-loop-feedback-v1",
                code_context={
                    "experiment": "run_closed_loop_feedback",
                    "record_source": record_source,
                    "hnsw_backend": vector_backend,
                },
            ),
        )
        engine = ClosedLoopEngine(
            manager,
            SkillRetriever(store),
            governance,
            candidate_index=candidate_index,
            store=store,
            hnsw_path=engine_hnsw_path,
        )
        search_kwargs = {
            "node_types": _node_types_for(seed.level),
            "top_k": args.top_k,
            "seed_k": args.seed_k,
            "expand_hops": args.expand_hops,
            "query_mode": "solve",
            "vector_backend": vector_backend,
            "hnsw_path": engine_hnsw_path,
            "include_inactive": False,
        }
        query = args.query or f"{seed.title}: {seed.summary}"
        success_use = engine.use(
            query,
            task_id=f"{run_id}:success",
            result=UsageResult.SUCCESS,
            validation_passed=True,
            token_cost=args.success_token_cost,
            notes="controlled successful execution after LLM applicability judgment",
            event_id=f"usage:{run_id}:success",
            search_kwargs=search_kwargs,
        )
        if success_use.selected_skill_id is None:
            raise RuntimeError("LLM judge returned no applicable skill for successful use")

        failure_use = engine.use(
            query,
            task_id=f"{run_id}:failure",
            result=UsageResult.FAILURE,
            failure_kind=FailureKind.SKILL_LOGIC,
            independent_context_id=f"{run_id}:independent-context-1",
            validation_passed=False,
            token_cost=args.failure_token_cost,
            notes="controlled injected failure for lifecycle governance",
            event_id=f"usage:{run_id}:failure",
            search_kwargs=search_kwargs,
        )
        if failure_use.selected_skill_id is None:
            raise RuntimeError("LLM judge returned no applicable skill for failed use")
        feedback = engine.report_failure(
            failure_use,
            incident_id=f"incident:{run_id}:failure",
            kind=FailureKind.SKILL_LOGIC,
            independent_context_id=f"{run_id}:independent-context-1",
            severity="high",
            evidence_ids=("experiment:closed-loop-feedback", f"usage:{run_id}:failure"),
            root_cause="controlled failure injected by the experiment",
            review=True,
        )
        if (
            feedback.revision_id is None
            and feedback.resulting_status is not None
            and feedback.resulting_status.value not in TERMINAL_STATUSES
        ):
            raise RuntimeError(
                "failure review completed without revision/quarantine/deprecation/retirement; "
                "use --fallback-action quarantine or revision to make the pilot mutation explicit"
            )

        runtime = _runtime_evidence(store)
        graph = _graph_evidence(store)
        hnsw_after = _build_hnsw(store, hnsw_path)
        evidence = {
            "schema_version": "closed-loop-feedback-v1",
            "generated_at": _utc_now(),
            "configuration": {
                "run_id": run_id,
                "db": str(args.db),
                "output": str(output),
                "snapshot": str(args.snapshot) if args.snapshot else None,
                "record_source": record_source,
                "offline": bool(args.offline),
                "base_url": args.base_url,
                "model": args.model if not args.offline else "offline-smoke",
                "fallback_action": args.fallback_action,
                "skill_id": seed.skill_id,
                "query": query,
                "vector_backend": vector_backend,
            },
            "restored": {
                "records": len(records),
                "active": sum(item.status is SkillStatus.ACTIVE for item in records),
                "by_level": {
                    level.value: sum(item.level is level for item in records)
                    for level in SkillLevel
                },
            },
            "retrieval_and_use": {
                "success": _use_json(success_use),
                "failure": _use_json(failure_use),
            },
            "feedback": _feedback_json(feedback),
            "governance_policy_fallbacks": list(transport.fallbacks),
            "runtime_persistence": runtime,
            "graph": graph,
            "hnsw": {
                "before_feedback": hnsw,
                "after_feedback": hnsw_after,
                "rebuilds_requested": 5 if hnsw["available"] else 2,
            },
            "llm": {
                "calls": list(transport.calls),
                "transcripts": list(transport.transcripts),
            },
        }
        # Never serialize the OpenAI-compatible config object or its api_key.
        destination = output / "closed-loop-evidence.json"
        destination.write_text(
            json.dumps(evidence, ensure_ascii=False, indent=2, default=str) + "\n",
            encoding="utf-8",
        )
        return evidence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True, help="existing skill-catalog.sqlite")
    parser.add_argument("--output", type=Path, required=True, help="JSON evidence directory")
    parser.add_argument("--snapshot", type=Path, help="optional SkillRecord JSON snapshot")
    parser.add_argument("--api-key", help="OpenAI-compatible API key; never persisted")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--offline", action="store_true", help="run deterministic local smoke; no API call")
    parser.add_argument(
        "--fallback-action", choices=("none", "quarantine", "revision"), default="quarantine",
        help="explicit local policy if an LLM failure review has no mutation (default: quarantine)",
    )
    parser.add_argument("--hnsw-path", type=Path)
    parser.add_argument("--skill-id", help="active skill to exercise; otherwise choose deterministically")
    parser.add_argument("--query", help="retrieval query; otherwise derive it from the selected skill")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--seed-k", type=int, default=32)
    parser.add_argument("--expand-hops", type=int, default=2)
    parser.add_argument("--success-token-cost", type=int, default=0)
    parser.add_argument("--failure-token-cost", type=int, default=0)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--max-output-tokens", type=int, default=4000)
    parser.add_argument("--retries", type=int, default=2)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        evidence = run_experiment(args)
    except Exception as exc:  # noqa: BLE001
        print(f"closed-loop experiment failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "evidence": str(args.output / "closed-loop-evidence.json"),
        "restored": evidence["restored"],
        "success_skill": evidence["retrieval_and_use"]["success"]["selected_skill_id"],
        "failure_skill": evidence["retrieval_and_use"]["failure"]["selected_skill_id"],
        "revision_id": evidence["feedback"]["revision_id"],
        "resulting_status": evidence["feedback"]["resulting_status"],
        "hnsw_available": evidence["hnsw"]["after_feedback"]["available"],
        "llm_calls": len(evidence["llm"]["calls"]),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())




