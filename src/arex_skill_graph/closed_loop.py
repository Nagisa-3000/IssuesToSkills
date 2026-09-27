"""End-to-end retrieval, use, feedback, and lifecycle orchestration.

The admission pipeline intentionally stays separate from this runtime loop.  This
module connects the already admitted graph to a task: retrieval proposes
candidates, the governance LLM chooses only from those candidates, execution is
recorded, and feedback can revise or remove a serving skill.  Every mutation is
persisted before an optional HNSW cache is rebuilt.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .admission import SkillCandidateRetriever
from .hnsw import HNSWUnavailable
from .lifecycle import (
    FailureIncident,
    FailureKind,
    LifecycleManager,
    SkillLevel,
    SkillStatus,
    SkillRecord,
    UsageEvent,
    UsageResult,
)
from .llm_governance import LLMGovernanceAdapter
from .retrieval import SearchHit, SearchResponse, SkillRetriever
from .store import CatalogStore


_TERMINAL = frozenset(
    {
        SkillStatus.QUARANTINED,
        SkillStatus.DEPRECATED,
        SkillStatus.RETIRED,
        SkillStatus.MERGED,
        SkillStatus.SUPERSEDED,
    }
)


@dataclass(frozen=True, slots=True)
class RetrievalUse:
    """Auditable result of one retrieval + LLM applicability decision."""

    query: str
    task_id: str
    response: SearchResponse
    judge: Mapping[str, Any]
    selected_skill_id: str | None
    usage_event: UsageEvent | None = None


@dataclass(frozen=True, slots=True)
class FeedbackResult:
    """The persisted failure and the lifecycle action selected by governance."""

    incident: FailureIncident
    health: Any
    review: Mapping[str, Any]
    affected_skill_id: str
    revision_id: str | None = None
    resulting_status: SkillStatus | None = None


class ClosedLoopEngine:
    """Run the serving and feedback half of the Skill graph.

    SkillRetriever remains score-only candidate generation.  This class
    makes the semantic and operational gates explicit: a selected id must be a
    returned candidate, must still be active, and every failure review is
    persisted together with the graph projection and optional HNSW rebuild.
    """

    def __init__(
        self,
        manager: LifecycleManager,
        retriever: SkillRetriever,
        governance: LLMGovernanceAdapter,
        *,
        candidate_index: SkillCandidateRetriever | None = None,
        store: CatalogStore | None = None,
        hnsw_path: str | None = None,
        embedding_kind: str = "routing",
        model_version: str = "hash-v1",
    ) -> None:
        self.manager = manager
        self.retriever = retriever
        self.governance = governance
        self.store = store or retriever.store
        self.candidate_index = candidate_index or SkillCandidateRetriever(self.store)
        self.hnsw_path = hnsw_path
        self.embedding_kind = embedding_kind
        self.model_version = model_version
        self._event_counter = 0

    def use(
        self,
        query: str,
        *,
        task_id: str,
        result: UsageResult = UsageResult.SUCCESS,
        failure_kind: FailureKind | None = None,
        independent_context_id: str | None = None,
        validation_passed: bool | None = None,
        token_cost: int | None = None,
        notes: str = "",
        event_id: str | None = None,
        search_kwargs: Mapping[str, Any] | None = None,
    ) -> RetrievalUse:
        """Retrieve, have the LLM judge, and record one task outcome.

        Inactive nodes are excluded before both graph expansion and judging.
        A null judge selection is a valid no-use outcome and therefore does
        not create a UsageEvent for an arbitrary skill.
        """
        kwargs = dict(search_kwargs or {})
        kwargs.setdefault("include_inactive", False)
        response = self.retriever.search(query, **kwargs)
        judge = dict(self.governance.judge_retrieval_use(query, response.hits))
        selected = judge.get("selected_skill_id")
        selected_id = None if selected is None else str(selected)
        if selected_id is None:
            if bool(judge.get("applicable")):
                raise ValueError("retrieval judge marked a null selection as applicable")
            return RetrievalUse(query, task_id, response, judge, None, None)

        candidate_ids = {hit.node.id for hit in response.hits}
        if selected_id not in candidate_ids:
            raise ValueError(f"retrieval judge selected a non-returned candidate: {selected_id}")
        skill = self.manager.get(selected_id)
        if skill.status is not SkillStatus.ACTIVE:
            raise ValueError(f"inactive skill cannot be used: {selected_id} ({skill.status.value})")
        if result is UsageResult.FAILURE and failure_kind is None:
            raise ValueError("failure usage requires failure_kind")
        if result is not UsageResult.FAILURE and failure_kind is not None:
            raise ValueError("failure_kind is only valid for failure usage")

        self._event_counter += 1
        event = UsageEvent(
            event_id=event_id or f"usage:{task_id}:{selected_id}:{self._event_counter}",
            skill_id=selected_id,
            skill_version=skill.version,
            task_id=task_id,
            result=result,
            failure_kind=failure_kind,
            independent_context_id=independent_context_id,
            validation_passed=validation_passed,
            token_cost=token_cost,
            notes=notes,
        )
        self.manager.record_usage(event)
        self._persist_and_reindex()
        return RetrievalUse(query, task_id, response, judge, selected_id, event)

    def report_failure(
        self,
        use: RetrievalUse,
        *,
        incident_id: str | None = None,
        kind: FailureKind | None = None,
        independent_context_id: str | None = None,
        severity: str = "medium",
        evidence_ids: Sequence[str] = (),
        root_cause: str | None = None,
        correction_candidate_id: str | None = None,
        review: bool = True,
    ) -> FeedbackResult:
        """Record an incident, invoke failure governance, and apply its decision."""
        if use.selected_skill_id is None or use.usage_event is None:
            raise ValueError("cannot report a failure for a null retrieval selection")
        event = use.usage_event
        failure_kind = kind or event.failure_kind
        if failure_kind is None:
            raise ValueError("failure incident requires a failure kind")
        context_id = independent_context_id or event.independent_context_id
        if not context_id:
            raise ValueError("failure incident requires independent_context_id")
        if event.result is not UsageResult.FAILURE:
            raise ValueError("report_failure requires a failed UsageEvent")

        incident = FailureIncident(
            incident_id=incident_id or f"incident:{event.event_id}",
            skill_id=use.selected_skill_id,
            task_id=event.task_id,
            kind=failure_kind,
            independent_context_id=context_id,
            severity=severity,
            evidence_ids=tuple(str(item) for item in evidence_ids),
            root_cause=root_cause,
            correction_candidate_id=correction_candidate_id,
        )
        # The UsageEvent has already contributed this failure to lifecycle health.
        # Persist the incident for audit without counting the same runtime failure
        # a second time.
        health = self.manager.report_incident(incident, count_failure=False)
        skill = self.manager.get(incident.skill_id)
        review_payload = dict(
            self.governance.review_failure(skill, _incident_mapping(incident))
            if review
            else {
                "failure_class": failure_kind.value,
                "root_cause": root_cause or "review deferred",
                "recommended_status": skill.status.value,
                "revision": None,
            }
        )
        result = self._apply_review(skill, incident, review_payload)
        self._persist_and_reindex()
        return FeedbackResult(
            incident=incident,
            health=health,
            review=review_payload,
            affected_skill_id=incident.skill_id,
            revision_id=result[0],
            resulting_status=result[1],
        )

    def _apply_review(
        self,
        skill: SkillRecord,
        incident: FailureIncident,
        review: Mapping[str, Any],
    ) -> tuple[str | None, SkillStatus | None]:
        """Apply only explicit, schema-checked lifecycle actions."""
        revision_id: str | None = None
        resulting_status: SkillStatus | None = None
        revision = review.get("revision")
        if isinstance(revision, Mapping):
            payload = revision.get("payload")
            if payload is not None and not isinstance(payload, Mapping):
                raise ValueError("failure review revision.payload must be an object")
            revised = self.manager.create_revision(
                skill.skill_id,
                title=str(revision["title"]) if revision.get("title") else None,
                summary=str(revision["summary"]) if revision.get("summary") else None,
                payload=dict(payload or {}),
            )
            self._revalidate_parents(revised)
            activated, _ = self.manager.activate_revision(revised.skill_id)
            revision_id = activated.skill_id
            resulting_status = activated.status
            self.manager.relations.append(
                {
                    "source": skill.skill_id,
                    "relation": "revision",
                    "target": activated.skill_id,
                    "incident_id": incident.incident_id,
                    "review": dict(review),
                }
            )
            return revision_id, resulting_status

        recommended = str(review.get("recommended_status", skill.status.value)).strip().lower()
        aliases = {
            "quarantine": SkillStatus.QUARANTINED,
            "deprecate": SkillStatus.DEPRECATED,
            "retire": SkillStatus.RETIRED,
            "active": SkillStatus.ACTIVE,
            "suspect": SkillStatus.SUSPECT,
        }
        try:
            status = aliases.get(recommended, SkillStatus(recommended))
        except ValueError as exc:
            raise ValueError(f"failure review returned invalid lifecycle status: {recommended}") from exc
        rationale = str(review.get("root_cause") or review.get("rationale") or "LLM failure review")
        if status in {SkillStatus.QUARANTINED, SkillStatus.DEPRECATED}:
            self.manager.apply_llm_lifecycle_decision(
                skill.skill_id, status=status, rationale=rationale
            )
            self._detach_all_parents(skill)
            resulting_status = status
        elif status is SkillStatus.RETIRED:
            # Retirement is never an implicit detach.  A quarantined/deprecated
            # skill may retire only after its serving edges are explicitly gone.
            if skill.status not in {SkillStatus.QUARANTINED, SkillStatus.DEPRECATED, SkillStatus.MERGED, SkillStatus.SUPERSEDED}:
                raise ValueError("retirement requires a prior quarantine/deprecation/supersession decision")
            self.manager.retire(skill.skill_id)
            resulting_status = status
        else:
            self.manager.apply_llm_lifecycle_decision(
                skill.skill_id, status=status, rationale=rationale
            )
            resulting_status = status
        self.manager.relations.append(
            {
                "source": skill.skill_id,
                "relation": "semantic_review",
                "target": incident.incident_id,
                "review": dict(review),
            }
        )
        return revision_id, resulting_status

    def _detach_all_parents(self, skill: SkillRecord) -> None:
        for parent_id in tuple(skill.parent_ids):
            self.manager.detach_parent(skill.skill_id, parent_id)

    def _revalidate_parents(self, skill: SkillRecord) -> None:
        for parent_id in tuple(skill.parent_ids):
            parent = self.manager.skills.get(parent_id)
            expected = {
                SkillLevel.ATOMIC: SkillLevel.WORKFLOW,
                SkillLevel.WORKFLOW: SkillLevel.PATTERN,
            }.get(skill.level)
            if (
                parent is None
                or parent.status in _TERMINAL
                or expected is None
                or parent.level is not expected
            ):
                skill.parent_ids.discard(parent_id)
        skill.touch()

    def _persist_and_reindex(self) -> None:
        for skill in self.manager.skills.values():
            self.candidate_index.index(skill)
        self.store.persist_lifecycle_manager(self.manager)
        if self.hnsw_path:
            try:
                self.store.build_hnsw_index(
                    self.hnsw_path,
                    embedding_kind=self.embedding_kind,
                    model_version=self.model_version,
                )
            except HNSWUnavailable:
                raise


def _incident_mapping(incident: FailureIncident) -> dict[str, Any]:
    return {
        "incident_id": incident.incident_id,
        "skill_id": incident.skill_id,
        "task_id": incident.task_id,
        "kind": incident.kind.value,
        "independent_context_id": incident.independent_context_id,
        "severity": incident.severity,
        "evidence_ids": list(incident.evidence_ids),
        "root_cause": incident.root_cause,
        "correction_candidate_id": incident.correction_candidate_id,
        "occurred_at": incident.occurred_at,
    }
