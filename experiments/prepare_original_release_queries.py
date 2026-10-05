#!/usr/bin/env python3
"""Prepare original historical queries using a uniform pre-input published source policy."""

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

from packaging.version import InvalidVersion, Version

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from arex_skill_graph.action_contracts import utc
from arex_skill_graph.historical_isolation import HistoricalIsolation
from arex_skill_graph.history_census import fingerprint, redact_history, write_json
from arex_skill_graph.published_history_query import prepare_published_query


def select_source(registry, package_name, input_at):
    """Select the highest stable version with one public sdist strictly before input."""
    eligible = []
    for version, artifacts in registry["releases"].items():
        try:
            parsed = Version(version)
        except InvalidVersion:
            continue
        if parsed.is_prerelease or parsed.is_devrelease or parsed.local:
            continue
        sdists = [
            row
            for row in artifacts
            if row["packagetype"] == "sdist" and utc(row["upload_time_iso_8601"]) < utc(input_at)
        ]
        if sdists:
            eligible.append((parsed, version, sdists))
    if not eligible:
        raise ValueError("no published stable source distribution strictly before input")
    _, version, sdists = max(eligible, key=lambda row: row[0])
    if len(sdists) != 1:
        raise ValueError("latest eligible stable version has ambiguous source archives")
    source = sdists[0]
    url = urlsplit(source["url"])
    filename = source["filename"]
    if (
        url.scheme != "https"
        or url.hostname != "files.pythonhosted.org"
        or url.username
        or url.password
        or url.query
        or url.fragment
        or Path(filename).name != filename
        or "\\" in filename
        or not filename.endswith(".tar.gz")
        or not re.fullmatch(r"[0-9a-f]{64}", source["digests"]["sha256"])
        or type(source["size"]) is not int
        or not 0 < source["size"] <= 64 * 1024**2
    ):
        raise ValueError("published source identity is unsafe or unsupported")
    return {
        "name": package_name,
        "version": version,
        "urls": [
            {
                key: source[key]
                for key in (
                    "filename",
                    "packagetype",
                    "url",
                    "upload_time_iso_8601",
                    "digests",
                    "size",
                )
            }
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("recovery", "project-map", "causal-isolation", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--training-cutoff", default="2021-01-01T00:00:00Z")
    parser.add_argument("--main-cutoff", default="2024-01-01T00:00:00Z")
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        raise ValueError("preserve existing published-query preparation; use a new version")
    recovery = json.loads(args.recovery.read_text())
    if (
        recovery.get("schema") != "original-public-history-query-recovery-v1"
        or recovery.get("later_comments_and_repairs_persisted") is not False
        or recovery["selected_targets"] != len(recovery["results"])
    ):
        raise ValueError("published queries require a complete original-input recovery receipt")
    project_map = json.loads(args.project_map.read_text())
    if any(
        not re.fullmatch(r"[A-Za-z0-9]+(?:[-_.][A-Za-z0-9]+)*", v) for v in project_map.values()
    ):
        raise ValueError("invalid configured public package name")
    isolation = HistoricalIsolation.load(args.causal_isolation)
    args.output_dir.mkdir(parents=True)
    policy = {
        "schema": "original-query-source-selection-policy-v1",
        "policy": "highest stable package version with one sdist strictly before original input",
        "prerelease_development_and_local_versions_excluded": True,
        "current_yank_flags_used": False,
        "historical_gold_outcomes_used_for_source_selection": False,
        "query_input_time_is_original_event_time": True,
        "synthetic_Git_commit_is_not_backdated": True,
        "project_map_sha256": fingerprint(project_map),
        "causal_isolation_sha256": isolation.sha256,
    }
    write_json(args.output_dir / "source-selection-policy.json", policy)
    registries, registry_hashes, queries, audits = {}, {}, [], []
    for row in recovery["results"]:
        qid = row["query_issue"]
        if row["status"] != "original_input_qualified":
            audits.append({"query_id": qid, "status": "original_input_unrecovered"})
            continue
        repository = qid.rsplit(":", 1)[0]
        case = qid.replace("/", "__").replace(":", "-")
        try:
            name = project_map[repository]
            if name not in registries:
                with urllib.request.urlopen(
                    "https://pypi.org/pypi/" + name + "/json", timeout=60
                ) as stream:
                    raw = stream.read(32 * 1024**2 + 1)
                if len(raw) > 32 * 1024**2:
                    raise ValueError("public registry metadata exceeds preparation bound")
                registries[name] = json.loads(raw)
                registry_hashes[name] = hashlib.sha256(raw).hexdigest()
            metadata = select_source(registries[name], name, row["input_available_at"])
            root = args.output_dir / "cases" / case
            write_json(root / "registry-metadata.json", metadata)
            source = metadata["urls"][0]
            archive = args.output_dir / "archives" / source["filename"]
            if not archive.exists():
                with urllib.request.urlopen(source["url"], timeout=60) as stream:
                    data = stream.read(source["size"] + 1)
                if (
                    len(data) != source["size"]
                    or hashlib.sha256(data).hexdigest() != source["digests"]["sha256"]
                ):
                    raise ValueError("downloaded source bytes differ from public registry identity")
                archive.parent.mkdir(exist_ok=True)
                archive.write_bytes(data)
            authority = [s for s in isolation.sources if s.bug_cluster_id == qid]
            if len(authority) != 1:
                raise ValueError("query needs one authoritative historical repair identity")
            task, audit = prepare_published_query(
                row["input_path"],
                row["qualification_path"],
                root / "registry-metadata.json",
                archive,
                root / "public-base",
            )
            queries.append(
                {
                    "task": task.to_dict(),
                    "bug_cluster_id": qid,
                    "fix_id": authority[0].fix_id,
                    "aliases": list(authority[0].aliases),
                    "copied_from": list(authority[0].copied_from),
                    "exposed": False,
                }
            )
            write_json(root / "task.json", task.to_dict())
            write_json(root / "source-preparation-audit.json", audit)
            audits.append(
                {
                    "query_id": qid,
                    "status": "registered_original_published_query",
                    "input_available_at": task.input_available_at,
                    "source_version": metadata["version"],
                    "source_upload_at": source["upload_time_iso_8601"],
                    "source_archive_sha256": audit["archive_sha256"],
                    "base_commit": task.base_commit,
                    "synthetic_commit_is_not_backdated": True,
                    "historical_causal_controls_completed": False,
                }
            )
        except (ValueError, KeyError, TypeError, OSError) as error:
            audits.append(
                {
                    "query_id": qid,
                    "status": "published_source_or_input_gap",
                    "failure_type": type(error).__name__,
                    "reason": redact_history(str(error)),
                }
            )
        write_json(
            args.output_dir / "progress.json",
            {
                "status": "running",
                "registered_queries": len(queries),
                "completed_targets": len(audits),
                "selected_targets": len(recovery["results"]),
                "actual_LLM_calls": 0,
                "new_utility_labels": 0,
                "formal_SWE_runs": 0,
            },
        )
    write_json(args.output_dir / "queries.json", queries)
    write_json(
        args.output_dir / "query-register.json",
        {
            "schema": "historical-public-ranker-query-register-v1",
            "audits": audits,
            "queries_sha256": fingerprint(queries),
            "input_recovery_sha256": fingerprint(recovery),
            "causal_isolation_sha256": isolation.sha256,
            "source_selection_policy_sha256": fingerprint(policy),
            "registry_response_sha256": registry_hashes,
            "training_cutoff": args.training_cutoff,
            "main_cutoff": args.main_cutoff,
            "selected_targets": len(recovery["results"]),
            "query_count": len(queries),
            "historical_causal_controls_completed": False,
            "model_calls": 0,
            "new_utility_labels": 0,
            "formal_SWE_queries": 0,
            "prepared_at_utc": datetime.now(UTC).isoformat(),
        },
    )
    print(
        json.dumps(
            {
                "original_published_queries": len(queries),
                "selected_targets": len(audits),
                "actual_LLM_calls": 0,
                "causal_control_acceptance": False,
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
