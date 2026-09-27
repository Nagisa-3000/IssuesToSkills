"""Versioned lifecycle and feedback control for Pattern/Workflow/Atomic skills.

This module deliberately keeps semantic adjudication pluggable: an LLM may propose a
relation or a revision, but the lifecycle manager applies only schema- and policy-
valid transitions.  The manager is the in-process state machine; ``CatalogStore.persist_lifecycle_manager``
provides the durable SQLite snapshot and audit adapter.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Callable, Iterable, Mapping


class SkillLevel(StrEnum):
    ATOMIC = "atomic"
    WORKFLOW = "workflow"
    PATTERN = "pattern"


class SkillStatus(StrEnum):
    CANDIDATE = "candidate"
    ACTIVE = "active"
    SUSPECT = "suspect"
    QUARANTINED = "quarantined"
    DEPRECATED = "deprecated"
    RETIRED = "retired"
    MERGED = "merged"
    SUPERSEDED = "superseded"


class DedupDecision(StrEnum):
    EXACT_DUPLICATE = "exact_duplicate"
    MERGEABLE = "mergeable"
    SPECIALIZATION = "specialization"
    GENERALIZATION = "generalization"
    RELATED_BUT_DISTINCT = "related_but_distinct"
    CONFLICTING = "conflicting"
    NO_MATCH = "no_match"


class FailureKind(StrEnum):
    RETRIEVAL = "retrieval_failure"
    APPLICABILITY = "applicability_failure"
    PRECONDITION = "precondition_failure"
    COMPOSITION = "composition_failure"
    SKILL_LOGIC = "skill_logic_failure"
    STALE = "stale_skill"
    EXECUTION = "execution_failure"
    VALIDATION = "validation_failure"


class UsageResult(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    NOT_APPLICABLE = "not_applicable"
    ABORTED = "aborted"


@dataclass(slots=True)
class UsageStats:
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    not_applicable: int = 0
    independent_failure_contexts: set[str] = field(default_factory=set)
    failure_by_kind: dict[str, int] = field(default_factory=dict)
    last_used_at: str | None = None
    last_failure_at: str | None = None

    def record(
        self,
        result: UsageResult,
        *,
        failure_kind: FailureKind | None = None,
        context_id: str | None = None,
        occurred_at: str | None = None,
    ) -> None:
        now = occurred_at or utc_now()
        self.attempts += 1
        self.last_used_at = now
        if result is UsageResult.SUCCESS:
            self.successes += 1
        elif result is UsageResult.NOT_APPLICABLE:
            self.not_applicable += 1
        elif result is UsageResult.FAILURE:
            self.failures += 1
            self.last_failure_at = now
            if failure_kind is not None:
                key = failure_kind.value
                self.failure_by_kind[key] = self.failure_by_kind.get(key, 0) + 1
                if failure_kind in {FailureKind.SKILL_LOGIC, FailureKind.STALE} and context_id:
                    self.independent_failure_contexts.add(context_id)

    def to_json(self) -> dict[str, Any]:
        value = asdict(self)
        value["independent_failure_contexts"] = sorted(self.independent_failure_contexts)
        return value


@dataclass(slots=True)
class SkillRecord:
    skill_id: str
    level: SkillLevel
    title: str
    summary: str
    version: int = 1
    status: SkillStatus = SkillStatus.CANDIDATE
    canonical_id: str | None = None
    aliases: set[str] = field(default_factory=set)
    supersedes: set[str] = field(default_factory=set)
    merged_from: set[str] = field(default_factory=set)
    parent_ids: set[str] = field(default_factory=set)
    evidence_ids: set[str] = field(default_factory=set)
    preconditions: tuple[str, ...] = ()
    exclusions: tuple[str, ...] = ()
    failure_modes: tuple[str, ...] = ()
    payload: dict[str, Any] = field(default_factory=dict)
    usage: UsageStats = field(default_factory=UsageStats)
    created_at: str = field(default_factory=lambda: utc_now())
    updated_at: str = field(default_factory=lambda: utc_now())
    quarantine_reason: str | None = None

    def __post_init__(self) -> None:
        if self.canonical_id is None:
            self.canonical_id = self.skill_id
        if self.version < 1:
            raise ValueError("skill version must be positive")

    def touch(self, timestamp: str | None = None) -> None:
        self.updated_at = timestamp or utc_now()

    def to_json(self) -> dict[str, Any]:
        result = asdict(self)
        result["level"] = self.level.value
        result["status"] = self.status.value
        result["aliases"] = sorted(self.aliases)
        result["supersedes"] = sorted(self.supersedes)
        result["merged_from"] = sorted(self.merged_from)
        result["parent_ids"] = sorted(self.parent_ids)
        result["evidence_ids"] = sorted(self.evidence_ids)
        result["usage"] = self.usage.to_json()
        return result


@dataclass(frozen=True, slots=True)
class DedupProposal:
    candidate_id: str
    peer_id: str
    decision: DedupDecision
    confidence: float
    rationale: str
    reviewer: str = "llm"
    evidence_ids: tuple[str, ...] = ()
    merged_payload: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("dedup confidence must be in [0, 1]")
        if not self.rationale.strip():
            raise ValueError("dedup rationale cannot be empty")


@dataclass(frozen=True, slots=True)
class UsageEvent:
    event_id: str
    skill_id: str
    skill_version: int
    task_id: str
    result: UsageResult
    failure_kind: FailureKind | None = None
    independent_context_id: str | None = None
    validation_passed: bool | None = None
    token_cost: int | None = None
    notes: str = ""
    occurred_at: str = ""

    def __post_init__(self) -> None:
        if not self.occurred_at:
            object.__setattr__(self, "occurred_at", utc_now())
        if self.result is UsageResult.FAILURE and self.failure_kind is None:
            raise ValueError("failure events require failure_kind")
        if self.result is not UsageResult.FAILURE and self.failure_kind is not None:
            raise ValueError("failure_kind is only valid for failure events")


@dataclass(frozen=True, slots=True)
class FailureIncident:
    incident_id: str
    skill_id: str
    task_id: str
    kind: FailureKind
    independent_context_id: str
    severity: str = "medium"
    evidence_ids: tuple[str, ...] = ()
    root_cause: str | None = None
    correction_candidate_id: str | None = None
    occurred_at: str = ""

    def __post_init__(self) -> None:
        if self.severity not in {"low", "medium", "high", "critical"}:
            raise ValueError("invalid incident severity")
        if not self.occurred_at:
            object.__setattr__(self, "occurred_at", utc_now())


@dataclass(frozen=True, slots=True)
class LifecyclePolicy:
    suspect_after_independent_failures: int = 1
    quarantine_after_independent_failures: int = 3
    exact_duplicate_auto_alias: bool = True

    def __post_init__(self) -> None:
        if self.suspect_after_independent_failures < 1:
            raise ValueError("suspect threshold must be positive")
        if self.quarantine_after_independent_failures < self.suspect_after_independent_failures:
            raise ValueError("quarantine threshold must not be below suspect threshold")


@dataclass(frozen=True, slots=True)
class HealthDecision:
    skill_id: str
    current_status: SkillStatus
    independent_logic_failures: int
    review_required: bool
    reason: str
    parent_ids_needing_revalidation: tuple[str, ...] = ()


class LifecycleManager:
    """Conservative state machine for skill admission, revision and retirement.

    The manager never calls an LLM itself.  ``DedupProposal`` is the typed boundary
    through which an LLM adjudicator can submit a semantic decision.  This keeps
    LLM reasoning auditable and prevents a malformed response from mutating the
    canonical tree.
    """

    def __init__(self, policy: LifecyclePolicy | None = None) -> None:
        self.policy = policy or LifecyclePolicy()
        self.skills: dict[str, SkillRecord] = {}
        self.relations: list[dict[str, Any]] = []
        self.dedup_proposals: list[DedupProposal] = []
        self.usage_events: list[UsageEvent] = []
        self.incidents: list[FailureIncident] = []

    def add_candidate(self, skill: SkillRecord) -> SkillRecord:
        if skill.skill_id in self.skills:
            raise ValueError(f"skill already exists: {skill.skill_id}")
        if skill.status not in {SkillStatus.CANDIDATE, SkillStatus.ACTIVE}:
            raise ValueError("new skills must start as candidate or active")
        self.skills[skill.skill_id] = skill
        return skill

    def get(self, skill_id: str) -> SkillRecord:
        try:
            return self.skills[skill_id]
        except KeyError as exc:
            raise KeyError(f"unknown skill: {skill_id}") from exc

    def attach_parent(self, child_id: str, parent_id: str) -> None:
        child = self.get(child_id)
        parent = self.get(parent_id)
        expected = {SkillLevel.ATOMIC: SkillLevel.WORKFLOW, SkillLevel.WORKFLOW: SkillLevel.PATTERN}.get(child.level)
        if expected is None or parent.level is not expected:
            raise ValueError(f"invalid tree parent: {child.level.value} -> {parent.level.value}")
        child.parent_ids.add(parent_id)
        child.touch()
        self.relations.append({"source": parent_id, "relation": "contains", "target": child_id})

    def detach_parent(self, child_id: str, parent_id: str) -> None:
        """Detach one current tree edge while preserving its audit history."""
        child = self.get(child_id)
        self.get(parent_id)
        if parent_id not in child.parent_ids:
            return
        child.parent_ids.remove(parent_id)
        child.touch()
        # ``relations`` is append-only audit data. The current graph projection
        # is rebuilt from ``parent_ids`` by CatalogStore, so do not delete the
        # historical attach event here.

    def validate_proposal(self, proposal: DedupProposal) -> None:
        candidate = self.get(proposal.candidate_id)
        peer = self.get(proposal.peer_id)
        if candidate.level is not peer.level:
            raise ValueError("deduplication is only allowed within the same skill level")
        if candidate.skill_id == peer.skill_id:
            raise ValueError("a skill cannot be compared with itself")
        if candidate.status in {SkillStatus.RETIRED, SkillStatus.MERGED}:
            raise ValueError("cannot deduplicate a retired or merged candidate")

    def apply_dedup(self, proposal: DedupProposal) -> SkillRecord | None:
        """Apply only safe state changes; return a new merged version when created."""
        self.validate_proposal(proposal)
        candidate = self.get(proposal.candidate_id)
        peer = self.get(proposal.peer_id)
        self.dedup_proposals.append(proposal)
        self.relations.append(
            {
                "source": candidate.skill_id,
                "relation": proposal.decision.value,
                "target": peer.skill_id,
                "confidence": proposal.confidence,
                "rationale": proposal.rationale,
                "reviewer": proposal.reviewer,
                "evidence_ids": list(proposal.evidence_ids),
            }
        )
        if proposal.decision is DedupDecision.EXACT_DUPLICATE:
            if not self.policy.exact_duplicate_auto_alias:
                return None
            candidate.status = SkillStatus.MERGED
            candidate.canonical_id = peer.canonical_id or peer.skill_id
            candidate.merged_from.add(peer.skill_id)
            candidate.touch()
            peer.aliases.add(candidate.skill_id)
            peer.evidence_ids.update(candidate.evidence_ids)
            peer.touch()
            return peer
        if proposal.decision is DedupDecision.MERGEABLE:
            return self._create_merged_revision(candidate, peer, proposal)
        # The remaining decisions preserve both nodes and only create a typed
        # relation.  In particular, related text must not collapse distinct skills.
        return None

    def _create_merged_revision(
        self, candidate: SkillRecord, peer: SkillRecord, proposal: DedupProposal
    ) -> SkillRecord:
        canonical = peer.canonical_id or peer.skill_id
        old_versions = [skill.version for skill in self.skills.values() if skill.canonical_id == canonical]
        version = max(old_versions or [peer.version]) + 1
        merged_id = f"{canonical}@v{version}"
        payload = dict(peer.payload)
        payload.update(candidate.payload)
        if proposal.merged_payload:
            payload.update(dict(proposal.merged_payload))
        merged = SkillRecord(
            skill_id=merged_id,
            level=peer.level,
            title=peer.title,
            summary=peer.summary,
            version=version,
            status=SkillStatus.CANDIDATE,
            canonical_id=canonical,
            aliases=set(peer.aliases) | set(candidate.aliases),
            supersedes={peer.skill_id, candidate.skill_id},
            merged_from={peer.skill_id, candidate.skill_id},
            parent_ids=set(peer.parent_ids) | set(candidate.parent_ids),
            evidence_ids=set(peer.evidence_ids) | set(candidate.evidence_ids) | set(proposal.evidence_ids),
            preconditions=tuple(dict.fromkeys(peer.preconditions + candidate.preconditions)),
            exclusions=tuple(dict.fromkeys(peer.exclusions + candidate.exclusions)),
            failure_modes=tuple(dict.fromkeys(peer.failure_modes + candidate.failure_modes)),
            payload=payload,
        )
        self.skills[merged_id] = merged
        peer.status = SkillStatus.SUPERSEDED
        candidate.status = SkillStatus.SUPERSEDED
        peer.touch()
        candidate.touch()
        return merged

    def record_usage(self, event: UsageEvent) -> None:
        skill = self.get(event.skill_id)
        if event.skill_version != skill.version and skill.canonical_id == skill.skill_id:
            # Historical versions remain recordable, but callers must make the
            # version mismatch explicit rather than silently crediting the head.
            pass
        skill.usage.record(
            event.result,
            failure_kind=event.failure_kind,
            context_id=event.independent_context_id,
            occurred_at=event.occurred_at,
        )
        skill.touch(event.occurred_at)
        self.usage_events.append(event)

    def report_incident(
        self, incident: FailureIncident, *, count_failure: bool = True
    ) -> HealthDecision:
        skill = self.get(incident.skill_id)
        if not any(item.incident_id == incident.incident_id for item in self.incidents):
            self.incidents.append(incident)
        # Incident reporting can be used when no UsageEvent was emitted by an
        # external runtime. Callers that already recorded the matching UsageEvent
        # (for example ClosedLoopEngine) pass count_failure=False so one runtime
        # failure is not counted twice. Direct incident-only callers retain the
        # historical behavior and count the incident as a failure.
        incident_already_counted = any(
            item.incident_id != incident.incident_id
            and item.skill_id == incident.skill_id
            and item.kind is incident.kind
            and item.independent_context_id == incident.independent_context_id
            for item in self.incidents
        )
        if (
            count_failure
            and incident.kind in {FailureKind.SKILL_LOGIC, FailureKind.STALE}
            and not incident_already_counted
        ):
            skill.usage.failure_by_kind[incident.kind.value] = skill.usage.failure_by_kind.get(incident.kind.value, 0) + 1
            skill.usage.independent_failure_contexts.add(incident.independent_context_id)
            skill.usage.failures += 1
            skill.usage.last_failure_at = incident.occurred_at
            skill.touch(incident.occurred_at)
        return self.health(skill.skill_id)

    def health(self, skill_id: str) -> HealthDecision:
        """Return an observation that may trigger the LLM governance Skill.

        Thresholds are scheduling/cost controls only. They never decide that a
        Skill is wrong or quarantine it; the LLM must classify incidents and
        explicitly request a lifecycle transition.
        """
        skill = self.get(skill_id)
        count = len(skill.usage.independent_failure_contexts)
        review_required = count >= self.policy.suspect_after_independent_failures
        quarantine_review = count >= self.policy.quarantine_after_independent_failures
        if quarantine_review:
            reason = f"{count} independent logic/staleness failures trigger LLM quarantine review"
        elif review_required:
            reason = f"{count} independent logic/staleness failure(s) trigger LLM investigation"
        else:
            reason = "no LLM review trigger reached"
        return HealthDecision(
            skill_id=skill_id,
            current_status=skill.status,
            independent_logic_failures=count,
            review_required=review_required,
            reason=reason,
            parent_ids_needing_revalidation=tuple(sorted(skill.parent_ids)) if review_required else (),
        )

    def apply_llm_lifecycle_decision(
        self,
        skill_id: str,
        *,
        status: SkillStatus,
        rationale: str,
    ) -> None:
        """Apply an explicit semantic decision returned by the governance Skill."""
        if status not in {
            SkillStatus.ACTIVE,
            SkillStatus.SUSPECT,
            SkillStatus.QUARANTINED,
            SkillStatus.DEPRECATED,
            SkillStatus.RETIRED,
        }:
            raise ValueError("LLM lifecycle decision is not an operational status")
        if not rationale.strip():
            raise ValueError("LLM lifecycle rationale cannot be empty")
        skill = self.get(skill_id)
        if status is SkillStatus.RETIRED:
            eligible, reason = self.eligible_for_retirement(skill_id)
            if not eligible:
                raise ValueError(reason)
        skill.status = status
        skill.quarantine_reason = rationale if status is SkillStatus.QUARANTINED else None
        skill.touch()
    def create_revision(self, skill_id: str, *, title: str | None = None, summary: str | None = None, payload: Mapping[str, Any] | None = None) -> SkillRecord:
        old = self.get(skill_id)
        canonical = old.canonical_id or old.skill_id
        versions = [skill.version for skill in self.skills.values() if skill.canonical_id == canonical]
        version = max(versions or [old.version]) + 1
        revision = SkillRecord(
            skill_id=f"{canonical}@v{version}",
            level=old.level,
            title=title or old.title,
            summary=summary or old.summary,
            version=version,
            canonical_id=canonical,
            supersedes={old.skill_id},
            parent_ids=set(old.parent_ids),
            evidence_ids=set(old.evidence_ids),
            preconditions=old.preconditions,
            exclusions=old.exclusions,
            failure_modes=old.failure_modes,
            payload=dict(old.payload) | dict(payload or {}),
        )
        self.skills[revision.skill_id] = revision
        return revision

    def activate_revision(self, revision_id: str) -> tuple[SkillRecord, tuple[str, ...]]:
        revision = self.get(revision_id)
        if not revision.supersedes:
            raise ValueError("revision must supersede at least one skill")
        for old_id in revision.supersedes:
            old = self.get(old_id)
            old.status = SkillStatus.SUPERSEDED
            old.touch()
        revision.status = SkillStatus.ACTIVE
        revision.touch()
        return revision, tuple(sorted(revision.parent_ids))

    def quarantine(self, skill_id: str, reason: str) -> tuple[str, ...]:
        skill = self.get(skill_id)
        if not reason.strip():
            raise ValueError("quarantine reason cannot be empty")
        skill.status = SkillStatus.QUARANTINED
        skill.quarantine_reason = reason
        skill.touch()
        return tuple(sorted(skill.parent_ids))

    def eligible_for_retirement(self, skill_id: str) -> tuple[bool, str]:
        skill = self.get(skill_id)
        if skill.status not in {SkillStatus.QUARANTINED, SkillStatus.DEPRECATED, SkillStatus.MERGED, SkillStatus.SUPERSEDED}:
            return False, "only quarantined/deprecated/merged/superseded skills can retire"
        if skill.parent_ids and skill.status in {SkillStatus.QUARANTINED, SkillStatus.DEPRECATED}:
            return False, "detach or revalidate all parent workflows before retirement"
        return True, "safe to retire as a soft-deleted historical record"

    def retire(self, skill_id: str) -> None:
        eligible, reason = self.eligible_for_retirement(skill_id)
        if not eligible:
            raise ValueError(reason)
        skill = self.get(skill_id)
        skill.status = SkillStatus.RETIRED
        skill.touch()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_llm_dedup_result(
    result: Mapping[str, Any],
    *,
    candidate_id: str,
    peer_id: str,
    reviewer: str = "llm",
) -> DedupProposal:
    """Turn constrained LLM JSON into a typed proposal, without applying it."""
    try:
        decision = DedupDecision(str(result["decision"]))
        confidence = float(result["confidence"])
        rationale = str(result["rationale"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("invalid LLM dedup result: expected decision/confidence/rationale") from exc
    evidence_ids = tuple(str(item) for item in result.get("evidence_ids", ()))
    merged_payload = result.get("merged_payload")
    if merged_payload is not None and not isinstance(merged_payload, Mapping):
        raise ValueError("merged_payload must be an object")
    return DedupProposal(
        candidate_id=candidate_id,
        peer_id=peer_id,
        decision=decision,
        confidence=confidence,
        rationale=rationale,
        reviewer=reviewer,
        evidence_ids=evidence_ids,
        merged_payload=merged_payload,
    )





