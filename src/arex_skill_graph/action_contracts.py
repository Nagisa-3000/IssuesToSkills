"""Versioned action contracts. Expected effects are never observed execution results."""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Any, Mapping, TypeVar


class CheckStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


T = TypeVar("T")


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()
    ).hexdigest()


def utc(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("timestamps must include a timezone")
    return result.astimezone(timezone.utc)


def contained_resource(value: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ValueError("resource must be a contained relative path")
    return value


def text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")
    return value


def strict(value: Mapping[str, Any], cls: type[T]) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{cls.__name__} must be an object")
    unknown = set(value) - {f.name for f in fields(cls)}
    if unknown:
        raise ValueError(f"unknown {cls.__name__} fields: {', '.join(sorted(unknown))}")
    return dict(value)


def strings(value: Any) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or any(not isinstance(x, str) or not x for x in value):
        raise ValueError("expected an array of nonempty strings")
    return tuple(value)


@dataclass(frozen=True)
class Predicate:
    key: str
    value: str | bool
    evaluator: str = "evidence"
    description: str = field(default="", compare=False)

    def __post_init__(self):
        text(self.key, "predicate key")
        if not isinstance(self.value, (str, bool)):
            raise ValueError("predicate values must be strings or booleans")
        if self.evaluator not in {"evidence", "file_exists", "symbol_exists"}:
            raise ValueError("unknown predicate evaluator")
        if self.evaluator != "evidence" and type(self.value) is not bool:
            raise ValueError("existence predicates require boolean values")

    @classmethod
    def from_dict(cls, value):
        return cls(**strict(value, cls))


@dataclass(frozen=True)
class Port:
    name: str
    semantic_role: str
    artifact_kind: str
    language: str
    scope: str
    phase: str
    state: str
    optional: bool = False

    def __post_init__(self):
        for key in (
            "name",
            "semantic_role",
            "artifact_kind",
            "language",
            "scope",
            "phase",
            "state",
        ):
            text(getattr(self, key), key)
        if type(self.optional) is not bool:
            raise ValueError("port optional must be boolean")

    @classmethod
    def from_dict(cls, value):
        return cls(**strict(value, cls))

    def compatible(self, consumer: Port) -> bool:
        # A candidate connection; semantic evidence is checked separately.
        return all(
            getattr(self, key) == getattr(consumer, key)
            for key in ("semantic_role", "artifact_kind", "language", "scope", "phase", "state")
        )


@dataclass(frozen=True)
class Oracle:
    id: str
    instruction: str
    evidence_refs: tuple[str, ...]
    kind: str = "public_probe"
    command: tuple[str, ...] = ()

    def __post_init__(self):
        text(self.id, "oracle ID")
        text(self.instruction, "oracle instruction")
        if self.kind not in {"public_probe", "public_mre", "repository_test"}:
            raise ValueError("oracle must use public inputs")
        if not self.evidence_refs:
            raise ValueError("oracle requires evidence")

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["evidence_refs"] = strings(d.get("evidence_refs", []))
        d["command"] = strings(d.get("command", []))
        return cls(**d)


@dataclass(frozen=True)
class SourceRecord:
    id: str
    repository: str
    bug_cluster_id: str
    fix_id: str
    revision: str
    available_at: str
    evidence_refs: tuple[str, ...]
    aliases: tuple[str, ...] = ()
    copied_from: tuple[str, ...] = ()
    verified_resolution: bool = False

    def __post_init__(self):
        for key in ("id", "repository", "bug_cluster_id", "fix_id", "revision"):
            text(getattr(self, key), key)
        utc(self.available_at)
        if not re.fullmatch(r"[0-9a-f]{40}", self.revision):
            raise ValueError("source revision must be a commit SHA")
        if not self.evidence_refs or type(self.verified_resolution) is not bool:
            raise ValueError("source requires evidence and explicit resolution state")

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        for key in ("evidence_refs", "aliases", "copied_from"):
            d[key] = strings(d.get(key, []))
        return cls(**d)


@dataclass(frozen=True)
class TemporalPolicy:
    cutoff: str
    excluded_ids: tuple[str, ...] = ()
    excluded_clusters: tuple[str, ...] = ()
    excluded_fixes: tuple[str, ...] = ()

    def __post_init__(self):
        utc(self.cutoff)

    def check(self, source: SourceRecord) -> None:
        if utc(source.available_at) >= utc(self.cutoff):
            raise ValueError("source is not available before cutoff")
        if (
            {source.id, *source.aliases, *source.copied_from} & set(self.excluded_ids)
            or source.bug_cluster_id in self.excluded_clusters
            or source.fix_id in self.excluded_fixes
        ):
            raise ValueError("source belongs to an excluded identity/bug cluster/fix")
        if not source.verified_resolution:
            raise ValueError("unverified resolution cannot authorize repair actions")


@dataclass(frozen=True)
class ActionContract:
    id: str
    intent: str
    mechanism: str
    semantic_role: str
    owner_role: str
    operation: str
    inputs: tuple[Port, ...]
    outputs: tuple[Port, ...]
    preconditions: tuple[Predicate, ...]
    effects: tuple[Predicate, ...]
    preserves: tuple[Predicate, ...]
    oracle: tuple[Oracle, ...]
    source_ids: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    resource: str
    package_id: str
    package_hash: str = ""
    kind: str = "edit"
    read_set: tuple[str, ...] = ()
    write_set: tuple[str, ...] = ()
    invalidates: tuple[str, ...] = ()
    exclusions: tuple[Predicate, ...] = ()
    validation_for: tuple[str, ...] = ()
    cleanup_for: tuple[str, ...] = ()
    estimated_cost: float = 1.0

    def __post_init__(self):
        for key in (
            "id",
            "intent",
            "mechanism",
            "semantic_role",
            "owner_role",
            "operation",
            "package_id",
        ):
            text(getattr(self, key), key)
        contained_resource(self.resource)
        if self.kind not in {"probe", "read", "edit", "validate", "bridge", "cleanup"}:
            raise ValueError("invalid action kind")
        if not self.oracle or not self.source_ids or not self.evidence_refs:
            raise ValueError("action requires oracle, source identities and evidence")
        if not self.effects and not self.outputs:
            raise ValueError("action must specify observable outputs or effects")
        for ports in (self.inputs, self.outputs):
            if len({p.name for p in ports}) != len(ports):
                raise ValueError("duplicate action port")
        if not math.isfinite(self.estimated_cost) or self.estimated_cost < 0:
            raise ValueError("invalid action cost")
        if self.package_hash and not re.fullmatch(r"[0-9a-f]{64}", self.package_hash):
            raise ValueError("invalid package hash")

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        for key in ("inputs", "outputs"):
            d[key] = tuple(Port.from_dict(x) for x in d.get(key, []))
        for key in ("preconditions", "effects", "preserves", "exclusions"):
            d[key] = tuple(Predicate.from_dict(x) for x in d.get(key, []))
        d["oracle"] = tuple(Oracle.from_dict(x) for x in d.get("oracle", []))
        for key in (
            "source_ids",
            "evidence_refs",
            "read_set",
            "write_set",
            "invalidates",
            "validation_for",
            "cleanup_for",
        ):
            d[key] = strings(d.get(key, []))
        return cls(**d)

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Dependency:
    before: str
    after: str
    reason: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self):
        if self.before == self.after or not self.evidence_refs:
            raise ValueError("dependency requires distinct endpoints and evidence")
        text(self.reason, "dependency reason")

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["evidence_refs"] = strings(d.get("evidence_refs", []))
        return cls(**d)


@dataclass(frozen=True)
class WorkflowContract:
    id: str
    goal: str
    mechanism: str
    actions: tuple[ActionContract, ...]
    source_ids: tuple[str, ...]
    required_effects: tuple[Predicate, ...]
    invariants: tuple[Predicate, ...]
    dependencies: tuple[Dependency, ...] = ()
    package_id: str = ""
    package_hash: str = ""
    optional_action_ids: tuple[str, ...] = ()

    def __post_init__(self):
        for key in ("id", "goal", "mechanism"):
            text(getattr(self, key), key)
        ids = {a.id for a in self.actions}
        if not ids or len(ids) != len(self.actions) or not self.source_ids:
            raise ValueError("workflow requires unique actions and sources")
        if not set(self.optional_action_ids).issubset(ids):
            raise ValueError("optional historical Action is dangling")
        if any(d.before not in ids or d.after not in ids for d in self.dependencies):
            raise ValueError("dangling historical dependency")

    @classmethod
    def from_dict(cls, value):
        d = strict(value, cls)
        d["actions"] = tuple(ActionContract.from_dict(x) for x in d.get("actions", []))
        d["source_ids"] = strings(d.get("source_ids", []))
        d["optional_action_ids"] = strings(d.get("optional_action_ids", []))
        for key in ("required_effects", "invariants"):
            d[key] = tuple(Predicate.from_dict(x) for x in d.get(key, []))
        d["dependencies"] = tuple(Dependency.from_dict(x) for x in d.get("dependencies", []))
        return cls(**d)

    def to_dict(self):
        return asdict(self)


def read_contract(markdown: str, marker: str = "arex-contract-v4") -> Mapping[str, Any]:
    matches = re.findall(r"```" + re.escape(marker) + r"\n(.*?)\n```", markdown, re.S)
    if len(matches) != 1:
        raise ValueError("resource needs exactly one authored contract block")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate contract key")
            result[key] = value
        return result

    value = json.loads(
        matches[0],
        object_pairs_hook=pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")),
    )
    if not isinstance(value, Mapping):
        raise ValueError("contract must be an object")
    return value
