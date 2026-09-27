from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from .mining import (
    GitCommitMiner,
    GitHubClient,
    LocalMergeEpisodeExtractor,
    ReviewedWorkflowBuilder,
    RepositoryProfiler,
    PatternCandidateBuilder,
)
from .retrieval import SkillRetriever
from .schema import NodeType
from .store import CatalogStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arex-skill-graph",
        description="Mine, index, and retrieve evidence-grounded AREX Skills.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Initialize a catalog database.")
    init.add_argument("--db", type=Path, required=True)

    mine = subparsers.add_parser(
        "mine-git",
        help="Mine deterministic commit and Change Action candidates.",
    )
    mine.add_argument("--db", type=Path, required=True)
    mine.add_argument("--repo", type=Path, required=True)
    mine.add_argument("--repo-name", required=True)
    mine.add_argument("--limit", type=int, default=200)
    mine.add_argument("--since")

    search = subparsers.add_parser("search", help="Search the Skill graph.")
    search.add_argument("--db", type=Path, required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--repository")
    search.add_argument("--node-type", action="append", choices=[t.value for t in NodeType])
    search.add_argument("--top-k", type=int, default=12)
    search.add_argument("--seed-k", type=int, default=50)
    search.add_argument("--expand-hops", type=int, default=2)
    search.add_argument("--query-mode", choices=["solve", "explain", "audit"], default="solve")
    search.add_argument("--vector-backend", choices=["exact", "hnsw"], default="exact")
    search.add_argument("--hnsw-path", type=Path)
    search.add_argument("--hnsw-ef-search", type=int, default=64)
    search.add_argument("--hnsw-oversample", type=int, default=4)

    build_hnsw = subparsers.add_parser(
        "build-hnsw",
        help="Build an optional HNSW vector index; exact search remains the default.",
    )
    build_hnsw.add_argument("--db", type=Path, required=True)
    build_hnsw.add_argument("--output", type=Path, required=True)
    build_hnsw.add_argument("--embedding-kind", default="routing")
    build_hnsw.add_argument("--model-version", default="hash-v1")
    build_hnsw.add_argument("--m", type=int, default=16)
    build_hnsw.add_argument("--ef-construction", type=int, default=200)
    build_hnsw.add_argument("--ef-search", type=int, default=64)

    stats = subparsers.add_parser("stats", help="Print catalog statistics.")
    stats.add_argument("--db", type=Path, required=True)

    profile = subparsers.add_parser(
        "profile-git",
        help="Profile a repository history and estimate high-quality extraction candidates.",
    )
    profile.add_argument("--repo", type=Path, required=True)
    profile.add_argument("--repo-name", required=True)
    profile.add_argument("--ref", default="HEAD")
    profile.add_argument("--max-count", type=int)
    profile.add_argument("--example-limit", type=int, default=30)
    profile.add_argument("--output", type=Path)

    github_episode = subparsers.add_parser(
        "fetch-github-episode",
        help="Fetch and cache normalized GitHub Issue/PR episode metadata.",
    )
    github_episode.add_argument("--repo-name", required=True)
    github_episode.add_argument("--number", type=int, required=True)
    github_episode.add_argument("--cache", type=Path, required=True)
    github_episode.add_argument("--refresh", action="store_true")
    github_episode.add_argument("--no-commits", action="store_true")
    github_episode.add_argument("--no-files", action="store_true")
    github_episode.add_argument("--output", type=Path)

    local_episode = subparsers.add_parser(
        "extract-local-pr-episode",
        help="Recover a merged PR episode from a local Git merge commit.",
    )
    local_episode.add_argument("--repo", type=Path, required=True)
    local_episode.add_argument("--repo-name", required=True)
    local_episode.add_argument("--number", type=int, required=True)
    local_episode.add_argument("--ref", default="--all")
    local_episode.add_argument("--max-commits", type=int, default=500)
    local_episode.add_argument("--output", type=Path)

    local_episodes = subparsers.add_parser(
        "extract-local-pr-episodes",
        help="Recover selected merged PR episodes into a review directory.",
    )
    local_episodes.add_argument("--repo", type=Path, required=True)
    local_episodes.add_argument("--repo-name", required=True)
    local_episodes.add_argument("--number", type=int, action="append", required=True)
    local_episodes.add_argument("--ref", default="--all")
    local_episodes.add_argument("--max-commits", type=int, default=500)
    local_episodes.add_argument("--output-dir", type=Path, required=True)

    local_profile = subparsers.add_parser(
        "profile-local-pr-episodes",
        help="Batch-profile merged PR episodes from a local Git object graph.",
    )
    local_profile.add_argument("--repo", type=Path, required=True)
    local_profile.add_argument("--repo-name", required=True)
    local_profile.add_argument("--ref", default="--all")
    local_profile.add_argument("--limit", type=int)
    local_profile.add_argument("--max-commits", type=int, default=500)
    local_profile.add_argument("--candidate-limit", type=int, default=200)
    local_profile.add_argument("--family-candidate-limit", type=int, default=20)
    local_profile.add_argument("--min-score", type=float, default=0.0)
    local_profile.add_argument("--manifest-dir", type=Path)
    local_profile.add_argument("--output", type=Path)

    reviewed_workflows = subparsers.add_parser(
        "build-reviewed-workflows",
        help="Build provisional Workflow/WorkflowStep nodes from reviewed episode manifests.",
    )
    reviewed_workflows.add_argument("--db", type=Path, required=True)
    reviewed_workflows.add_argument("--manifest-root", type=Path, required=True)
    reviewed_workflows.add_argument("--labels", type=Path, required=True)

    patterns = subparsers.add_parser("build-pattern-candidates", help="Build provenance-preserving cross-repository Pattern candidates.")
    patterns.add_argument("--db", type=Path, required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "init":
        with CatalogStore(args.db) as store:
            store.initialize()
        print(json.dumps({"ok": True, "db": str(args.db)}, ensure_ascii=False))
        return 0

    if args.command == "mine-git":
        with CatalogStore(args.db) as store:
            store.initialize()
            report = GitCommitMiner(args.repo, args.repo_name).mine_to_store(
                store,
                limit=args.limit,
                since=args.since,
            )
        print(json.dumps(asdict(report), ensure_ascii=False, indent=2))
        return 0

    if args.command == "search":
        node_types = (
            [NodeType(value) for value in args.node_type] if args.node_type else None
        )
        with CatalogStore(args.db) as store:
            store.initialize()
            response = SkillRetriever(store).search(
                args.query,
                node_types=node_types,
                repository=args.repository,
                top_k=args.top_k,
                seed_k=args.seed_k,
                expand_hops=args.expand_hops,
                query_mode=args.query_mode,
                vector_backend=args.vector_backend,
                hnsw_path=args.hnsw_path,
                hnsw_ef_search=args.hnsw_ef_search,
                hnsw_oversample=args.hnsw_oversample,
            )
        payload = {
            "query": response.query,
            "seed_count": response.seed_count,
            "expanded_count": response.expanded_count,
            "unresolved": response.unresolved,
            "hits": [
                {
                    "id": hit.node.id,
                    "type": hit.node.node_type.value,
                    "title": hit.node.title,
                    "repository": hit.node.repository,
                    "score": hit.score,
                    "sources": hit.sources,
                    "trace": hit.trace,
                }
                for hit in response.hits
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command == "build-hnsw":
        with CatalogStore(args.db) as store:
            store.initialize()
            index = store.build_hnsw_index(
                args.output,
                embedding_kind=args.embedding_kind,
                model_version=args.model_version,
                m=args.m,
                ef_construction=args.ef_construction,
                ef_search=args.ef_search,
            )
        print(json.dumps({"index": str(args.output), "metadata": index.metadata.to_dict()}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "stats":
        with CatalogStore(args.db) as store:
            store.initialize()
            payload = store.stats()
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if args.command == "profile-git":
        payload = RepositoryProfiler(args.repo, args.repo_name).profile(
            ref=args.ref,
            max_count=args.max_count,
            example_limit=args.example_limit,
        ).to_dict()
        rendered = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(f"{rendered}\n", encoding="utf-8")
        print(rendered)
        return 0

    if args.command == "fetch-github-episode":
        episode = GitHubClient(args.cache).fetch_episode(
            args.repo_name,
            args.number,
            refresh=args.refresh,
            include_commits=not args.no_commits,
            include_files=not args.no_files,
        )
        rendered = json.dumps(episode.to_dict(), ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(f"{rendered}\n", encoding="utf-8")
        print(rendered)
        return 0

    if args.command == "extract-local-pr-episode":
        episode = LocalMergeEpisodeExtractor(
            args.repo,
            args.repo_name,
        ).extract(
            args.number,
            ref=args.ref,
            max_commits=args.max_commits,
        )
        rendered = json.dumps(episode.to_dict(), ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(f"{rendered}\n", encoding="utf-8")
        print(rendered)
        return 0

    if args.command == "extract-local-pr-episodes":
        extractor = LocalMergeEpisodeExtractor(args.repo, args.repo_name)
        args.output_dir.mkdir(parents=True, exist_ok=True)
        written: list[dict[str, object]] = []
        for number in args.number:
            episode = extractor.extract(
                number,
                ref=args.ref,
                max_commits=args.max_commits,
            )
            path = args.output_dir / f"pr-{number}.json"
            path.write_text(
                json.dumps(episode.to_dict(), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            written.append(
                {
                    "number": number,
                    "path": str(path),
                    "commits": len(episode.commits),
                    "files": len(episode.files),
                    "quality": episode.quality.tier,
                }
            )
        print(
            json.dumps(
                {"repository": args.repo_name, "written": written},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.command == "profile-local-pr-episodes":
        profile = LocalMergeEpisodeExtractor(
            args.repo,
            args.repo_name,
        ).profile(
            ref=args.ref,
            limit=args.limit,
            max_commits=args.max_commits,
            candidate_limit=args.candidate_limit,
            family_candidate_limit=args.family_candidate_limit,
            min_score=args.min_score,
            manifest_dir=args.manifest_dir,
        )
        rendered = json.dumps(profile.to_dict(), ensure_ascii=False, indent=2)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(f"{rendered}\n", encoding="utf-8")
        print(rendered)
        return 0

    if args.command == "build-reviewed-workflows":
        with CatalogStore(args.db) as store:
            store.initialize()
            report = ReviewedWorkflowBuilder(
                args.manifest_root,
                args.labels,
            ).build_to_store(store)
            stats = store.stats()
        print(
            json.dumps(
                {"report": report.to_dict(), "catalog": stats},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if args.command == "build-pattern-candidates":
        with CatalogStore(args.db) as store:
            store.initialize()
            report = PatternCandidateBuilder().build_to_store(store)
            stats = store.stats()
        print(
            json.dumps(
                {"report": report.to_dict(), "catalog": stats},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(f"unsupported command: {args.command}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
