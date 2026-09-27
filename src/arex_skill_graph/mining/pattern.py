from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from ..schema import Edge, Node, NodeType, RelationType, stable_id
from ..store import CatalogStore


@dataclass(frozen=True, slots=True)
class PatternStepSpec:
    key: str
    title: str
    summary: str
    roles: tuple[str, ...]
    predicate: str


@dataclass(frozen=True, slots=True)
class PatternSpec:
    key: str
    title: str
    summary: str
    domain_aliases: frozenset[str]
    steps: tuple[PatternStepSpec, ...]


@dataclass(slots=True)
class PatternBuildReport:
    specs_seen: int
    candidates_built: int
    skipped_insufficient_support: int
    patterns_steps_built: int
    workflow_support_edges: int
    workflow_step_realizations: int
    action_conformance_edges: int
    predicates_built: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# These are intentionally conservative, human-auditable candidate families.
# A family is eligible only when its reviewed Workflows occur in at least two
# repositories.  The aliases are semantic labels from the review manifest, not
# repository filenames or directory names.
DEFAULT_PATTERN_SPECS: tuple[PatternSpec, ...] = (
    PatternSpec(
        key="provider-contract-adaptation",
        title="Adapt a provider-specific interface to a stable agent contract",
        summary="Normalize provider capabilities, response fields, or errors while preserving provider evidence.",
        domain_aliases=frozenset({"model_provider_adapter"}),
        steps=(
            PatternStepSpec(
                "normalize-contract",
                "Normalize the provider contract",
                "Translate provider-specific inputs or responses into the agent's stable contract.",
                ("implement", "integrate", "repair"),
                "A provider adapter is needed when an external model API exposes incompatible fields, capabilities, or errors.",
            ),
            PatternStepSpec(
                "preserve-evidence",
                "Preserve provider evidence",
                "Retain raw provider metadata or error detail while exposing the normalized contract.",
                ("implement", "repair"),
                "Raw provider evidence must remain available for diagnosis without leaking provider-specific assumptions into callers.",
            ),
            PatternStepSpec(
                "verify-contract",
                "Verify the compatibility contract",
                "Exercise the adapter against provider-specific and provider-neutral regression cases.",
                ("validate",),
                "The normalized contract is usable only when provider-specific regressions are covered.",
            ),
        ),
    ),
    PatternSpec(
        key="context-compaction-safety",
        title="Preserve state and budget invariants during context compaction",
        summary="Coordinate compaction, retry, and concurrent-input behavior without losing state-machine safety.",
        domain_aliases=frozenset({"context_compaction", "context_compaction_and_concurrency"}),
        steps=(
            PatternStepSpec(
                "preserve-budget",
                "Preserve the compaction budget",
                "Reserve output or retry budget before selecting a compaction boundary.",
                ("implement", "integrate", "repair"),
                "Compaction must leave enough budget for the next response or retry.",
            ),
            PatternStepSpec(
                "gate-concurrent-input",
                "Gate input during state transition",
                "Reject or serialize new input while compaction or retry state is not stable.",
                ("implement", "repair"),
                "A session must not accept work against a partially compacted or retrying transcript.",
            ),
            PatternStepSpec(
                "verify-state-transition",
                "Verify the state transition",
                "Test the compaction/retry boundary and the resulting transcript or branch state.",
                ("validate",),
                "The state transition must be observable through a focused regression test.",
            ),
        ),
    ),
    PatternSpec(
        key="credential-boundary",
        title="Separate credential discovery, placement, and persistence",
        summary="Resolve credentials at a boundary, place secrets safely, and preserve unrelated configuration state.",
        domain_aliases=frozenset({"auth_credentials"}),
        steps=(
            PatternStepSpec(
                "discover-credentials",
                "Discover credentials through the supported boundary",
                "Resolve the requested credential source without conflating provider or profile configuration.",
                ("implement", "integrate", "repair"),
                "Credential lookup must respect the configured provider and profile boundary.",
            ),
            PatternStepSpec(
                "persist-safely",
                "Persist credentials without collateral loss",
                "Write secrets to the expected location while preserving unrelated settings.",
                ("implement", "repair"),
                "Persistence must not overwrite unrelated models, profiles, or configuration fields.",
            ),
            PatternStepSpec(
                "verify-auth-flow",
                "Verify the authentication flow",
                "Exercise success, missing-credential, and persistence cases.",
                ("validate",),
                "Authentication behavior is accepted only with focused credential and secret-placement coverage.",
            ),
        ),
    ),
    PatternSpec(
        key="tool-execution-boundary",
        title="Enforce a stable tool-execution boundary",
        summary="Normalize tool execution semantics at the boundary and fail safely when configuration is invalid.",
        domain_aliases=frozenset({"tool_execution"}),
        steps=(
            PatternStepSpec(
                "normalize-execution",
                "Normalize the execution request",
                "Collapse or route model-visible tool requests to the correct executor and scope.",
                ("implement", "integrate", "repair"),
                "The model-facing execution contract must map to one explicit runtime boundary.",
            ),
            PatternStepSpec(
                "fail-closed",
                "Fail closed at the configuration boundary",
                "Clamp, reject, or isolate invalid execution settings before launching work.",
                ("implement", "repair"),
                "Invalid execution configuration must not create unsafe or ambiguous runtime behavior.",
            ),
            PatternStepSpec(
                "verify-tool-contract",
                "Verify tool execution behavior",
                "Cover the model-visible contract and the runtime execution result.",
                ("validate",),
                "The executor boundary needs regression coverage for the affected mode or setting.",
            ),
        ),
    ),
    PatternSpec(
        key="extension-state-isolation",
        title="Isolate extension state across delegated execution",
        summary="Prevent plugin or extension work from corrupting parent state while preserving activation behavior.",
        domain_aliases=frozenset({"extension_plugin_loading"}),
        steps=(
            PatternStepSpec(
                "isolate-state",
                "Isolate delegated extension state",
                "Copy or scope mutable plugin state before delegated execution.",
                ("implement", "repair", "integrate"),
                "A delegated extension must not mutate the parent's active context accidentally.",
            ),
            PatternStepSpec(
                "bound-activation",
                "Bound extension activation",
                "Keep network, authentication, or loading behavior inside an explicit extension boundary.",
                ("implement", "repair"),
                "Extension activation must preserve fallback and timeout behavior at its boundary.",
            ),
            PatternStepSpec(
                "verify-isolation",
                "Verify extension isolation",
                "Test parent-state preservation and the delegated result.",
                ("validate",),
                "The parent context and delegated extension behavior require separate assertions.",
            ),
        ),
    ),
    PatternSpec(
        key="durable-session-recovery",
        title="Make session state durable and recoverable",
        summary="Persist session state incrementally, expose a read-friendly projection, and validate recovery behavior.",
        domain_aliases=frozenset({"session_persistence", "session_streaming", "history_persistence"}),
        steps=(
            PatternStepSpec(
                "persist-state",
                "Persist session state",
                "Write session or history state with an explicit ownership and durability invariant.",
                ("implement", "integrate", "repair"),
                "A recoverable session requires durable state boundaries rather than transient in-memory assumptions.",
            ),
            PatternStepSpec(
                "project-readable-state",
                "Project readable state",
                "Expose tail, listing, or replay data without loading the entire durable log.",
                ("implement", "integrate", "repair"),
                "Read paths should preserve recovery semantics while avoiding unnecessary full-history work.",
            ),
            PatternStepSpec(
                "verify-recovery",
                "Verify recovery and history invariants",
                "Test restart, replay, ownership, or history-size behavior.",
                ("validate",),
                "Durability is useful only when recovery and history invariants are regression-tested.",
            ),
        ),
    ),
    PatternSpec(
        key="skill-provenance-boundary",
        title="Preserve skill provenance at the prompt boundary",
        summary="Carry skill or system-prompt provenance from discovery into the model-facing request and verify consumption.",
        domain_aliases=frozenset({"skill_prompt_discovery"}),
        steps=(
            PatternStepSpec(
                "preserve-provenance",
                "Preserve discovered provenance",
                "Keep the source identity and metadata of a discovered skill or prompt fragment.",
                ("implement", "integrate", "repair"),
                "Prompt content must remain attributable to the discovered skill or source artifact.",
            ),
            PatternStepSpec(
                "handoff-at-boundary",
                "Handoff provenance at the model boundary",
                "Expose the composed prompt or metadata to the model-facing request without silently dropping it.",
                ("implement", "repair", "integrate"),
                "The runtime boundary must carry the normalized skill metadata into the request.",
            ),
            PatternStepSpec(
                "verify-prompt-contract",
                "Verify the prompt contract",
                "Assert that provenance is present at the consumer and remains stable across the request path.",
                ("validate",),
                "Prompt provenance requires a consumer-side regression assertion, not only an extraction test.",
            ),
        ),
    ),
)


