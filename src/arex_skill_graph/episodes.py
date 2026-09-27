"""Evidence-bearing change episode inputs for multi-level Skill extraction."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True, slots=True)
class ChangeEpisode:
    """A bounded before/after engineering change, not a Skill node.

    Workflows are extracted from this object because a workflow is the causal
    sequence of actions in one episode. Atomic Skills are the reusable
    primitives grounded in the same episode; they are not used as a substitute
    for the episode's control-flow evidence.
    """

    episode_id: str
    repository: str
    revision: str
    title: str
    before: str = ""
    after: str = ""
    diff: str = ""
    call_sites: tuple[str, ...] = ()
    tests: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "repository": self.repository,
            "revision": self.revision,
            "title": self.title,
            "before": self.before,
            "after": self.after,
            "diff": self.diff,
            "call_sites": list(self.call_sites),
            "tests": list(self.tests),
            "evidence_ids": list(self.evidence_ids),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ChangeEpisode":
        return cls(
            episode_id=str(value["episode_id"]),
            repository=str(value["repository"]),
            revision=str(value["revision"]),
            title=str(value.get("title", value["episode_id"])),
            before=str(value.get("before", "")),
            after=str(value.get("after", "")),
            diff=str(value.get("diff", "")),
            call_sites=tuple(str(x) for x in value.get("call_sites", ())),
            tests=tuple(str(x) for x in value.get("tests", ())),
            evidence_ids=tuple(str(x) for x in value.get("evidence_ids", ())),
            metadata=dict(value.get("metadata", {})),
        )
