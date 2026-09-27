from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Iterable, Iterator, Sequence

from .schema import (
    Edge,
    Node,
    NodeType,
    RelationType,
    canonical_json,
    validate_endpoint,
)
from .text import cosine, hash_embedding, tokenize


class CatalogStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA synchronous = NORMAL")
        self._hnsw_cache: dict[tuple[str, str, str, str, int], object] = {}

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "CatalogStore":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @contextmanager
    def transaction(self) -> Iterator[None]:
        try:
            self.connection.execute("BEGIN")
            yield
        except Exception:
            self.connection.rollback()
            raise
        else:
            self.connection.commit()

    def initialize(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY,
                node_type TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                repository TEXT,
                version TEXT NOT NULL,
                lifecycle TEXT NOT NULL,
                confidence REAL NOT NULL,
                facets_json TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                provenance_json TEXT NOT NULL,
                searchable_text TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS nodes_type_repository
                ON nodes(node_type, repository);

            CREATE VIRTUAL TABLE IF NOT EXISTS node_fts USING fts5(
                node_id UNINDEXED,
                title,
                summary,
                searchable_text,
                tokenize = 'unicode61 remove_diacritics 2'
            );

            CREATE TABLE IF NOT EXISTS edges (
                id TEXT PRIMARY KEY,
                source_id TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
                target_id TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
                relation TEXT NOT NULL,
                weight REAL NOT NULL,
                confidence REAL NOT NULL,
                evidence_json TEXT NOT NULL,
                provenance_json TEXT NOT NULL,
                condition_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS edges_source_relation
                ON edges(source_id, relation);
            CREATE INDEX IF NOT EXISTS edges_target_relation
                ON edges(target_id, relation);

            CREATE TABLE IF NOT EXISTS embeddings (
                node_id TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
                embedding_kind TEXT NOT NULL,
                dimensions INTEGER NOT NULL,
                vector_json TEXT NOT NULL,
                model_version TEXT NOT NULL,
                PRIMARY KEY(node_id, embedding_kind, model_version)
            );

            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value_json TEXT NOT NULL
            );

            -- Versioned skill governance is persisted separately from catalog nodes.
            -- The JSON payload keeps the registry forward-compatible while the
            -- event tables provide an append-only audit trail.
            CREATE TABLE IF NOT EXISTS skill_versions (
                skill_id TEXT PRIMARY KEY,
                canonical_id TEXT NOT NULL,
                level TEXT NOT NULL,
                version INTEGER NOT NULL,
                status TEXT NOT NULL,
                skill_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS skill_versions_canonical
                ON skill_versions(canonical_id, version);

            CREATE TABLE IF NOT EXISTS skill_aliases (
                alias_id TEXT PRIMARY KEY,
                canonical_id TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS skill_lifecycle_events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                occurred_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS skill_lifecycle_events_skill
                ON skill_lifecycle_events(skill_id, event_id);

            CREATE TABLE IF NOT EXISTS skill_usage_events (
                event_id TEXT PRIMARY KEY,
                skill_id TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS skill_failure_incidents (
                incident_id TEXT PRIMARY KEY,
                skill_id TEXT NOT NULL,
                occurred_at TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS skill_dedup_proposals (
                proposal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id TEXT NOT NULL,
                peer_id TEXT NOT NULL,
                decision TEXT NOT NULL,
                confidence REAL NOT NULL,
                reviewer TEXT NOT NULL,
                rationale TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.connection.commit()

    # --- Persistent skill lifecycle registry ---------------------------------
    # These methods intentionally store LLM proposals verbatim.  The catalog
    # never derives semantic equivalence from a score or a threshold.
    def persist_skill_record(self, skill) -> None:
        payload = skill.to_json()
        self.connection.execute(
            """INSERT INTO skill_versions(
                skill_id, canonical_id, level, version, status, skill_json, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(skill_id) DO UPDATE SET
                canonical_id=excluded.canonical_id, level=excluded.level,
                version=excluded.version, status=excluded.status,
                skill_json=excluded.skill_json, updated_at=excluded.updated_at
            """,
            (skill.skill_id, skill.canonical_id or skill.skill_id, skill.level.value,
             skill.version, skill.status.value, canonical_json(payload), skill.updated_at),
        )
        self.connection.executemany(
            "INSERT OR REPLACE INTO skill_aliases(alias_id, canonical_id) VALUES (?, ?)",
            [(alias, skill.canonical_id or skill.skill_id) for alias in skill.aliases],
        )

    def record_skill_lifecycle_event(self, skill_id: str, event_type: str, payload, occurred_at: str) -> None:
        payload_json = canonical_json(payload)
        self.connection.execute(
            "INSERT INTO skill_lifecycle_events(skill_id, event_type, payload_json, occurred_at) "
            "SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM skill_lifecycle_events "
            "WHERE skill_id = ? AND event_type = ? AND payload_json = ?)",
            (skill_id, event_type, payload_json, occurred_at,
             skill_id, event_type, payload_json),
        )

    def record_usage_event(self, event) -> None:
        self.connection.execute(
            "INSERT OR IGNORE INTO skill_usage_events(event_id, skill_id, occurred_at, payload_json) VALUES (?, ?, ?, ?)",
            (event.event_id, event.skill_id, event.occurred_at, canonical_json({
                "event_id": event.event_id, "skill_id": event.skill_id,
                "skill_version": event.skill_version, "task_id": event.task_id,
                "result": event.result.value,
                "failure_kind": event.failure_kind.value if event.failure_kind else None,
                "independent_context_id": event.independent_context_id,
                "validation_passed": event.validation_passed, "token_cost": event.token_cost,
                "notes": event.notes, "occurred_at": event.occurred_at,
            })),
        )

    def record_failure_incident(self, incident) -> None:
        self.connection.execute(
            "INSERT OR IGNORE INTO skill_failure_incidents(incident_id, skill_id, occurred_at, payload_json) VALUES (?, ?, ?, ?)",
            (incident.incident_id, incident.skill_id, incident.occurred_at, canonical_json({
                "incident_id": incident.incident_id, "skill_id": incident.skill_id,
                "task_id": incident.task_id, "kind": incident.kind.value,
                "independent_context_id": incident.independent_context_id,
                "severity": incident.severity, "evidence_ids": list(incident.evidence_ids),
                "root_cause": incident.root_cause,
                "correction_candidate_id": incident.correction_candidate_id,
                "occurred_at": incident.occurred_at,
            })),
        )

    def record_dedup_proposal(self, proposal) -> None:
        self.connection.execute(
            """INSERT INTO skill_dedup_proposals(
                candidate_id, peer_id, decision, confidence, reviewer, rationale, payload_json
            ) SELECT ?, ?, ?, ?, ?, ?, ? WHERE NOT EXISTS (
                SELECT 1 FROM skill_dedup_proposals WHERE candidate_id = ? AND peer_id = ?
                AND decision = ? AND rationale = ? AND reviewer = ?
            )""",
            (proposal.candidate_id, proposal.peer_id, proposal.decision.value,
             proposal.confidence, proposal.reviewer, proposal.rationale,
             canonical_json({"evidence_ids": list(proposal.evidence_ids),
                             "merged_payload": proposal.merged_payload}),
             proposal.candidate_id, proposal.peer_id, proposal.decision.value,
             proposal.rationale, proposal.reviewer),
        )

    def persist_lifecycle_manager(self, manager) -> None:
        """Durably snapshot a LifecycleManager and append its audit events."""
        with self.transaction():
            for skill in manager.skills.values():
                self.persist_skill_record(skill)
            for event in manager.usage_events:
                self.record_usage_event(event)
            for incident in manager.incidents:
                self.record_failure_incident(incident)
            for proposal in getattr(manager, "dedup_proposals", ()):
                self.record_dedup_proposal(proposal)
            for relation in manager.relations:
                self.record_skill_lifecycle_event(
                    relation.get("source", ""), "relation", relation,
                    relation.get("occurred_at") or datetime.now(timezone.utc).isoformat(),
                )                # ``contains`` is the durable projection of the lifecycle
                # manager's abstract skill tree. Other lifecycle relations
                # remain audit events and are not materialized as graph edges.
                if relation.get("relation") == RelationType.CONTAINS.value:
                    source_id = str(relation.get("source", ""))
                    target_id = str(relation.get("target", ""))
                    if not source_id or not target_id:
                        raise ValueError("contains relation requires source and target")
                    self.upsert_edge(
                        Edge.create(
                            source_id,
                            target_id,
                            RelationType.CONTAINS,
                            confidence=float(relation.get("confidence", 1.0)),
                            evidence_ids=tuple(relation.get("evidence_ids", ())),
                            provenance={
                                "source": "lifecycle_manager",
                                "event": "attach_parent",
                            },
                        )
                    )
            self.sync_lifecycle_graph(manager)

    def sync_lifecycle_graph(self, manager) -> None:
        """Reconcile the current ``Pattern -> Workflow -> Atomic`` projection.

        Lifecycle relations are append-only audit data, but ``edges`` is the
        serving projection used by retrieval. Rebuilding only the current
        ``parent_ids`` prevents detached, quarantined, retired, merged, or
        superseded skills from remaining reachable after feedback updates.
        """
        terminal = {"quarantined", "deprecated", "retired", "merged", "superseded"}
        current: set[tuple[str, str]] = set()
        for child in manager.skills.values():
            if child.status.value in terminal:
                continue
            for parent_id in child.parent_ids:
                parent = manager.skills.get(parent_id)
                if parent is None or parent.status.value in terminal:
                    continue
                current.add((parent_id, child.skill_id))

        rows = self.connection.execute(
            "SELECT id, source_id, target_id FROM edges WHERE relation = ?",
            (RelationType.CONTAINS.value,),
        ).fetchall()
        for row in rows:
            if (row["source_id"], row["target_id"]) not in current:
                self.connection.execute("DELETE FROM edges WHERE id = ?", (row["id"],))

        for parent_id, child_id in sorted(current):
            self.upsert_edge(
                Edge.create(
                    parent_id,
                    child_id,
                    RelationType.CONTAINS,
                    provenance={"source": "lifecycle_manager", "projection": "current"},
                )
            )

    def load_skill_json(self) -> list[dict]:
        rows = self.connection.execute(
            "SELECT skill_json FROM skill_versions ORDER BY canonical_id, version, skill_id"
        ).fetchall()
        return [json.loads(row["skill_json"]) for row in rows]

    def upsert_node(
        self,
        node: Node,
        *,
        embed: bool = True,
        embedding_kind: str = "routing",
        model_version: str = "hash-v1",
    ) -> None:
        searchable_text = node.searchable_text()
        self.connection.execute(
            """
            INSERT INTO nodes(
                id, node_type, title, summary, repository, version, lifecycle,
                confidence, facets_json, payload_json, provenance_json,
                searchable_text, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                node_type = excluded.node_type,
                title = excluded.title,
                summary = excluded.summary,
                repository = excluded.repository,
                version = excluded.version,
                lifecycle = excluded.lifecycle,
                confidence = excluded.confidence,
                facets_json = excluded.facets_json,
                payload_json = excluded.payload_json,
                provenance_json = excluded.provenance_json,
                searchable_text = excluded.searchable_text,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                node.id,
                node.node_type.value,
                node.title,
                node.summary,
                node.repository,
                node.version,
                node.lifecycle,
                node.confidence,
                canonical_json(node.facets),
                canonical_json(node.payload),
                canonical_json(node.provenance),
                searchable_text,
            ),
        )
        self.connection.execute("DELETE FROM node_fts WHERE node_id = ?", (node.id,))
        self.connection.execute(
            """
            INSERT INTO node_fts(node_id, title, summary, searchable_text)
            VALUES (?, ?, ?, ?)
            """,
            (node.id, node.title, node.summary, searchable_text),
        )
        if embed:
            self.upsert_embedding(
                node.id,
                hash_embedding(searchable_text),
                embedding_kind=embedding_kind,
                model_version=model_version,
            )

    def upsert_nodes(self, nodes: Iterable[Node], *, embed: bool = True) -> None:
        for node in nodes:
            self.upsert_node(node, embed=embed)

    def get_node(self, node_id: str) -> Node | None:
        row = self.connection.execute(
            "SELECT * FROM nodes WHERE id = ?", (node_id,)
        ).fetchone()
        return _row_to_node(row) if row else None

    def list_nodes(
        self,
        *,
        node_types: Sequence[NodeType] | None = None,
        repository: str | None = None,
        limit: int | None = None,
    ) -> list[Node]:
        clauses: list[str] = []
        values: list[object] = []
        if node_types:
            placeholders = ",".join("?" for _ in node_types)
            clauses.append(f"node_type IN ({placeholders})")
            values.extend(node_type.value for node_type in node_types)
        if repository:
            clauses.append("repository = ?")
            values.append(repository)
        where = f" WHERE {' AND '.join(clauses)}" if clauses else ""
        limit_sql = " LIMIT ?" if limit is not None else ""
        if limit is not None:
            values.append(limit)
        rows = self.connection.execute(
            f"SELECT * FROM nodes{where} ORDER BY id{limit_sql}", values
        ).fetchall()
        return [_row_to_node(row) for row in rows]

    def upsert_edge(self, edge: Edge) -> None:
        source = self.get_node(edge.source_id)
        target = self.get_node(edge.target_id)
        if source is None or target is None:
            raise KeyError(
                f"edge endpoints must exist: source={edge.source_id!r}, "
                f"target={edge.target_id!r}"
            )
        validate_endpoint(edge, source.node_type, target.node_type)
        self.connection.execute(
            """
            INSERT INTO edges(
                id, source_id, target_id, relation, weight, confidence,
                evidence_json, provenance_json, condition_json, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
                weight = excluded.weight,
                confidence = excluded.confidence,
                evidence_json = excluded.evidence_json,
                provenance_json = excluded.provenance_json,
                condition_json = excluded.condition_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                edge.id,
                edge.source_id,
                edge.target_id,
                edge.relation.value,
                edge.weight,
                edge.confidence,
                canonical_json(edge.evidence_ids),
                canonical_json(edge.provenance),
                canonical_json(edge.condition),
            ),
        )

    def neighbors(
        self,
        node_id: str,
        *,
        relations: Sequence[RelationType] | None = None,
        direction: str = "both",
    ) -> list[tuple[Edge, Node, str]]:
        if direction not in {"out", "in", "both"}:
            raise ValueError("direction must be out, in, or both")
        relation_clause = ""
        relation_values: list[object] = []
        if relations:
            placeholders = ",".join("?" for _ in relations)
            relation_clause = f" AND e.relation IN ({placeholders})"
            relation_values.extend(relation.value for relation in relations)

        result: list[tuple[Edge, Node, str]] = []
        if direction in {"out", "both"}:
            rows = self.connection.execute(
                f"""
                SELECT
                    e.id AS edge_id,
                    e.source_id AS edge_source_id,
                    e.target_id AS edge_target_id,
                    e.relation AS edge_relation,
                    e.weight AS edge_weight,
                    e.confidence AS edge_confidence,
                    e.evidence_json AS edge_evidence_json,
                    e.provenance_json AS edge_provenance_json,
                    e.condition_json AS edge_condition_json,
                    n.*
                FROM edges e
                JOIN nodes n ON n.id = e.target_id
                WHERE e.source_id = ?{relation_clause}
                """,
                [node_id, *relation_values],
            ).fetchall()
            result.extend((_row_to_edge(row), _row_to_node(row), "out") for row in rows)
        if direction in {"in", "both"}:
            rows = self.connection.execute(
                f"""
                SELECT
                    e.id AS edge_id,
                    e.source_id AS edge_source_id,
                    e.target_id AS edge_target_id,
                    e.relation AS edge_relation,
                    e.weight AS edge_weight,
                    e.confidence AS edge_confidence,
                    e.evidence_json AS edge_evidence_json,
                    e.provenance_json AS edge_provenance_json,
                    e.condition_json AS edge_condition_json,
                    n.*
                FROM edges e
                JOIN nodes n ON n.id = e.source_id
                WHERE e.target_id = ?{relation_clause}
                """,
                [node_id, *relation_values],
            ).fetchall()
            result.extend((_row_to_edge(row), _row_to_node(row), "in") for row in rows)
        return result

    def search_lexical(
        self,
        query: str,
        *,
        node_types: Sequence[NodeType] | None = None,
        repository: str | None = None,
        limit: int = 50,
    ) -> list[tuple[Node, float]]:
        tokens = tokenize(query)
        if not tokens:
            return []
        fts_query = " OR ".join(f'"{token}"' for token in tokens)
        clauses = ["node_fts MATCH ?"]
        values: list[object] = [fts_query]
        if node_types:
            placeholders = ",".join("?" for _ in node_types)
            clauses.append(f"n.node_type IN ({placeholders})")
            values.extend(node_type.value for node_type in node_types)
        if repository:
            clauses.append("n.repository = ?")
            values.append(repository)
        values.append(limit)
        rows = self.connection.execute(
            f"""
            SELECT n.*, bm25(node_fts, 2.0, 1.0, 0.5) AS lexical_rank
            FROM node_fts
            JOIN nodes n ON n.id = node_fts.node_id
            WHERE {' AND '.join(clauses)}
            ORDER BY lexical_rank
            LIMIT ?
            """,
            values,
        ).fetchall()
        return [(_row_to_node(row), -float(row["lexical_rank"])) for row in rows]

    def upsert_embedding(
        self,
        node_id: str,
        vector: Sequence[float],
        *,
        embedding_kind: str,
        model_version: str,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO embeddings(
                node_id, embedding_kind, dimensions, vector_json, model_version
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(node_id, embedding_kind, model_version) DO UPDATE SET
                dimensions = excluded.dimensions,
                vector_json = excluded.vector_json
            """,
            (
                node_id,
                embedding_kind,
                len(vector),
                canonical_json(list(vector)),
                model_version,
            ),
        )

    def embedding_items(
        self,
        *,
        embedding_kind: str = "routing",
        model_version: str = "hash-v1",
        node_types: Sequence[NodeType] | None = None,
        repository: str | None = None,
    ) -> list[tuple[str, tuple[float, ...]]]:
        """Return authoritative vectors in stable node-id order."""
        clauses = ["e.embedding_kind = ?", "e.model_version = ?"]
        values: list[object] = [embedding_kind, model_version]
        if node_types:
            placeholders = ",".join("?" for _ in node_types)
            clauses.append(f"n.node_type IN ({placeholders})")
            values.extend(node_type.value for node_type in node_types)
        if repository:
            clauses.append("n.repository = ?")
            values.append(repository)
        rows = self.connection.execute(
            f"""
            SELECT e.node_id, e.vector_json
            FROM embeddings e
            JOIN nodes n ON n.id = e.node_id
            WHERE {" AND ".join(clauses)}
            ORDER BY e.node_id
            """,
            values,
        ).fetchall()
        return [
            (row["node_id"], tuple(float(x) for x in json.loads(row["vector_json"])))
            for row in rows
        ]

    def build_hnsw_index(
        self,
        path: str | Path,
        *,
        embedding_kind: str = "routing",
        model_version: str = "hash-v1",
        m: int = 16,
        ef_construction: int = 200,
        ef_search: int = 64,
    ):
        """Build the optional HNSW cache from authoritative SQLite vectors."""
        from .hnsw import HNSWIndex

        return HNSWIndex.build(
            path,
            self.embedding_items(embedding_kind=embedding_kind, model_version=model_version),
            embedding_kind=embedding_kind,
            model_version=model_version,
            m=m,
            ef_construction=ef_construction,
            ef_search=ef_search,
        )

    def search_vector(
        self,
        query: str,
        *,
        node_types: Sequence[NodeType] | None = None,
        repository: str | None = None,
        embedding_kind: str = "routing",
        model_version: str = "hash-v1",
        limit: int = 50,
        vector_backend: str = "exact",
        hnsw_path: str | Path | None = None,
        hnsw_ef_search: int = 64,
        hnsw_oversample: int = 4,
    ) -> list[tuple[Node, float]]:
        if limit <= 0:
            return []
        if vector_backend not in {"exact", "hnsw"}:
            raise ValueError("vector_backend must be exact or hnsw")
        query_vector = hash_embedding(query)
        all_items = self.embedding_items(
            embedding_kind=embedding_kind, model_version=model_version
        )
        allowed_ids: set[str] | None = None
        if node_types or repository:
            allowed_ids = {
                node.id for node in self.list_nodes(node_types=node_types, repository=repository)
            }

        def exact_scores() -> list[tuple[str, float]]:
            scored = [
                (node_id, cosine(query_vector, vector))
                for node_id, vector in all_items
                if allowed_ids is None or node_id in allowed_ids
            ]
            scored.sort(key=lambda item: (-item[1], item[0]))
            return scored

        if vector_backend == "exact":
            scores = exact_scores()[:limit]
        else:
            if hnsw_path is None:
                raise ValueError("hnsw_path is required when vector_backend=hnsw")
            from .hnsw import HNSWIndex

            # Keep the native index resident across searches. The inventory
            # signature is part of the key, so a catalog update naturally
            # invalidates the cache and reloads (or raises on a stale file).
            from .hnsw import inventory_signature

            cache_key = (
                str(Path(hnsw_path).resolve()),
                embedding_kind,
                model_version,
                inventory_signature(all_items),
                hnsw_ef_search,
            )
            index = self._hnsw_cache.get(cache_key)
            if index is None:
                index = HNSWIndex.load(
                    hnsw_path,
                    expected_embedding_kind=embedding_kind,
                    expected_model_version=model_version,
                    expected_items=all_items,
                    ef_search=hnsw_ef_search,
                )
                self._hnsw_cache[cache_key] = index
            scores = index.query(
                query_vector,
                limit=limit,
                oversample=hnsw_oversample,
                allowed_node_ids=allowed_ids,
                exact_fallback=exact_scores,
            )
        nodes = {node.id: node for node in self.list_nodes()}
        return [(nodes[node_id], score) for node_id, score in scores if node_id in nodes]

    def stats(self) -> dict[str, object]:
        nodes = self.connection.execute(
            "SELECT node_type, COUNT(*) AS count FROM nodes GROUP BY node_type"
        ).fetchall()
        edges = self.connection.execute(
            "SELECT relation, COUNT(*) AS count FROM edges GROUP BY relation"
        ).fetchall()
        return {
            "nodes": {row["node_type"]: row["count"] for row in nodes},
            "edges": {row["relation"]: row["count"] for row in edges},
            "embeddings": self.connection.execute(
                "SELECT COUNT(*) FROM embeddings"
            ).fetchone()[0],
        }


def _row_to_node(row: sqlite3.Row) -> Node:
    return Node(
        id=row["id"],
        node_type=NodeType(row["node_type"]),
        title=row["title"],
        summary=row["summary"],
        repository=row["repository"],
        version=row["version"],
        lifecycle=row["lifecycle"],
        confidence=float(row["confidence"]),
        facets=json.loads(row["facets_json"]),
        payload=json.loads(row["payload_json"]),
        provenance=json.loads(row["provenance_json"]),
    )


def _row_to_edge(row: sqlite3.Row) -> Edge:
    return Edge(
        id=row["edge_id"],
        source_id=row["edge_source_id"],
        target_id=row["edge_target_id"],
        relation=RelationType(row["edge_relation"]),
        weight=float(row["edge_weight"]),
        confidence=float(row["edge_confidence"]),
        evidence_ids=tuple(json.loads(row["edge_evidence_json"])),
        provenance=json.loads(row["edge_provenance_json"]),
        condition=json.loads(row["edge_condition_json"]),
    )


