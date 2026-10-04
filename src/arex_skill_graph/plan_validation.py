"""Current-task binding, dependency and verification checks for temporary plans."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from itertools import combinations

from .action_contracts import (
    ActionContract,
    CheckStatus,
    Dependency,
    Predicate,
    TemporalPolicy,
    digest,
    strict,
    strings,
)
from .pattern_contracts import PatternContract, load_native_package
from .task_context import Binding, TaskContext


@dataclass(frozen=True)
class InputLink:
    consumer: str
    input_port: str
    producer: str = ""
    output_port: str = ""
    current_port: str = ""
    evidence_refs: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["evidence_refs"] = strings(d.get("evidence_refs", []))
        return cls(**d)


@dataclass(frozen=True)
class ActionInstance:
    id: str
    action: ActionContract
    bindings: tuple[Binding, ...]
    role: str
    adaptation: str

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["action"] = ActionContract.from_dict(d["action"])
        d["bindings"] = tuple(Binding.from_dict(x) for x in d["bindings"])
        return cls(**d)


@dataclass(frozen=True)
class TaskWorkflowPlan:
    id: str
    task_id: str
    base_commit: str
    context_revision: int
    instances: tuple[ActionInstance, ...]
    dependencies: tuple[Dependency, ...]
    input_links: tuple[InputLink, ...]
    required_effects: tuple[Predicate, ...]
    invariants: tuple[Predicate, ...]
    parent_workflow_ids: tuple[str, ...]
    pattern: PatternContract | None = None
    changes: tuple[dict, ...] = ()
    stop_conditions: tuple[str, ...] = (
        "Stop and refresh context when code/evidence changes or an oracle fails.",
        "Before every modifying action, verify its actual inputs and preconditions.",
    )

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        for key, parser in [
            ("instances", ActionInstance),
            ("dependencies", Dependency),
            ("input_links", InputLink),
            ("required_effects", Predicate),
            ("invariants", Predicate),
        ]:
            d[key] = tuple(parser.from_dict(x) for x in d.get(key, []))
        d["pattern"] = PatternContract.from_dict(d["pattern"]) if d.get("pattern") else None
        for key in ("parent_workflow_ids", "stop_conditions"):
            if key in d:
                d[key] = strings(d[key])
        d["changes"] = tuple(d.get("changes", []))
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    @property
    def package_ids(self):
        ids = {i.action.package_id for i in self.instances}
        if self.pattern and self.pattern.package_id:
            ids.add(self.pattern.package_id)
        return ids


@dataclass(frozen=True)
class PlanCheck:
    code: str
    status: CheckStatus
    subject: str
    rationale: str
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class PlanValidationReport:
    plan_id: str
    checks: tuple[PlanCheck, ...]

    @property
    def status(self):
        if any(c.status == CheckStatus.FAIL for c in self.checks):
            return CheckStatus.FAIL
        if any(c.status == CheckStatus.UNKNOWN for c in self.checks):
            return CheckStatus.UNKNOWN
        return CheckStatus.PASS

    @property
    def mode(self):
        return {
            CheckStatus.PASS: "use",
            CheckStatus.UNKNOWN: "probe_only",
            CheckStatus.FAIL: "reject",
        }[self.status]

    def to_dict(self):
        return {
            "plan_id": self.plan_id,
            "status": self.status,
            "mode": self.mode,
            "checks": [asdict(c) for c in self.checks],
            "behavior_verified": False,
        }


@dataclass(frozen=True)
class ResourcePolicy:
    temporal: TemporalPolicy
    package_refs: tuple[Mapping, ...]
    max_root_packages: int = 2
    verify_head: bool = True

    def load(self):
        packages = tuple(load_native_package(r, self.temporal) for r in self.package_refs)
        if len({p.reference["skill_id"] for p in packages}) != len(packages):
            raise ValueError("duplicate resource roots")
        for attribute in ("actions", "workflows"):
            identities = [x.id for p in packages for x in getattr(p, attribute)]
            if len(identities) != len(set(identities)):
                raise ValueError("ambiguous native identities across resource roots")
        return packages


def topological(ids, dependencies):
    ids = set(ids)
    incoming = {i: set() for i in ids}
    for edge in dependencies:
        if edge.before not in ids or edge.after not in ids:
            raise ValueError("dangling plan dependency")
        incoming[edge.after].add(edge.before)
    result = []
    while incoming:
        ready = sorted(i for i, parents in incoming.items() if not parents)
        if not ready:
            raise ValueError("plan dependency cycle")
        result.extend(ready)
        for i in ready:
            del incoming[i]
        for parents in incoming.values():
            parents.difference_update(ready)
    return result


def ancestor_map(ids, dependencies):
    order = topological(ids, dependencies)
    parents = {i: set() for i in ids}
    for d in dependencies:
        parents[d.after].add(d.before)
    result = {}
    for i in order:
        result[i] = set(parents[i])
        for p in parents[i]:
            result[i].update(result[p])
    return order, result


def validate_task_plan(
    plan: TaskWorkflowPlan, task: TaskContext, resource_policy: ResourcePolicy
) -> PlanValidationReport:
    checks = []

    def add(code, status, subject, rationale, refs=()):
        checks.append(PlanCheck(code, CheckStatus(status), subject, rationale, tuple(refs)))

    def boolean(code, ok, subject, rationale, refs=()):
        add(code, CheckStatus.PASS if ok else CheckStatus.FAIL, subject, rationale, refs)

    boolean(
        "task_identity",
        plan.task_id == task.task_id
        and plan.base_commit == task.base_commit
        and plan.context_revision == task.revision,
        plan.id,
        "Plan belongs to this current context.",
    )
    try:
        task.verify(verify_head=resource_policy.verify_head)
        packages = resource_policy.load()
    except (ValueError, OSError, KeyError) as exc:
        add("current_or_package_evidence", CheckStatus.FAIL, plan.id, str(exc))
        return PlanValidationReport(plan.id, tuple(checks))
    actions = {a.id: a for p in packages for a in p.actions}
    historical_workflows = {w.id: w for p in packages for w in p.workflows}
    patterns = {p.pattern.id: p.pattern for p in packages if p.pattern}
    historical_evidence = {e for p in packages for e in p.evidence_ids}
    current_evidence = {e.id for e in task.anchors}
    ids = {i.id for i in plan.instances}
    boolean(
        "unique_instances",
        bool(ids) and len(ids) == len(plan.instances),
        plan.id,
        "Plan requires unique Action instances.",
    )
    boolean(
        "root_budget",
        len(plan.package_ids) <= resource_policy.max_root_packages,
        plan.id,
        "Independent Pattern and Action resources share the root-package cap.",
    )
    boolean(
        "parent_provenance",
        bool(plan.parent_workflow_ids)
        and set(plan.parent_workflow_ids).issubset(historical_workflows),
        plan.id,
        "Parent workflows are frozen native realizations.",
    )
    for parent_id in plan.parent_workflow_ids:
        if parent_id in historical_workflows:
            boolean(
                "parent_invariants",
                set(historical_workflows[parent_id].invariants).issubset(plan.invariants),
                parent_id,
                "A current binding cannot silently drop parent preserved behavior.",
            )
    if plan.pattern:
        boolean(
            "pattern_contract",
            plan.pattern.id in patterns
            and asdict(patterns[plan.pattern.id]) == asdict(plan.pattern),
            plan.pattern.id,
            "Pattern matches the authored native resource.",
        )
        semantic = task.semantic("pattern:" + plan.pattern.id)
        add(
            "pattern_relevance",
            semantic.status,
            plan.pattern.id,
            semantic.rationale,
            semantic.evidence_refs,
        )
        for condition in plan.pattern.applicability:
            add(
                "pattern_applicability",
                task.condition(condition),
                condition.key,
                "Pattern conditions use current observations.",
            )
        for exclusion in plan.pattern.exclusions:
            status = task.condition(exclusion)
            add(
                "pattern_exclusion",
                {
                    CheckStatus.PASS: CheckStatus.FAIL,
                    CheckStatus.FAIL: CheckStatus.PASS,
                    CheckStatus.UNKNOWN: CheckStatus.UNKNOWN,
                }[status],
                exclusion.key,
                "An unknown exclusion requires a probe.",
            )
        boolean(
            "pattern_goals",
            set(plan.pattern.required_effects).issubset(plan.required_effects),
            plan.id,
            "Pattern necessary effects cannot be dropped.",
        )
        boolean(
            "pattern_invariants",
            set(plan.pattern.invariants).issubset(plan.invariants),
            plan.id,
            "Pattern preserved behavior cannot be dropped.",
        )
    try:
        order, ancestors = ancestor_map(ids, plan.dependencies)
    except ValueError as exc:
        add("DAG", CheckStatus.FAIL, plan.id, str(exc))
        return PlanValidationReport(plan.id, tuple(checks))
    add("DAG", CheckStatus.PASS, plan.id, "Dependencies are closed and acyclic.")
    by_instance = {i.id: i for i in plan.instances}
    for d in plan.dependencies:
        boolean(
            "dependency_evidence",
            set(d.evidence_refs).issubset(current_evidence | historical_evidence),
            d.after,
            "Dependency has attributable evidence.",
            d.evidence_refs,
        )
    for link in plan.input_links:
        consumer = by_instance.get(link.consumer)
        boolean(
            "link_closed",
            consumer is not None and any(p.name == link.input_port for p in consumer.action.inputs),
            link.consumer,
            "Links refer to actual consumer ports.",
        )
        boolean(
            "link_evidence",
            bool(link.evidence_refs)
            and set(link.evidence_refs).issubset(current_evidence | historical_evidence),
            link.consumer,
            "Links carry closed provenance.",
        )
        boolean(
            "link_source",
            bool(link.producer) != bool(link.current_port),
            link.consumer,
            "Input has exactly one origin.",
        )
    initial = {(f.key, "evidence"): (f.value, f.evidence_refs) for f in task.facts}

    def state_for(before):
        state = dict(initial)
        for aid in order:
            if aid not in before:
                continue
            action = by_instance[aid].action
            for key in action.invalidates:
                for state_key in tuple(state):
                    if state_key[0] == key:
                        state.pop(state_key, None)
            for effect in action.effects:
                state[(effect.key, effect.evaluator)] = (effect.value, action.evidence_refs)
        return state

    for instance in plan.instances:
        a = instance.action
        boolean(
            "action_contract",
            a.id in actions and actions[a.id].to_dict() == a.to_dict(),
            instance.id,
            "Action matches its native file and package hash.",
            a.evidence_refs,
        )
        boolean(
            "instance_role",
            instance.role == a.semantic_role,
            instance.id,
            "Current instance keeps its native semantic operation role.",
        )
        parent_actions = {
            x.id
            for pid in plan.parent_workflow_ids
            if pid in historical_workflows
            for x in historical_workflows[pid].actions
        }
        boolean(
            "action_lineage",
            a.id in parent_actions,
            instance.id,
            "Every selected/Bridge action has a parent historical realization.",
        )
        for key in ("action:" + a.id, "owner:" + a.owner_role):
            decision = task.semantic(key)
            add(
                "current_semantics",
                decision.status,
                key,
                decision.rationale,
                decision.evidence_refs,
            )
        binding = next((b for b in instance.bindings if b.role == a.owner_role), None)
        if binding is None:
            add(
                "current_binding",
                CheckStatus.UNKNOWN,
                instance.id,
                "Locate and check the current semantic owner.",
            )
        else:
            boolean(
                "current_binding",
                binding in task.bindings,
                instance.id,
                "Binding is a current evidence-backed object/interface.",
                binding.evidence_refs,
            )
            languages = {p.language.casefold() for p in (*a.inputs, *a.outputs)} - {"agnostic"}
            boolean(
                "binding_language",
                not languages or languages == {binding.language.casefold()},
                instance.id,
                "Concrete port objects must use the currently bound implementation language.",
                binding.evidence_refs,
            )
        state = state_for(ancestors[instance.id])
        for pre in a.preconditions:
            observed = state.get((pre.key, pre.evaluator))
            status = (
                task.condition(pre)
                if observed is None
                else (CheckStatus.PASS if observed[0] == pre.value else CheckStatus.FAIL)
            )
            add(
                "precondition",
                status,
                instance.id + ":" + pre.key,
                "Prerequisite must be observed or produced by a verified predecessor; expected effects remain conditional.",
                observed[1] if observed else (),
            )
        for exclusion in a.exclusions:
            status = task.condition(exclusion)
            add(
                "action_exclusion",
                {
                    CheckStatus.PASS: CheckStatus.FAIL,
                    CheckStatus.FAIL: CheckStatus.PASS,
                    CheckStatus.UNKNOWN: CheckStatus.UNKNOWN,
                }[status],
                a.id,
                "Exclusion must be checked against current context.",
            )
        for port in a.inputs:
            links = [
                item
                for item in plan.input_links
                if item.consumer == instance.id and item.input_port == port.name
            ]
            if not links and port.optional:
                continue
            if len(links) != 1:
                add(
                    "port",
                    CheckStatus.UNKNOWN if not links else CheckStatus.FAIL,
                    instance.id,
                    "Input needs one explicit source.",
                )
                continue
            link = links[0]
            if link.producer:
                producer = by_instance.get(link.producer)
                output = (
                    next((p for p in producer.action.outputs if p.name == link.output_port), None)
                    if producer
                    else None
                )
                boolean(
                    "port_dependency",
                    link.producer in ancestors[instance.id],
                    instance.id,
                    "Producer must precede consumer; lexical ordering is insufficient.",
                )
                boolean(
                    "port_contract",
                    output is not None and output.compatible(port),
                    instance.id,
                    "Semantic role, artifact, language, scope, phase and state must match.",
                )
                proof = task.semantic(
                    f"connect:{producer.action.id if producer else link.producer}:{a.id}:{port.name}"
                )
                add(
                    "port_semantics",
                    proof.status,
                    instance.id,
                    proof.rationale,
                    proof.evidence_refs,
                )
            elif link.current_port:
                value = next(
                    (v for v in task.port_values if v.port.name == link.current_port), None
                )
                boolean(
                    "port_current_value",
                    value is not None and value.port.compatible(port),
                    instance.id,
                    "Current input is an observed compatible value.",
                    value.evidence_refs if value else (),
                )
                proof = task.semantic(f"current-connect:{link.current_port}:{a.id}:{port.name}")
                add(
                    "port_current_semantics",
                    proof.status,
                    instance.id,
                    proof.rationale,
                    proof.evidence_refs,
                )
            else:
                add("port", CheckStatus.FAIL, instance.id, "Input connection is unspecified.")
        boolean("oracle", bool(a.oracle), instance.id, "Each action has a focused public oracle.")
        for oracle in a.oracle:
            bound_oracle = next(
                (
                    o
                    for o in task.oracles
                    if o.action_id == a.id and o.source_oracle_id == oracle.id
                ),
                None,
            )
            add(
                "current_oracle_binding",
                CheckStatus.PASS if bound_oracle else CheckStatus.UNKNOWN,
                a.id + ":" + oracle.id,
                "Historical commands must be adapted to public current inputs.",
                bound_oracle.evidence_refs if bound_oracle else (),
            )
            proof = task.semantic(f"oracle:{a.id}:{oracle.id}")
            add(
                "current_oracle_semantics",
                proof.status,
                a.id + ":" + oracle.id,
                proof.rationale,
                proof.evidence_refs,
            )
        for invariant in (*plan.invariants, *a.preserves):
            status = task.condition(invariant)
            add(
                "invariant_entry",
                status,
                invariant.key,
                "Preserved behavior must have current evidence.",
            )
            for effect in a.effects:
                if (
                    effect.key == invariant.key
                    and effect.evaluator == invariant.evaluator
                    and effect.value != invariant.value
                ):
                    add(
                        "invariant_violation",
                        CheckStatus.FAIL,
                        a.id,
                        "Expected effect violates preserved behavior.",
                    )
            if invariant.key in a.invalidates:
                add(
                    "invariant_invalidation",
                    CheckStatus.FAIL,
                    a.id,
                    "Action invalidates a required invariant.",
                )
    bound_by_role = {b.role: b for b in task.bindings}
    anchors = {a.id: a for a in task.anchors}

    def resources(instance, writes=False):
        action = instance.action
        tokens = action.write_set if writes else action.read_set
        if not tokens and (not writes or action.kind in {"edit", "bridge", "cleanup"}):
            tokens = (action.owner_role,)
        result = set()
        for token in tokens:
            binding = bound_by_role.get(token.removeprefix("role:"))
            result.add("current-file:" + anchors[binding.anchor_id].path if binding else token)
        return result

    for left, right in combinations(plan.instances, 2):
        overlap = (resources(left, True) & (resources(right) | resources(right, True))) | (
            resources(right, True) & resources(left)
        )
        fact_overlap = set(left.action.invalidates) & {p.key for p in right.action.preconditions}
        fact_overlap |= set(right.action.invalidates) & {p.key for p in left.action.preconditions}
        fact_overlap |= {p.key for p in left.action.effects} & {
            p.key for p in right.action.preconditions
        }
        fact_overlap |= {p.key for p in right.action.effects} & {
            p.key for p in left.action.preconditions
        }
        incompatible = {
            p.key
            for p in left.action.effects
            for q in right.action.effects
            if p.key == q.key and p.value != q.value
        }
        ordered = left.id in ancestors[right.id] or right.id in ancestors[left.id]
        boolean(
            "write_conflict",
            not (overlap or fact_overlap or incompatible) or ordered,
            left.id + "/" + right.id,
            "Shared writes/state effects require explicit semantic ordering.",
        )
    for instance in plan.instances:
        required_cleanup = {a.id for a in actions.values() if instance.action.id in a.cleanup_for}
        selected_cleanup = {j.action.id for j in plan.instances if instance.id in ancestors[j.id]}
        boolean(
            "cleanup_closure",
            required_cleanup.issubset(selected_cleanup),
            instance.id,
            "Cuts/substitutions retain explicit restore and cleanup operations.",
        )
    # Every plan edit must retain its explicitly associated verification actions.
    for i in plan.instances:
        if i.action.kind not in {"edit", "bridge", "cleanup"}:
            continue
        required = {a.id for a in actions.values() if i.action.id in a.validation_for}
        selected = {
            j.action.id
            for j in plan.instances
            if i.id in ancestors[j.id] and j.action.kind == "validate"
        }
        boolean(
            "verification_closure",
            bool(required) and required.issubset(selected),
            i.id,
            "Truncation cannot drop a required validation action.",
        )
    final = state_for(ids)
    for goal in (*task.goals, *plan.required_effects):
        value = final.get((goal.key, goal.evaluator))
        add(
            "goal_coverage",
            CheckStatus.UNKNOWN
            if value is None
            else CheckStatus.PASS
            if value[0] == goal.value
            else CheckStatus.FAIL,
            goal.key,
            "Plan predicts required effect; actual repair requires independent acceptance.",
            value[1] if value else (),
        )
    if plan.pattern:
        for role in plan.pattern.roles:
            realized = [
                i for i in plan.instances if i.role == role.id and i.action.id in role.alternatives
            ]
            already_satisfied = bool(role.effects) and all(
                task.condition(e) == CheckStatus.PASS for e in role.effects
            )
            boolean(
                "pattern_role",
                not role.required or bool(realized) or already_satisfied,
                role.id,
                "Required role needs an evidenced realization or observed satisfaction.",
                role.evidence_refs,
            )
            for effect in role.effects if role.required else ():
                value = final.get((effect.key, effect.evaluator))
                boolean(
                    "pattern_role_effect",
                    value is not None and value[0] == effect.value,
                    role.id,
                    "Selected role realizes its required effect.",
                    role.evidence_refs,
                )
        for constraint in plan.pattern.partial_order:
            left = [i.id for i in plan.instances if i.role == constraint.before]
            right = [i.id for i in plan.instances if i.role == constraint.after]
            boolean(
                "pattern_dependency",
                all(a in ancestors[b] for a in left for b in right),
                plan.pattern.id,
                "Current plan preserves the Pattern's evidenced semantic dependency.",
            )
    boolean(
        "stop_conditions", bool(plan.stop_conditions), plan.id, "Plan has a stop/refresh boundary."
    )
    return PlanValidationReport(plan.id, tuple(checks))


def plan_id(task, actions, parents, *, pattern=None, dependencies=(), links=()):
    return (
        "task-plan:"
        + digest(
            {
                "task": task.task_id,
                "base": task.base_commit,
                "revision": task.revision,
                "actions": sorted(actions),
                "parents": sorted(parents),
                "pattern": pattern.id if pattern else None,
                "dependencies": [asdict(d) for d in dependencies],
                "links": [asdict(link) for link in links],
            }
        )[:20]
    )
