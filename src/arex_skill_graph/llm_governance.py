from __future__ import annotations

"""LLM-facing governance boundary for semantic Skill decisions.

This module deliberately contains no keyword, similarity, or threshold-based
semantic classification. Retrieval supplies peers; the provider reads the
before/after code, call sites, tests, and evidence and returns constrained JSON.
"""
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol

from .episodes import ChangeEpisode
from .lifecycle import DedupDecision, DedupProposal, SkillLevel, SkillRecord, parse_llm_dedup_result


class LLMTransport(Protocol):
    def complete(self, *, system: str, user: str, response_schema: Mapping[str, Any]) -> Mapping[str, Any]: ...


@dataclass(frozen=True, slots=True)
class GovernanceContext:
    evidence: tuple[Mapping[str, Any], ...] = ()
    repository: str | None = None
    model: str = "unspecified"
    prompt_version: str = "skill-governance-v1"
    # Raw code context is deliberately passed through to the LLM. It is not
    # parsed by local rules and may contain before/after code, diff hunks,
    # call-sites, tests, issue/PR text, and runtime traces.
    code_context: Mapping[str, Any] = field(default_factory=dict)


class LLMGovernanceAdapter:
    """Provider-neutral adapter used by ``BottomUpSkillAdmission`` callbacks.

    The three episode methods are intentionally separate from the legacy
    ``extract`` method. This prevents a caller from accidentally deriving a
    Workflow by wrapping one Atomic, or a Pattern by wrapping one Workflow.
    """

    SYSTEM = (
        "You are the AREX Skill Lifecycle Governance Skill. Read the supplied "
        "before/after implementation, call sites, tests, and evidence. Semantic "
        "equivalence, applicability, extraction, abstraction, and failure cause "
        "are your judgment; never infer them from titles, filenames, keywords, "
        "or retrieval scores. Return only JSON matching the requested schema. "
        "Atomic means one reusable problem-solving operation. Workflow means "
        "the causal orchestration of an entire ChangeEpisode. Pattern means a "
        "cross-workflow abstraction, and must not be invented from one workflow."
    )

    EXTRACTION_SCHEMA: Mapping[str, Any] = {
        "type": "object",
        "required": ["skills"],
        "properties": {
            "skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["skill_id", "title", "summary"],
                    "additionalProperties": True,
                },
            }
        },
    }

    def __init__(self, transport: LLMTransport, context: GovernanceContext | None = None):
        self.transport = transport
        self.context = context or GovernanceContext()

    def judge(self, candidate: SkillRecord, peer: SkillRecord) -> DedupProposal:
        result = self.transport.complete(
            system=self.SYSTEM,
            user=self._prompt("deduplicate", {"candidate": candidate.to_json(), "peer": peer.to_json()}),
            response_schema={
                "type": "object", "required": ["decision", "confidence", "rationale"],
                "properties": {
                    "decision": {"enum": [item.value for item in DedupDecision]},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "rationale": {"type": "string"},
                    "evidence_ids": {"type": "array", "items": {"type": "string"}},
                    "merged_payload": {"type": ["object", "null"]},
                },
            },
        )
        return parse_llm_dedup_result(
            result,
            candidate_id=candidate.skill_id,
            peer_id=peer.skill_id,
            reviewer=self.context.model,
        )

    def judge_retrieval_use(self, query: str, hits: Sequence[Any]) -> Mapping[str, Any]:
        """Ask the LLM to select/apply one retrieved Skill for a task.

        Retrieval scores only form the candidate context. The provider must
        decide applicability and may return ``selected_skill_id = null`` when
        none of the candidates is safe to use.
        """
        applicability_keys = {
            "goal",
            "intent",
            "entry_state",
            "exit_state",
            "pre_state",
            "post_state",
            "steps",
            "validation",
            "invariants",
            "known_failure_modes",
            "counterexamples",
            "promotion_status",
            "supporting_repositories",
            "supporting_workflows",
            "unresolved_or_deferred",
            "when_to_use",
            "anti_goals",
            "not_applicable_when",
            "action_template",
            "decision_points",
            "ordering_constraints",
            "validation_ladder",
            "workflow_realizations",
            "exclusions",
            "missing_probes",
            "stop_conditions",
        }
        candidates = []
        for hit in hits:
            payload = hit.node.payload if isinstance(hit.node.payload, Mapping) else {}
            skill_context = {}
            if payload.get("skill_package"):
                from .skill_packages import hydrate_package

                skill_context = hydrate_package({**payload, "id": hit.node.id,
                                                 "lifecycle": hit.node.lifecycle})
            candidates.append(
                {
                    "skill_id": hit.node.id,
                    "node_type": hit.node.node_type.value,
                    "title": hit.node.title,
                    "summary": hit.node.summary,
                    "repository": hit.node.repository,
                    "lifecycle": hit.node.lifecycle,
                    "facets": dict(hit.node.facets),
                    "applicability_contract": {
                        key: payload[key] for key in applicability_keys if key in payload
                    },
                    "score": hit.score,
                    "sources": dict(hit.sources),
                    "trace": list(hit.trace),
                    **({"skill_package_context": skill_context} if skill_context else {}),
                }
            )
        result = self.transport.complete(
            system=self.SYSTEM,
            user=self._prompt(
                "judge_retrieval_use",
                {
                    "query": query,
                    "candidates": candidates,
                    "instruction": "Select exactly one applicable candidate or return null. Explain the causal evidence and state any missing precondition.",
                },
            ),
            response_schema={
                "type": "object",
                "required": ["selected_skill_id", "applicable", "confidence", "rationale"],
                "properties": {
                    "selected_skill_id": {"type": ["string", "null"]},
                    "applicable": {"type": "boolean"},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "rationale": {"type": "string"},
                    "missing_preconditions": {"type": "array", "items": {"type": "string"}},
                },
            },
        )
        selected = result.get("selected_skill_id")
        applicable = result.get("applicable")
        candidate_ids = {str(item.get("skill_id")) for item in candidates}
        if selected is not None and str(selected) not in candidate_ids:
            raise ValueError(f"retrieval judge selected a non-candidate skill: {selected}")
        if applicable is True and selected is None:
            raise ValueError("retrieval judge marked candidates applicable without selecting one")
        if applicable is False and selected is not None:
            raise ValueError("retrieval judge selected a skill while marking it inapplicable")
        if not isinstance(result.get("rationale"), str) or not result["rationale"].strip():
            raise ValueError("retrieval judge rationale cannot be empty")
        return dict(result)

    def extract(self, level: SkillLevel, source: SkillRecord | None = None) -> tuple[SkillRecord, ...]:
        """Legacy generic extraction entry point.

        Prefer the explicit episode methods below for production extraction.
        This method remains useful for callers that already own a structured
        source record and for compatibility with existing tests.
        """
        if source is None:
            source = SkillRecord(
                "source:code-reading",
                level,
                "Code evidence",
                "Code evidence supplied by governance context",
            )
        result = self.transport.complete(
            system=self.SYSTEM,
            user=self._prompt(
                "extract_" + level.value,
                {"source": source.to_json(), "required_level": level.value},
            ),
            response_schema=self.EXTRACTION_SCHEMA,
        )
        relation_key = "atomic_ids" if level is SkillLevel.WORKFLOW else "workflow_ids" if level is SkillLevel.PATTERN else None
        relation_ids = [source.skill_id] if relation_key else ()
        return self._records_from_result(
            result,
            level,
            source,
            default_relation_key=relation_key,
            default_relation_ids=relation_ids,
        )

    def extract_atomics_from_episode(self, episode: ChangeEpisode) -> tuple[SkillRecord, ...]:
        """Extract Atomic candidates from the complete code-change evidence."""
        episode_json = episode.to_json()
        result = self.transport.complete(
            system=self.SYSTEM,
            user=self._prompt(
                "extract_atomics_from_episode",
                {
                    "required_level": SkillLevel.ATOMIC.value,
                    "episode": episode_json,
                    "before": episode.before,
                    "after": episode.after,
                    "diff": episode.diff,
                    "call_sites": list(episode.call_sites),
                    "tests": list(episode.tests),
                },
            ),
            response_schema=self.EXTRACTION_SCHEMA,
        )
        source = self._episode_source(episode, SkillLevel.ATOMIC, "atomic")
        return self._records_from_result(result, SkillLevel.ATOMIC, source)

    def extract_workflows_from_episode(
        self,
        episode: ChangeEpisode,
        atomics: Sequence[SkillRecord],
    ) -> tuple[SkillRecord, ...]:
        """Extract Workflows once from one complete episode and all Atomics."""
        episode_json = episode.to_json()
        result = self.transport.complete(
            system=self.SYSTEM,
            user=self._prompt(
                "extract_workflows_from_episode",
                {
                    "required_level": SkillLevel.WORKFLOW.value,
                    "episode": episode_json,
                    "before": episode.before,
                    "after": episode.after,
                    "diff": episode.diff,
                    "call_sites": list(episode.call_sites),
                    "tests": list(episode.tests),
                    "atomic_candidates": [item.to_json() for item in atomics],
                    "workflow_extraction_rule": "Derive at least one Workflow when the episode contains a case_workflow goal and ordered case_actions supported by evidence; do not return an empty array merely because the evidence is summarized.",
                },
            ),
            response_schema=self.EXTRACTION_SCHEMA,
        )
        source = self._episode_source(episode, SkillLevel.WORKFLOW, "workflow")
        return self._records_from_result(
            result,
            SkillLevel.WORKFLOW,
            source,
            default_relation_key="atomic_ids",
            default_relation_ids=[item.skill_id for item in atomics],
        )

    def extract_patterns_from_workflows(
        self,
        workflows: Sequence[SkillRecord],
    ) -> tuple[SkillRecord, ...]:
        """Extract Patterns from a set of resolved Workflows."""
        result = self.transport.complete(
            system=self.SYSTEM,
            user=self._prompt(
                "extract_patterns_from_workflows",
                {
                    "required_level": SkillLevel.PATTERN.value,
                    "workflow_candidates": [item.to_json() for item in workflows],
                    "instruction": "Only return an abstraction supported by multiple workflows; put exactly those supporting workflow skill IDs in workflow_ids; return an empty skills array when none is justified.",
                },
            ),
            response_schema=self.EXTRACTION_SCHEMA,
        )
        source = SkillRecord(
            "source:workflow-set",
            SkillLevel.PATTERN,
            "Workflow evidence",
            "Resolved workflows supplied for cross-case abstraction",
            evidence_ids={evidence_id for item in workflows for evidence_id in item.evidence_ids},
        )
        records = self._records_from_result(
            result,
            SkillLevel.PATTERN,
            source,
            default_relation_key="workflow_ids",
            default_relation_ids=[item.skill_id for item in workflows],
        )
        workflow_by_id = {item.skill_id: item for item in workflows}
        values = result.get("skills", ())
        for record, value in zip(records, values):
            workflow_ids = tuple(dict.fromkeys(record.payload["workflow_ids"]))
            unknown = [item for item in workflow_ids if item not in workflow_by_id]
            if unknown:
                raise ValueError(
                    f"Pattern {record.skill_id} references unknown Workflows: {unknown}"
                )
            if len(workflow_ids) < 2:
                raise ValueError(
                    f"Pattern {record.skill_id} must be supported by at least two Workflows"
                )
            record.payload["workflow_ids"] = list(workflow_ids)
            if isinstance(value, Mapping) and "evidence_ids" not in value:
                record.evidence_ids = {
                    evidence_id
                    for workflow_id in workflow_ids
                    for evidence_id in workflow_by_id[workflow_id].evidence_ids
                }
        return records

    def review_failure(self, skill: SkillRecord, incident: Mapping[str, Any]) -> Mapping[str, Any]:
        return self.transport.complete(
            system=self.SYSTEM,
            user=self._prompt("failure_review", {"skill": skill.to_json(), "incident": dict(incident)}),
            response_schema={
                "type": "object", "required": ["failure_class", "root_cause", "recommended_status"],
                "properties": {
                    "failure_class": {"type": "string"},
                    "root_cause": {"type": "string"},
                    "recommended_status": {"type": "string"},
                    "revision": {"type": ["object", "null"]},
                },
            },
        )

    def _prompt(self, operation: str, payload: Mapping[str, Any]) -> str:
        return json.dumps(
            {
                "operation": operation,
                "prompt_version": self.context.prompt_version,
                "repository": self.context.repository,
                "evidence": list(self.context.evidence),
                "code_context": dict(self.context.code_context),
                "payload": payload,
            },
            ensure_ascii=False,
            sort_keys=True,
        )

    @staticmethod
    def _episode_source(episode: ChangeEpisode, level: SkillLevel, kind: str) -> SkillRecord:
        return SkillRecord(
            f"source:episode:{episode.episode_id}:{kind}",
            level,
            episode.title,
            f"Complete ChangeEpisode evidence for {kind} extraction",
            evidence_ids=set(episode.evidence_ids),
        )

    def _records_from_result(
        self,
        result: Mapping[str, Any],
        level: SkillLevel,
        source: SkillRecord,
        *,
        default_relation_key: str | None = None,
        default_relation_ids: Sequence[str] = (),
    ) -> tuple[SkillRecord, ...]:
        values = result.get("skills")
        if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
            raise TypeError("LLM extraction response must contain a skills array")
        return tuple(
            self._record(
                level,
                item,
                source,
                default_relation_key=default_relation_key,
                default_relation_ids=default_relation_ids,
            )
            for item in values
        )

    @staticmethod
    def _record(
        level: SkillLevel,
        value: Any,
        source: SkillRecord,
        *,
        default_relation_key: str | None = None,
        default_relation_ids: Sequence[str] = (),
    ) -> SkillRecord:
        if not isinstance(value, Mapping):
            raise TypeError("each extracted skill must be an object")
        skill_id = str(value.get("skill_id") or value.get("id") or "")
        title = str(value.get("title") or "")
        summary = str(value.get("summary") or "")
        if not skill_id or not title or not summary:
            raise ValueError("LLM skill extraction requires skill_id, title and summary")
        payload = dict(value.get("payload") or {})
        if default_relation_key and default_relation_key not in payload:
            aliases = {
                "atomic_ids": ("atomic_ids", "uses_atomic_skill_ids"),
                "workflow_ids": (
                    "workflow_ids",
                    "supported_by",
                    "supporting_workflow_ids",
                ),
            }.get(default_relation_key, (default_relation_key,))
            explicit = next((value[key] for key in aliases if key in value), None)
            payload[default_relation_key] = list(
                default_relation_ids if explicit is None else explicit
            )
        return SkillRecord(
            skill_id=skill_id,
            level=level,
            title=title,
            summary=summary,
            evidence_ids={str(x) for x in value.get("evidence_ids", source.evidence_ids)},
            preconditions=tuple(str(x) for x in value.get("preconditions", ())),
            exclusions=tuple(str(x) for x in value.get("exclusions", ())),
            failure_modes=tuple(str(x) for x in value.get("failure_modes", ())),
            payload=payload,
        )


