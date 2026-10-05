"""Validation-only historical causal identity; never rewrite native Skill sources."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from .action_contracts import SourceRecord, utc
from .history_census import fingerprint


def validate_cluster_review(response, records):
    allowed, evidence = {}, {}
    for row in records:
        owned = allowed.setdefault(row["issue_id"], set())
        for entry in row["entries"]:
            key = (row["issue_id"], entry["id"])
            if key in evidence and evidence[key] != fingerprint(entry):
                raise ValueError("ambiguous causal evidence ID; namespace source variants")
            evidence[key] = fingerprint(entry)
            owned.add(entry["id"])
    reviews = response.get("reviews")
    if not isinstance(reviews, list) or len(reviews) != len(allowed):
        raise ValueError("cluster review omitted or added historical issues")
    if {row.get("issue_id") for row in reviews} != set(allowed):
        raise ValueError("cluster review changed issue identities")
    for row in reviews:
        if (
            not row.get("mechanism")
            or not row.get("reason")
            or not row.get("evidence_refs")
            or not set(row["evidence_refs"]).issubset(allowed[row["issue_id"]])
        ):
            raise ValueError("causal review lacks issue-owned evidence")
    for kind in ("duplicate_groups", "uncertain_groups"):
        if not isinstance(response.get(kind), list):
            raise ValueError("cluster groups must be explicit arrays")  # noqa: TRY004
        for group in response[kind]:
            members = group.get("members", [])
            if (
                len(set(members)) < 2
                or len(set(members)) != len(members)
                or not set(members).issubset(allowed)
                or not group.get("reason")
            ):
                raise ValueError("cluster group members or rationale are invalid")
            refs = set(group.get("evidence_refs", []))
            if (
                not refs
                or not refs.issubset(set().union(*(allowed[member] for member in members)))
                or any(not refs.intersection(allowed[member]) for member in members)
            ):
                raise ValueError("cluster relation requires evidence for every member")
    return response


@dataclass(frozen=True)
class IsolationSource:
    id: str
    bug_cluster_id: str
    fix_id: str
    revision: str
    aliases: tuple[str, ...] = ()
    copied_from: tuple[str, ...] = ()
    source_sha256: str = ""

    @classmethod
    def from_source(cls, source):
        return cls(
            source.id,
            source.bug_cluster_id,
            source.fix_id,
            source.revision,
            source.aliases,
            source.copied_from,
            fingerprint(asdict(source)),
        )

    @property
    def names(self):
        return (
            self.id,
            self.bug_cluster_id,
            *self.aliases,
            *self.copied_from,
            self.fix_id,
            "revision:" + self.revision,
        )


@dataclass(frozen=True)
class IsolationComponent:
    id: str
    identities: tuple[str, ...]
    bug_clusters: tuple[str, ...]
    fix_ids: tuple[str, ...]
    conservative_uncertainty: bool


@dataclass(frozen=True)
class HistoricalIsolation:
    sources: tuple[IsolationSource, ...]
    components: tuple[IsolationComponent, ...]
    review_sha256: tuple[str, ...]
    reviewed_issue_ids: tuple[str, ...]
    reviewed_source_ids: tuple[str, ...]

    @property
    def full_corpus_causal_review_complete(self):
        return bool(self.sources) and {s.id for s in self.sources}.issubset(
            self.reviewed_source_ids
        )

    @property
    def sha256(self):
        return fingerprint(asdict(self))

    def to_dict(self):
        return {
            "schema": "historical-causal-isolation-v1",
            **asdict(self),
            "isolation_sha256": self.sha256,
            "validation_only": True,
            "full_corpus_causal_review_complete": self.full_corpus_causal_review_complete,
        }

    @classmethod
    def from_dict(cls, value):
        if (
            value.get("schema") != "historical-causal-isolation-v1"
            or value.get("validation_only") is not True
        ):
            raise ValueError("unsupported or overclaimed causal isolation index")
        result = cls(
            tuple(
                IsolationSource(
                    **{**s, "aliases": tuple(s["aliases"]), "copied_from": tuple(s["copied_from"])}
                )
                for s in value["sources"]
            ),
            tuple(
                IsolationComponent(
                    **{**c, **{k: tuple(c[k]) for k in ("identities", "bug_clusters", "fix_ids")}}
                )
                for c in value["components"]
            ),
            tuple(value["review_sha256"]),
            tuple(value["reviewed_issue_ids"]),
            tuple(value["reviewed_source_ids"]),
        )
        if (
            value.get("full_corpus_causal_review_complete")
            is not result.full_corpus_causal_review_complete
        ):
            raise ValueError("causal isolation review coverage is overclaimed")
        if result.sha256 != value.get("isolation_sha256"):
            raise ValueError("causal isolation index hash mismatch")
        # The closure is derived, not an independently editable source of truth.
        names = [name for c in result.components for name in c.identities]
        if len(names) != len(set(names)) or len({s.id for s in result.sources}) != len(
            result.sources
        ):
            raise ValueError("ambiguous causal isolation identity")
        for s in result.sources:
            if not re.fullmatch(r"[0-9a-f]{40}", s.revision):
                raise ValueError("invalid causal isolation source revision")
            if s.source_sha256 and not re.fullmatch(r"[0-9a-f]{64}", s.source_sha256):
                raise ValueError("invalid causal isolation source fingerprint")
            containing = [c for c in result.components if s.id in c.identities]
            if len(containing) != 1 or not set(s.names).issubset(containing[0].identities):
                raise ValueError("causal isolation omitted source identity closure")
        return result

    @classmethod
    def load(cls, path):
        return cls.from_dict(json.loads(Path(path).read_text()))

    def related_components(self, identities):
        names = set(identities)
        return tuple(c for c in self.components if names.intersection(c.identities))

    def query_components(self, query):
        return self.related_components(
            (
                query.task.task_id,
                query.bug_cluster_id,
                query.fix_id,
                *query.aliases,
                *query.copied_from,
            )
        )

    def cluster_keys(self, query):
        return (query.bug_cluster_id, *(c.id for c in self.query_components(query)))

    def query_cluster_id(self, query):
        groups = self.query_components(query)
        if not groups:
            return query.bug_cluster_id
        if len(groups) == 1:
            return groups[0].id
        return "causal-isolation:" + fingerprint(sorted(c.id for c in groups))[:24]

    def query_exclusions(self, query):
        groups = self.query_components(query)
        return (
            tuple(
                sorted(
                    {
                        query.task.task_id,
                        *query.aliases,
                        *query.copied_from,
                        *(name for c in groups for name in c.identities),
                    }
                )
            ),
            tuple(
                sorted({query.bug_cluster_id, *(name for c in groups for name in c.bug_clusters)})
            ),
            tuple(sorted({query.fix_id, *(name for c in groups for name in c.fix_ids)})),
        )

    def verify_sources(self, sources):
        authority = {s.id: s for s in self.sources}
        for source in sources:
            expected = authority.get(source.id)
            if expected is None:
                raise ValueError("native source absent from causal isolation index")
            if (expected.bug_cluster_id, expected.fix_id, expected.revision) != (
                source.bug_cluster_id,
                source.fix_id,
                source.revision,
            ) or (expected.source_sha256 and expected.source_sha256 != fingerprint(asdict(source))):
                raise ValueError("native source differs from causal isolation authority")

    def independent_source_groups(self, sources):
        self.verify_sources(sources)
        return tuple(
            sorted(
                {
                    c.id
                    for s in sources
                    for c in self.related_components(
                        (s.id, s.bug_cluster_id, s.fix_id, "revision:" + s.revision)
                    )
                }
            )
        )


def reconcile_cluster_reviews(review_directories, sources: tuple[SourceRecord, ...] = ()):
    """Merge exact accepted reviews and authoritative aliases/fixes/copies as exclusions.

    Uncertain relations are conservative exclusions, not confirmed duplicate labels.
    No reviewer mechanism, target repair text, or hidden observation is exported.
    """
    known = {s.id: IsolationSource.from_source(s) for s in sources}
    if len(known) != len(sources):
        raise ValueError("duplicate supplied causal isolation source")
    relations, reviewed, reviewed_sources, receipt_hashes = [], set(), set(), []
    for directory in review_directories:
        directory = Path(directory)
        payload = json.loads((directory / "review-input.json").read_text())
        response = json.loads((directory / "review-response.json").read_text())
        receipt = json.loads((directory / "cluster-review.json").read_text())
        records = payload["historical_records"]
        if (
            receipt.get("schema")
            not in {"historical-causal-cluster-review-v1", "historical-causal-cluster-review-v2"}
            or receipt.get("input_sha256") != fingerprint(payload)
            or receipt.get("response_sha256") != fingerprint(response)
            or receipt.get("review") != response
            or receipt.get("issue_count") != len({r["issue_id"] for r in records})
            or (
                receipt["schema"] == "historical-causal-cluster-review-v2"
                and receipt.get("source_count") != len(records)
            )
            or receipt.get("query_count") != len(payload["queries"])
        ):
            raise ValueError("causal review receipt disagrees with exact input/response")
        cutoff = utc(payload["cutoff_exclusive"])
        if any(utc(e["available_at"]) >= cutoff for row in records for e in row["entries"]):
            raise ValueError("post-cutoff evidence in causal identity review")
        validate_cluster_review(response, records)
        receipt_hashes.append(fingerprint(receipt))
        for row in records:
            candidate = IsolationSource(
                row["source_id"], row["issue_id"], row["fix_id"], row["revision"]
            )
            if candidate.id in known:
                existing = known[candidate.id]
                if (existing.bug_cluster_id, existing.fix_id, existing.revision) != (
                    candidate.bug_cluster_id,
                    candidate.fix_id,
                    candidate.revision,
                ):
                    raise ValueError("review source differs from immutable native authority")
            else:
                known[candidate.id] = candidate
            reviewed.add(row["issue_id"])
            reviewed_sources.add(row["source_id"])
        relations.extend(
            (tuple(g["members"]), kind == "uncertain_groups")
            for kind in ("duplicate_groups", "uncertain_groups")
            for g in response[kind]
        )
    if not receipt_hashes:
        raise ValueError("causal isolation requires an accepted review")
    parents = {}

    def root(name):
        parents.setdefault(name, name)
        while parents[name] != name:
            parents[name] = parents[parents[name]]
            name = parents[name]
        return name

    def merge(names):
        first = root(names[0])
        for name in names[1:]:
            other = root(name)
            if other != first:
                parents[other] = first

    for source in known.values():
        merge(source.names)
    for names, _uncertain in relations:
        merge(names)
    grouped = {}
    for name in parents:
        grouped.setdefault(root(name), set()).add(name)
    components = []
    for names in grouped.values():
        members = [s for s in known.values() if s.id in names]
        clusters = tuple(sorted({s.bug_cluster_id for s in members}))
        components.append(
            IsolationComponent(
                "causal-isolation:" + fingerprint(clusters)[:24],
                tuple(sorted(names)),
                clusters,
                tuple(sorted({s.fix_id for s in members})),
                any(uncertain and set(group).intersection(names) for group, uncertain in relations),
            )
        )
    result = HistoricalIsolation(
        tuple(sorted(known.values(), key=lambda s: s.id)),
        tuple(sorted(components, key=lambda c: c.id)),
        tuple(sorted(set(receipt_hashes))),
        tuple(sorted(reviewed)),
        tuple(sorted(reviewed_sources)),
    )
    return HistoricalIsolation.from_dict(result.to_dict())
