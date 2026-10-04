"""Ranker supervision with per-query temporal catalogs and bug-cluster isolation."""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass
from itertools import combinations

from .action_contracts import TemporalPolicy, digest, utc
from .pattern_contracts import load_native_package
from .plan_validation import ResourcePolicy, TaskWorkflowPlan
from .task_context import TaskContext, assert_public
from .workflow_ranker import CandidateCapsule, plan_capsule, workflow_capsule


@dataclass(frozen=True)
class HistoricalQuery:
    task: TaskContext
    bug_cluster_id: str
    fix_id: str
    aliases: tuple[str, ...] = ()
    copied_from: tuple[str, ...] = ()
    exposed: bool = False


@dataclass(frozen=True)
class SupervisionLabel:
    query_id: str
    candidate_id: str
    candidate_kind: str
    applicability: str | None
    label_source: str
    evidence_refs: tuple[str, ...]
    reviewer: str
    input_available_at: str
    outcome: bool | None = None
    regression_pass: bool | None = None
    measured_cost: float | None = None
    evaluator_version: str = ""
    trajectory_sha256: str = ""
    sampling_probability: float = 1.0
    replicate: int = 0
    operational_mode: str | None = None

    def __post_init__(self):
        if self.applicability is not None and self.applicability not in {
            "unrelated",
            "probe_only",
            "adaptively_usable",
        }:
            raise ValueError("invalid graded applicability")
        if self.label_source == "evidence_review" and self.applicability is None:
            raise ValueError("evidence review needs a reviewed applicability grade")
        if self.operational_mode not in {None, "use", "probe_only", "reject"}:
            raise ValueError("invalid operational authorization mode")
        if self.label_source == "evidence_review" and self.operational_mode is not None:
            raise ValueError("operational authorization is not an applicability review")
        if (
            self.label_source not in {"evidence_review", "execution"}
            or not self.evidence_refs
            or not self.reviewer
        ):
            raise ValueError("self-preference is not verified supervision")
        if self.candidate_kind not in {"workflow", "plan"}:
            raise ValueError("invalid supervised candidate kind")
        if not 0 < self.sampling_probability <= 1:
            raise ValueError("invalid sampling probability")
        utc(self.input_available_at)
        if self.label_source == "evidence_review" and any(
            value is not None for value in (self.outcome, self.regression_pass, self.measured_cost)
        ):
            raise ValueError("evidence review cannot claim an independently executed outcome")
        if self.measured_cost is not None and (
            type(self.measured_cost) not in (int, float) or not math.isfinite(self.measured_cost)
        ):
            raise ValueError("measured execution cost must be finite")
        if self.label_source == "execution" and (
            type(self.outcome) is not bool
            or type(self.regression_pass) is not bool
            or not self.evaluator_version
            or not re.fullmatch(r"[0-9a-f]{64}", self.trajectory_sha256)
            or self.measured_cost is None
            or self.measured_cost < 0
        ):
            raise ValueError(
                "execution label needs completed independent evaluation, trajectory and cost"
            )


@dataclass(frozen=True)
class TrainingExample:
    query_id: str
    bug_cluster_id: str
    split: str
    task_input: dict
    candidate: dict
    label: dict
    temporal_catalog_sha256: str
    catalog_cutoff: str


def eligible_catalog(query: HistoricalQuery, references, *, training_cutoff, main_cutoff):
    tq = utc(query.task.input_available_at)
    tau = utc(training_cutoff)
    if not tau < utc(main_cutoff) or tq >= utc(main_cutoff) or query.exposed:
        raise ValueError("formal/exposed queries cannot supervise the ranker")
    cutoff = query.task.input_available_at if tq < tau else training_cutoff
    policy = TemporalPolicy(
        cutoff,
        (query.task.task_id, *query.aliases, *query.copied_from),
        (query.bug_cluster_id,),
        (query.fix_id,),
    )
    eligible, rejected = [], []
    for ref in references:
        try:
            package = load_native_package(ref, policy)
        except (ValueError, OSError) as exc:
            rejected.append({"package_id": ref.get("skill_id"), "reason": str(exc)})
            continue
        eligible.append(package.reference)
    snapshot = digest(sorted((r["skill_id"], r["package_sha256"]) for r in eligible))
    return policy, tuple(eligible), snapshot, tuple(rejected)


