"""Conservative identity components; connected records count as one support.

This closes declared aliases, copies, issue clusters and shared repair artifacts.
It does not establish semantic independence or a common repair mechanism; native
qualification and independent causal review remain separate requirements.
"""

from __future__ import annotations

from collections.abc import Iterable

from .action_contracts import SourceRecord


def independent_source_components(
    sources: Iterable[SourceRecord],
) -> tuple[tuple[SourceRecord, ...], ...]:
    """Keep redundant evidence without letting it increase independent support."""
    records = {}
    for source in sources:
        if source.id in records and records[source.id] != source:
            raise ValueError("conflicting source identity in independent support")
        records[source.id] = source
    parents = {identifier: identifier for identifier in records}

    def root(identifier):
        while parents[identifier] != identifier:
            parents[identifier] = parents[parents[identifier]]
            identifier = parents[identifier]
        return identifier

    owners = {}
    for identifier, source in sorted(records.items()):
        identities = {
            source.id,
            source.bug_cluster_id,
            source.fix_id,
            source.revision,
            *getattr(source, "aliases", ()),
            *getattr(source, "copied_from", ()),
        }
        for identity in identities:
            if identity in owners:
                left, right = root(identifier), root(owners[identity])
                parents[max(left, right)] = min(left, right)
            else:
                owners[identity] = identifier
    components = {}
    for identifier in sorted(records):
        components.setdefault(root(identifier), []).append(records[identifier])
    return tuple(tuple(components[key]) for key in sorted(components))
