from __future__ import annotations

"""Optional HNSW vector index for the skill catalog.

The catalog remains exact-search by default.  This module deliberately keeps
HNSW as a replaceable acceleration layer: vectors and their authoritative
metadata stay in SQLite, while the hnswlib file is a rebuildable cache.
"""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Callable, Iterable, Sequence

from .text import cosine


class HNSWUnavailable(RuntimeError):
    """Raised when the optional hnswlib dependency is not installed."""


class HNSWMetadataError(RuntimeError):
    """Raised when a persisted index does not match the catalog."""


def _dependencies():
    try:
        import hnswlib  # type: ignore
        import numpy as np  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise HNSWUnavailable(
            "HNSW search requires the optional dependencies; install "
            "arex-skill-graph[hnsw] (hnswlib and numpy)"
        ) from exc
    return hnswlib, np


def inventory_signature(items: Iterable[tuple[str, Sequence[float]]]) -> str:
    """Return a stable signature for the indexed node/vector inventory."""
    digest = hashlib.sha256()
    for node_id, vector in sorted(items, key=lambda item: item[0]):
        digest.update(node_id.encode("utf-8"))
        digest.update(b"\0")
        digest.update(json.dumps([float(x) for x in vector], separators=(",", ":")).encode())
        digest.update(b"\n")
    return digest.hexdigest()