def build_examples(
    queries,
    references,
    labels,
    candidate_provider,
    *,
    training_cutoff,
    main_cutoff,
    excluded_query_ids=(),
):
    identities = {}
    clusters = {}
    fixes = {}
    for query in queries:
        qid = query.task.task_id
        if qid in excluded_query_ids:
            raise ValueError("excluded target query in ranker population")
        names = {qid, *query.aliases, *query.copied_from}
        if names & set(excluded_query_ids):
            raise ValueError("excluded alias/copied query in ranker population")
        if names & set(identities):
            raise ValueError("duplicate/aliased/copied ranker query")
        identities.update({name: qid for name in names})
        split = (
            "train" if utc(query.task.input_available_at) < utc(training_cutoff) else "development"
        )
        if query.bug_cluster_id in clusters and clusters[query.bug_cluster_id] != split:
            raise ValueError("bug cluster crosses training/development boundary")
        clusters[query.bug_cluster_id] = split
        if query.fix_id in fixes and fixes[query.fix_id] != split:
            raise ValueError("fix crosses training/development boundary")
        fixes[query.fix_id] = split
    by_label = {}
    for label in labels:
        key = (label.query_id, label.candidate_id, label.label_source, label.replicate)
        if key in by_label:
            raise ValueError("duplicate supervision observation")
        by_label[key] = label
    examples, audits = [], []
    used_labels = set()
    for query in queries:
        policy, eligible, snapshot, rejected = eligible_catalog(
            query, references, training_cutoff=training_cutoff, main_cutoff=main_cutoff
        )
        resource_policy = ResourcePolicy(policy, eligible)
        native_workflows = {w.id: w for p in resource_policy.load() for w in p.workflows}
        capsules = []
        for item in candidate_provider(query.task, eligible, policy):
            if isinstance(item, TaskWorkflowPlan):
                capsule, report = plan_capsule(item, query.task, resource_policy)
                if report.status == "FAIL":
                    # Hard negatives may remain labeled unrelated; their contract failure is visible.
                    pass
            else:
                capsule = item
                if capsule.candidate_kind != "workflow" or capsule.id not in native_workflows:
                    raise ValueError(
                        "supervision candidate lacks authoritative Workflow or Task Plan"
                    )
                if capsule != workflow_capsule(
                    native_workflows[capsule.id], query.task, resource_policy
                ):
                    raise ValueError("supervision capsule differs from native source")
            capsules.append(capsule)
        capsules = tuple(capsules)
        if len({c.id for c in capsules}) != len(capsules):
            raise ValueError("duplicate training candidate")
        split = clusters[query.bug_cluster_id]
        task_input = query.task.to_dict()
        task_input.pop("root")
        assert_public(task_input)
        for c in capsules:
            for key, label in by_label.items():
                if label.query_id != query.task.task_id or label.candidate_id != c.id:
                    continue
                if (
                    label.input_available_at != query.task.input_available_at
                    or label.candidate_kind != c.candidate_kind
                ):
                    raise ValueError("label query time/candidate kind mismatch")
                examples.append(
                    TrainingExample(
                        query.task.task_id,
                        query.bug_cluster_id,
                        split,
                        task_input,
                        c.to_dict(),
                        asdict(label),
                        snapshot,
                        policy.cutoff,
                    )
                )
                used_labels.add(key)
        audits.append(
            {
                "query_id": query.task.task_id,
                "split": split,
                "catalog_sha256": snapshot,
                "catalog_cutoff": policy.cutoff,
                "eligible_packages": len(eligible),
                "candidate_count": len(capsules),
                "rejected_packages": rejected,
                "unrun_candidates_are_failure_labels": False,
            }
        )
    if set(by_label) != used_labels:
        raise ValueError("label references a missing, future or excluded candidate/query")
    return tuple(examples), tuple(audits)


def pair_preferences(examples):
    """Pair verified observations within a query; preserve ties and sampling weights."""
    groups = {}
    for e in examples:
        groups.setdefault((e.query_id, e.candidate["candidate_kind"], e.split), []).append(e)
    pairs = []
    for (qid, kind, split), items in groups.items():
        # Aggregate replicates, never pick the best attempt.
        candidates = {}
        for e in items:
            candidates.setdefault(e.candidate["id"], []).append(e)

        def selected(entries, source):
            return [e for e in entries if e.label["label_source"] == source]

        def score(entries, execution=False):
            labels = [e.label for e in entries]
            if execution:
                return sum(
                    int(item["outcome"] and item["regression_pass"]) for item in labels
                ) / len(labels)
            values = {"unrelated": 0, "probe_only": 1, "adaptively_usable": 2}
            return sum(values[item["applicability"]] for item in labels) / len(labels)

        for left, right in combinations(sorted(candidates), 2):
            both_executed = all(selected(candidates[cid], "execution") for cid in (left, right))
            source = "execution" if both_executed else "evidence_review"
            observations = [selected(candidates[cid], source) for cid in (left, right)]
            if not all(observations):
                # Operational grades on an execution are not reviewed mechanism labels.
                # A missing execution or independent review does not imply a loser.
                continue
            a, b = (score(entries, both_executed) for entries in observations)
            pairs.append(
                {
                    "query_id": qid,
                    "candidate_kind": kind,
                    "split": split,
                    "left": left,
                    "right": right,
                    "target": 1.0 if a > b else 0.0 if a < b else 0.5,
                    "supervision": "execution" if both_executed else "reviewed_applicability",
                    "tie": a == b,
                    "observations": [len(entries) for entries in observations],
                    "sampling_probabilities": [
                        min(e.label["sampling_probability"] for e in entries)
                        for entries in observations
                    ],
                }
            )
    return tuple(pairs)


