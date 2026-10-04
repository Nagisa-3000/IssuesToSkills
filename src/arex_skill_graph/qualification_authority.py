"""Bind independent historical replay records to immutable native source identities.

Replay reports are validation provenance. Their checked_at, runtime and outputs
never become pre-cutoff evidence or proof that authored Skill evals executed.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from .action_contracts import TemporalPolicy, utc
from .history_census import fingerprint

PHASES = ("original_base", "base_with_regression", "historical_fixed")


def validate_historical_qualification(report, source, policy, *, fix_aliases=()):
    """Check artifacts under both the query and original replay boundaries.

    Later validation never changes report hashes, artifact dates, or learned
    content. NativePackage.admit additionally checks the full generation context.
    """
    policy.check(source)
    identity = report["identity"]
    qid = identity["issue_id"]
    if (
        report.get("schema") != "historical-causal-verification-v1"
        or not source.verified_resolution
        or qid != source.bug_cluster_id
        or qid.rsplit(":", 1)[0] != source.repository
        or identity["merge_commit"] != source.revision
        or not re.fullmatch(r"[0-9a-f]{40}", identity["base_commit"])
        or utc(source.available_at) >= utc(identity["cutoff_exclusive"])
        or identity.get("fix_id") not in {source.fix_id, *fix_aliases}
        or utc(identity["repair_available_at"]) > utc(source.available_at)
        or utc(identity["repair_available_at"]) >= utc(policy.cutoff)
        or utc(report["checked_at"]) < utc(identity["repair_available_at"])
    ):
        raise ValueError("historical qualification source identity/time mismatch")
    if (
        report.get("verified_resolution") is not True
        or report.get("historical_artifact_verified") is not True
        or report.get("issue_relationship_verified") is not True
        or identity.get("resolution_relationship") not in {"direct_closure", "closing_reference"}
        or not identity.get("resolution_relationship_evidence_refs")
        or report.get("qualification_scope") != "changed-test-files-with-original-base-control"
        or report.get("formal_SWE_run") is not False
        or report.get("verification_does_not_backdate_new_information") is not True
    ):
        raise ValueError("historical qualification lacks independent causal/relationship controls")
    observations = report["observations"]
    runs = report["runs"]
    if (
        set(observations) != set(PHASES)
        or set(runs) != set(PHASES)
        or fingerprint(observations) != report["observations_sha256"]
        or not re.fullmatch(r"[0-9a-f]{64}", report["runtime_sha256"])
        or any(
            not isinstance(observations[p], dict)
            or not observations[p]
            or not set(observations[p].values()).issubset({"passed", "failed", "skipped"})
            or runs[p].get("timed_out") is not False
            or runs[p].get("runtime_sha256") != report["runtime_sha256"]
            or not runs[p].get("isolation")
            for p in PHASES
        )
    ):
        raise ValueError("historical qualification observations/runtime changed or incomplete")
    original, before, after = (observations[p] for p in PHASES)
    f2p = sorted(k for k, v in before.items() if v == "failed" and after.get(k) == "passed")
    p2p = sorted(k for k, v in original.items() if v == "passed")
    if (
        [runs[p]["exit_code"] for p in PHASES] != [0, 1, 0]
        or not f2p
        or not p2p
        or report["fail_to_pass"] != f2p
        or report["pass_to_pass"] != p2p
        or set(before) != set(after)
        or any(v not in {"passed", "skipped"} for v in original.values())
        or any(after.get(k) != "passed" for k in p2p)
        or any(v not in {"passed", "skipped"} for v in after.values())
    ):
        raise ValueError("historical qualification causal outcomes do not recompute")


@dataclass(frozen=True)
class HistoricalQualification:
    source_id: str
    verification_sha256: str
    inventory_sha256: str
    report: dict
    fix_aliases: tuple[str, ...] = ()

    def validate(self, source, policy):
        if self.source_id != source.id or fingerprint(self.report) != self.verification_sha256:
            raise ValueError("qualification record binding/hash changed")
        validate_historical_qualification(self.report, source, policy, fix_aliases=self.fix_aliases)

    def to_dict(self):
        return {
            "source_id": self.source_id,
            "verification_sha256": self.verification_sha256,
            "inventory_sha256": self.inventory_sha256,
            "fix_aliases": list(self.fix_aliases),
            "report": self.report,
            "purpose": "validation-only; not pre-cutoff learned content or Skill functional execution",
        }


def load_source_qualifications(inventory_path, sources, policy: TemporalPolicy):
    """Require completed canonical inventory and one matching report per source.

    Alias acceptance requires the same repository, issue and complete merge SHA;
    unrelated mentions do not become independent resolution support.
    """
    inventory = json.loads(Path(inventory_path).read_text())
    rows = inventory["results"]
    if inventory.get(
        "schema"
    ) != "historical-development-verification-inventory-v1" or inventory.get(
        "canonical_requested_count"
    ) != len(rows):
        raise ValueError("qualification inventory is not a complete canonical population")
    by_source = {source.id: source for source in sources}
    if len(by_source) != len(sources):
        raise ValueError("duplicate qualification source identity")
    matched = {}
    for row in rows:
        if row.get("verified_resolution") is not True:
            continue
        candidates = [s for s in sources if s.bug_cluster_id == row["issue_id"]]
        if not candidates:
            continue
        report = json.loads(Path(row["verification_path"]).read_text())
        identity = report["identity"]
        if (
            identity["issue_id"] != row["issue_id"]
            or identity.get("fix_id") != row["fix_id"]
            or row["fail_to_pass_count"] != len(report["fail_to_pass"])
            or row["pass_to_pass_count"] != len(report["pass_to_pass"])
        ):
            raise ValueError("qualification inventory row disagrees with its report")
        aliases = {row["fix_id"]}
        for alias in row.get("request_aliases", []):
            locator = alias.get("locator", {})
            if (
                locator.get("repository") == row["issue_id"].rsplit(":", 1)[0]
                and locator.get("commit") == identity["merge_commit"]
            ):
                aliases.add(alias["fix_id"])
        for source in candidates:
            if source.revision != identity["merge_commit"] or source.fix_id not in aliases:
                continue
            if source.id in matched:
                raise ValueError("duplicate canonical qualification for one source")
            record = HistoricalQualification(
                source.id,
                fingerprint(report),
                fingerprint(inventory),
                report,
                tuple(sorted(aliases)),
            )
            record.validate(source, policy)
            matched[source.id] = record
    if set(matched) != set(by_source):
        raise ValueError(
            "missing independently verified source qualifications: "
            + str(sorted(set(by_source) - set(matched)))
        )
    return tuple(matched[sid] for sid in sorted(matched))