@dataclass(frozen=True)
class HNSWMetadata:
    dimension: int
    embedding_kind: str
    model_version: str
    node_ids: tuple[str, ...]
    inventory_signature: str
    space: str = "cosine"
    format_version: int = 1

    def to_dict(self) -> dict[str, object]:
        return {
            "format_version": self.format_version,
            "space": self.space,
            "dimension": self.dimension,
            "embedding_kind": self.embedding_kind,
            "model_version": self.model_version,
            "node_ids": list(self.node_ids),
            "inventory_signature": self.inventory_signature,
        }

    @classmethod
    def from_dict(cls, value: dict[str, object]) -> "HNSWMetadata":
        try:
            return cls(
                dimension=int(value["dimension"]),
                embedding_kind=str(value["embedding_kind"]),
                model_version=str(value["model_version"]),
                node_ids=tuple(str(x) for x in value["node_ids"]),
                inventory_signature=str(value["inventory_signature"]),
                space=str(value.get("space", "cosine")),
                format_version=int(value.get("format_version", 1)),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise HNSWMetadataError("invalid HNSW metadata") from exc


class HNSWIndex:
    """A persisted cosine HNSW index with deterministic filtered querying.

    ``node_ids[label]`` is the stable label mapping.  Labels are assigned from
    sorted node IDs, never from SQLite row order, so a rebuild is reproducible.
    The exact vectors are retained in memory after loading only to recompute
    scores/tie-breaks and to support an exact fallback for restrictive filters.
    """

    def __init__(
        self,
        path: str | Path,
        *,
        metadata: HNSWMetadata,
        vectors: dict[str, tuple[float, ...]],
        index: object,
    ) -> None:
        self.path = Path(path)
        self.metadata = metadata
        self.vectors = vectors
        self._index = index
        self._labels = {node_id: label for label, node_id in enumerate(metadata.node_ids)}

    @property
    def dimension(self) -> int:
        return self.metadata.dimension

    @classmethod
    def build(
        cls,
        path: str | Path,
        items: Iterable[tuple[str, Sequence[float]]],
        *,
        embedding_kind: str = "routing",
        model_version: str = "hash-v1",
        m: int = 16,
        ef_construction: int = 200,
        ef_search: int = 64,
    ) -> "HNSWIndex":
        hnswlib, np = _dependencies()
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        vectors = {str(node_id): tuple(float(x) for x in vector) for node_id, vector in items}
        if not vectors:
            raise ValueError("cannot build an HNSW index with no vectors")
        node_ids = tuple(sorted(vectors))
        dimensions = {len(vectors[node_id]) for node_id in node_ids}
        if len(dimensions) != 1 or not dimensions:
            raise ValueError("all indexed vectors must have the same non-zero dimension")
        dimension = dimensions.pop()
        if dimension <= 0:
            raise ValueError("vector dimension must be positive")
        if m <= 0 or ef_construction <= 0 or ef_search <= 0:
            raise ValueError("HNSW M and ef parameters must be positive")

        ann = hnswlib.Index(space="cosine", dim=dimension)
        ann.init_index(max_elements=len(node_ids), ef_construction=ef_construction, M=m)
        matrix = np.asarray([vectors[node_id] for node_id in node_ids], dtype=np.float32)
        ann.add_items(matrix, np.arange(len(node_ids), dtype=np.int64))
        ann.set_ef(max(ef_search, 1))
        ann.set_num_threads(1)
        ann.save_index(str(path))

        metadata = HNSWMetadata(
            dimension=dimension,
            embedding_kind=embedding_kind,
            model_version=model_version,
            node_ids=node_ids,
            inventory_signature=inventory_signature(vectors.items()),
        )
        metadata_path(path).write_text(
            json.dumps(metadata.to_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return cls(path, metadata=metadata, vectors=vectors, index=ann)

    @classmethod
    def load(
        cls,
        path: str | Path,
        *,
        expected_embedding_kind: str | None = None,
        expected_model_version: str | None = None,
        expected_items: Iterable[tuple[str, Sequence[float]]] | None = None,
        ef_search: int = 64,
    ) -> "HNSWIndex":
        hnswlib, _ = _dependencies()
        path = Path(path)
        metadata_file = metadata_path(path)
        if not path.exists() or not metadata_file.exists():
            raise FileNotFoundError(f"HNSW index and metadata are required: {path}")
        metadata = HNSWMetadata.from_dict(json.loads(metadata_file.read_text(encoding="utf-8")))
        if metadata.space != "cosine" or metadata.format_version != 1:
            raise HNSWMetadataError("unsupported HNSW index format or metric")
        if expected_embedding_kind is not None and metadata.embedding_kind != expected_embedding_kind:
            raise HNSWMetadataError("embedding kind does not match HNSW metadata")
        if expected_model_version is not None and metadata.model_version != expected_model_version:
            raise HNSWMetadataError("embedding model version does not match HNSW metadata")

        vectors: dict[str, tuple[float, ...]] = {}
        if expected_items is not None:
            vectors = {str(node_id): tuple(float(x) for x in vector) for node_id, vector in expected_items}
            if tuple(sorted(vectors)) != metadata.node_ids:
                raise HNSWMetadataError("indexed node inventory is stale")
            if inventory_signature(vectors.items()) != metadata.inventory_signature:
                raise HNSWMetadataError("indexed vectors are stale")
        else:
            # Querying without authoritative vectors is allowed, but filtered
            # exact fallback and score recomputation are unavailable.
            vectors = {}

        ann = hnswlib.Index(space=metadata.space, dim=metadata.dimension)
        ann.load_index(str(path), max_elements=len(metadata.node_ids))
        ann.set_ef(max(ef_search, 1))
        ann.set_num_threads(1)
        return cls(path, metadata=metadata, vectors=vectors, index=ann)

    def query(
        self,
        vector: Sequence[float],
        *,
        limit: int = 10,
        oversample: int = 4,
        allowed_node_ids: set[str] | None = None,
        exact_fallback: Callable[[], list[tuple[str, float]]] | None = None,
    ) -> list[tuple[str, float]]:
        if limit <= 0:
            return []
        if len(vector) != self.dimension:
            raise ValueError(f"query dimension {len(vector)} != index dimension {self.dimension}")
        _, np = _dependencies()
        count = min(len(self.metadata.node_ids), max(limit, limit * max(1, oversample)))
        labels, distances = self._index.knn_query(
            np.asarray([list(vector)], dtype=np.float32), k=count
        )
        candidates: list[tuple[str, float]] = []
        for label, distance in zip(labels[0], distances[0]):
            node_id = self.metadata.node_ids[int(label)]
            if allowed_node_ids is not None and node_id not in allowed_node_ids:
                continue
            if self.vectors:
                score = cosine(vector, self.vectors[node_id])
            else:
                score = 1.0 - float(distance)
            candidates.append((node_id, float(score)))
        candidates.sort(key=lambda item: (-item[1], item[0]))
        if len(candidates) < limit and exact_fallback is not None:
            seen = {node_id for node_id, _ in candidates}
            for node_id, score in exact_fallback():
                if node_id not in seen:
                    candidates.append((node_id, float(score)))
            candidates.sort(key=lambda item: (-item[1], item[0]))
        return candidates[:limit]


def metadata_path(index_path: str | Path) -> Path:
    path = Path(index_path)
    return path.with_name(path.name + ".meta.json")
