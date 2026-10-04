"""Complete learning inputs are temporal dependencies, even when not cited as support."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass

from .action_contracts import SourceRecord, digest, strict, text


@dataclass(frozen=True)
class GenerationContext:
    source_corpus_sha256: str
    source_package_hashes: dict[str, str]
    sources: tuple[SourceRecord, ...]
    schema: str = "arex-generation-context-v1"

    def __post_init__(self):
        if self.schema != "arex-generation-context-v1" or not re.fullmatch(
            r"[0-9a-f]{64}", self.source_corpus_sha256
        ):
            raise ValueError("invalid generation context identity")
        if not isinstance(self.source_package_hashes, dict):
            raise ValueError("generation context package hashes must be an object")  # noqa: TRY004 -- JSON contract errors consistently use ValueError.
        for identifier, value in self.source_package_hashes.items():
            text(identifier, "generation context package ID")
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise ValueError("invalid generation context package hash")
        if not self.sources or len({s.id for s in self.sources}) != len(self.sources):
            raise ValueError("generation context needs unique source records")

    @classmethod
    def from_dict(cls, value):
        data = strict(value, cls)
        data["sources"] = tuple(SourceRecord.from_dict(s) for s in data.get("sources", []))
        return cls(**data)

    def to_dict(self):
        return json.loads(json.dumps(asdict(self)))

    def require_support(self, sources, package_hashes=None):
        by_id = {s.id: s for s in self.sources}
        if any(by_id.get(s.id) != s for s in sources):
            raise ValueError("generation context omits or changes a support source")
        if any(
            self.source_package_hashes.get(pid) != sha
            for pid, sha in (package_hashes or {}).items()
        ):
            raise ValueError("generation context omits or changes an upstream package")


def generation_context_for_packages(packages, *, source_corpus_sha256=None):
    """Include the complete discovery corpus and inherited authoring dependencies."""
    records, hashes = {}, {}
    for package in packages:
        context = package.generation_context
        candidates = (*package.sources, *(context.sources if context else ()))
        for source in candidates:
            if source.id in records and records[source.id] != source:
                raise ValueError("conflicting generation context source")
            records[source.id] = source
        upstream = list(context.source_package_hashes.items()) if context else []
        upstream.append((package.reference["skill_id"], package.reference["package_sha256"]))
        for pid, sha in upstream:
            if pid in hashes and hashes[pid] != sha:
                raise ValueError("conflicting generation context package")
            hashes[pid] = sha
    sources = tuple(records[k] for k in sorted(records))
    hashes = dict(sorted(hashes.items()))
    identity = source_corpus_sha256 or digest(
        {"source_package_hashes": hashes, "sources": [asdict(s) for s in sources]}
    )
    return GenerationContext(identity, hashes, sources)