def validate_training_snapshot(payload):
    if payload.get("schema") != "temporal-workflow-ranker-data-v1":
        raise ValueError("unsupported ranking dataset")
    if not utc(payload["training_cutoff"]) < utc(payload["main_cutoff"]):
        raise ValueError("invalid ranker temporal split")
    examples = payload["examples"]
    clusters = {}
    for row in examples:
        task, label = row["task_input"], row["label"]
        if (
            row["query_id"] != task["task_id"]
            or label["query_id"] != row["query_id"]
            or label["candidate_id"] != row["candidate"]["id"]
            or label["candidate_kind"] != row["candidate"]["candidate_kind"]
        ):
            raise ValueError("supervision identity mismatch")
        assert_public(task)
        CandidateCapsule(
            **{
                **row["candidate"],
                **{
                    key: tuple(row["candidate"][key])
                    for key in (
                        "conditions",
                        "exclusions",
                        "action_roles",
                        "evidence_refs",
                        "package_hashes",
                        "validation_summary",
                    )
                },
            }
        )
        SupervisionLabel(**{**label, "evidence_refs": tuple(label["evidence_refs"])})
        tq = utc(task["input_available_at"])
        if tq >= utc(payload["main_cutoff"]) or utc(row["catalog_cutoff"]) > tq:
            raise ValueError("future supervision/candidate catalog")
        expected = "train" if tq < utc(payload["training_cutoff"]) else "development"
        if row["split"] != expected or label["input_available_at"] != task["input_available_at"]:
            raise ValueError("temporal label split mismatch")
        if row["split"] == "train" and row["catalog_cutoff"] != task["input_available_at"]:
            raise ValueError("training catalogs must be reconstructed as of each query")
        if row["split"] == "development" and row["catalog_cutoff"] != payload["training_cutoff"]:
            raise ValueError("development catalog must freeze at training cutoff")
        if row["bug_cluster_id"] in clusters and clusters[row["bug_cluster_id"]] != row["split"]:
            raise ValueError("ranker cluster leakage")
        clusters[row["bug_cluster_id"]] = row["split"]
    recorded = payload.get("dataset_sha256")
    if recorded != digest({k: v for k, v in payload.items() if k != "dataset_sha256"}):
        raise ValueError("ranker dataset content hash mismatch")
    return payload


def execution_label_from_run(
    query, candidate_id, candidate_kind, run, *, sampling_probability, replicate=0
):
    """Include controlled failures after termination and completed independent evaluation."""
    assert_public(run)
    evaluation = run.get("evaluation", {})
    if run.get("task_id") != query.task.task_id or run.get("base_commit") != query.task.base_commit:
        raise ValueError("execution trajectory belongs to another query/base")
    if (
        not (run.get("solver_ended") or run.get("solver_terminated"))
        or not evaluation.get("evaluator_version")
        or evaluation.get("evaluation_completed") is not True
    ):
        raise ValueError("completed independent execution is required")
    if evaluation.get("causal_controls_passed") is not True:
        raise ValueError(
            "causally reconciled independent evaluation is required for utility supervision"
        )
    usage = run.get("guidance_usage", [])
    relevant = (
        [record for record in usage if record["plan_id"] == candidate_id]
        if candidate_kind == "plan"
        else [record for record in usage if record["parent_workflow_ids"] == [candidate_id]]
    )
    if not relevant:
        raise ValueError("trajectory did not use the nominated candidate as controlled guidance")
    if candidate_kind == "workflow":
        switched = any(record["parent_workflow_ids"] != [candidate_id] for record in usage)
    else:
        switched = any(
            record["plan_id"] != candidate_id and record.get("nominated_plan_id") != candidate_id
            for record in usage
        )
    if switched:
        raise ValueError("trajectory switched away from the nominated controlled candidate")
    if not run.get("requests") or run["budget"].get("model_tokens", 0) <= 0:
        raise ValueError("controlled guidance did not reach a real solver request")
    return SupervisionLabel(
        query.task.task_id,
        candidate_id,
        candidate_kind,
        None,
        "execution",
        ("evaluation:" + evaluation["evaluation_spec_sha256"],),
        "independent-evaluator",
        query.task.input_available_at,
        outcome=bool(
            run.get("solver_ended") and not run.get("failure") and run.get("benchmark_resolved")
        ),
        regression_pass=bool(evaluation.get("regression_exit_codes"))
        and all(code == 0 for code in evaluation["regression_exit_codes"]),
        measured_cost=float(run["budget"]["model_tokens"]),
        evaluator_version=evaluation["evaluator_version"],
        trajectory_sha256=digest(run),
        sampling_probability=sampling_probability,
        replicate=replicate,
    )