class PatternCandidateBuilder:
    """Build conservative, provenance-preserving Pattern candidates.

    This builder deliberately uses reviewed domain labels and structural roles,
    not an LLM or repository filenames. It emits candidates only when at least
    two reviewed Workflows from at least two repositories support the family.
    """

    def __init__(
        self,
        specs: Iterable[PatternSpec] = DEFAULT_PATTERN_SPECS,
        *,
        min_workflows: int = 2,
        min_repositories: int = 2,
    ) -> None:
        self.specs = tuple(specs)
        self.min_workflows = min_workflows
        self.min_repositories = min_repositories

    def build_to_store(self, store: CatalogStore) -> PatternBuildReport:
        workflows = store.list_nodes(node_types=[NodeType.WORKFLOW])
        built = 0
        skipped = 0
        step_count = 0
        support_edges = 0
        realization_edges = 0
        conformance_edges = 0
        predicate_count = 0

        for spec in self.specs:
            supported = [
                workflow
                for workflow in workflows
                if str(workflow.facets.get("domain", "")) in spec.domain_aliases
            ]
            repositories = {workflow.repository for workflow in supported}
            if len(supported) < self.min_workflows or len(repositories) < self.min_repositories:
                skipped += 1
                continue

            pattern_id = stable_id("pattern", spec.key)
            predicate_nodes: list[Node] = []
            pattern_steps: list[Node] = []
            nodes: list[Node] = []
            edges: list[Edge] = []
            pattern = Node(
                id=pattern_id,
                node_type=NodeType.PATTERN,
                title=spec.title,
                summary=spec.summary,
                lifecycle="candidate",
                confidence=0.68,
                facets={
                    "pattern_key": spec.key,
                    "supporting_workflow_count": len(supported),
                    "supporting_repository_count": len(repositories),
                    "source_domains": sorted(spec.domain_aliases),
                },
                payload={
                    "candidate": True,
                    "supporting_workflow_ids": [workflow.id for workflow in supported],
                    "supporting_repositories": sorted(repositories),
                    "abstraction_basis": "reviewed domain aliases plus typed workflow-step roles",
                    "routing_terms": [spec.key, spec.title, *sorted(spec.domain_aliases)],
                    "rejected_mappings": [],
                },
                provenance={
                    "kind": "deterministic_pattern_candidate",
                    "builder": "pattern-candidate-v1",
                    "minimum_support": {
                        "workflows": self.min_workflows,
                        "repositories": self.min_repositories,
                    },
                },
            )
            nodes.append(pattern)

            for step_spec in spec.steps:
                step_id = stable_id("pattern_step", pattern_id, step_spec.key)
                predicate_id = stable_id("predicate", pattern_id, step_spec.key)
                predicate = Node(
                    id=predicate_id,
                    node_type=NodeType.PREDICATE,
                    title=f"When: {step_spec.key.replace('-', ' ')}",
                    summary=step_spec.predicate,
                    lifecycle="candidate",
                    confidence=0.60,
                    facets={"pattern_key": spec.key, "pattern_step": step_spec.key},
                    payload={"condition": step_spec.predicate, "routing_terms": [spec.key, step_spec.key, "predicate"]},
                    provenance={"kind": "pattern_step_predicate", "pattern_id": pattern_id},
                )
                pattern_step = Node(
                    id=step_id,
                    node_type=NodeType.PATTERN_STEP,
                    title=step_spec.title,
                    summary=step_spec.summary,
                    lifecycle="candidate",
                    confidence=0.64,
                    facets={
                        "pattern_key": spec.key,
                        "step_key": step_spec.key,
                        "abstract_roles": list(step_spec.roles),
                    },
                    payload={
                        "abstract_role": step_spec.key,
                        "predicate": step_spec.predicate,
                        "routing_terms": [spec.key, step_spec.key, *step_spec.roles],
                    },
                    provenance={
                        "kind": "deterministic_pattern_step_candidate",
                        "pattern_id": pattern_id,
                        "supporting_workflow_ids": [workflow.id for workflow in supported],
                        "source_workflow_step_ids": [],
                    },
                )
                predicate_nodes.append(predicate)
                pattern_steps.append(pattern_step)
                nodes.extend([predicate, pattern_step])
                edges.extend(
                    [
                        Edge.create(
                            pattern_id,
                            step_id,
                            RelationType.DECLARES_STEP,
                            confidence=0.68,
                            evidence_ids=tuple(workflow.id for workflow in supported),
                            provenance={"method": "pattern_spec"},
                        ),
                        Edge.create(
                            pattern_id,
                            predicate_id,
                            RelationType.APPLICABLE_WHEN,
                            confidence=0.60,
                            provenance={"method": "pattern_predicate"},
                        ),
                        Edge.create(
                            step_id,
                            predicate_id,
                            RelationType.APPLICABLE_WHEN,
                            confidence=0.60,
                            provenance={"method": "pattern_step_predicate"},
                        ),
                    ]
                )

            for workflow in supported:
                edges.extend(
                    [
                        Edge.create(
                            pattern_id,
                            workflow.id,
                            RelationType.SUPPORTED_BY,
                            confidence=0.68,
                            evidence_ids=(workflow.id,),
                            provenance={"method": "cross_repository_workflow_support"},
                        ),
                        Edge.create(
                            workflow.id,
                            pattern_id,
                            RelationType.INSTANTIATES,
                            confidence=0.65,
                            evidence_ids=(workflow.id,),
                            provenance={"method": "domain_alias_support"},
                        ),
                    ]
                )
                support_edges += 2
                workflow_steps = [
                    node
                    for _, node, direction in store.neighbors(
                        workflow.id,
                        relations=[RelationType.HAS_STEP],
                        direction="out",
                    )
                    if direction == "out" and node.node_type == NodeType.WORKFLOW_STEP
                ]
                for workflow_step in workflow_steps:
                    role = str(workflow_step.facets.get("role", ""))
                    step_spec = self._map_step(spec.steps, role)
                    if step_spec is None:
                        continue
                    pattern_step = next(
                        item for item in pattern_steps if item.facets.get("step_key") == step_spec.key
                    )
                    source_steps = list(pattern_step.provenance.get("source_workflow_step_ids", []))
                    source_steps.append(workflow_step.id)
                    pattern_step.provenance["source_workflow_step_ids"] = sorted(set(source_steps))
                    edges.append(
                        Edge.create(
                            workflow_step.id,
                            pattern_step.id,
                            RelationType.REALIZES,
                            confidence=0.55,
                            evidence_ids=(workflow_step.id,),
                            provenance={"method": "typed_role_mapping", "source_domain": workflow_step.facets.get("domain")},
                            condition={"workflow_domain": workflow_step.facets.get("domain"), "role": role},
                        )
                    )
                    realization_edges += 1
                    actions = [
                        node
                        for _, node, direction in store.neighbors(
                            workflow_step.id,
                            relations=[RelationType.EXECUTED_BY],
                            direction="out",
                        )
                        if direction == "out" and node.node_type == NodeType.ACTION
                    ]
                    for action in actions:
                        edges.append(
                            Edge.create(
                                action.id,
                                pattern_step.id,
                                RelationType.CONFORMS_TO,
                                confidence=0.50,
                                evidence_ids=(workflow_step.id,),
                                provenance={"method": "typed_role_mapping", "workflow_id": workflow.id},
                            )
                        )
                        conformance_edges += 1

            for pattern_step in pattern_steps:
                pattern_step.provenance["source_workflow_step_ids"] = sorted(
                    set(pattern_step.provenance.get("source_workflow_step_ids", []))
                )
            with store.transaction():
                store.upsert_nodes(nodes)
                for edge in edges:
                    store.upsert_edge(edge)
            built += 1
            step_count += len(pattern_steps)
            predicate_count += len(predicate_nodes)

        return PatternBuildReport(
            specs_seen=len(self.specs),
            candidates_built=built,
            skipped_insufficient_support=skipped,
            patterns_steps_built=step_count,
            workflow_support_edges=support_edges,
            workflow_step_realizations=realization_edges,
            action_conformance_edges=conformance_edges,
            predicates_built=predicate_count,
        )

    @staticmethod
    def _map_step(specs: tuple[PatternStepSpec, ...], role: str) -> PatternStepSpec | None:
        for step_spec in specs:
            if role in step_spec.roles:
                return step_spec
        return None
