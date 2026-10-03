#!/usr/bin/env python3
"""Audit the frozen survey offline, optionally rehashing its external raw cache."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

ORIGINAL_COUNTS = {
    "astropy/astropy": (95, 6, 22),
    "django/django": (850, 114, 231),
    "matplotlib/matplotlib": (184, 23, 34),
    "mwaskom/seaborn": (22, 4, 2),
    "pallets/flask": (11, 3, 1),
    "psf/requests": (44, 6, 8),
    "pydata/xarray": (110, 5, 22),
    "pylint-dev/pylint": (57, 6, 10),
    "pytest-dev/pytest": (119, 17, 19),
    "scikit-learn/scikit-learn": (229, 23, 32),
    "sphinx-doc/sphinx": (187, 16, 44),
    "sympy/sympy": (386, 77, 75),
}

# Standard SPDX licenses actually used by this frozen source/peer shortlist.
# Custom and unrecognized cases require the separately stored file review.
SHORTLIST_OPEN_LICENSES = {
    "MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "MPL-2.0",
    "GPL-2.0", "GPL-3.0", "AGPL-3.0",
}


def load(root: Path, filename: str) -> dict:
    return json.loads((root / filename).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--analysis", default=Path("analysis"), type=Path)
    parser.add_argument("--cache", type=Path, help="External raw cache; never copied into the repository")
    args = parser.parse_args()
    output = args.data / "data-audit.json"
    snapshots = load(args.data, "dataset-snapshots.json")["datasets"]
    census = load(args.data, "benchmark-project-census.json")
    metadata_doc = load(args.data, "github-repositories.json")
    metadata = metadata_doc["projects"]
    activity_doc = load(args.data, "github-pr-activity.json")
    activity = activity_doc["projects"]
    selection = load(args.data, "project-selection.json")
    manual = load(args.data, "manual-license-decisions.json")["projects"]
    license_sources = load(args.data, "manual-license-sources.json")["projects"]
    source_groups = load(args.data, "similarity-groups.json")["groups"]
    rest = load(args.data, "rest-date-range-crosscheck.json")["results"]
    snapshot = date.fromisoformat(selection["snapshot_date"])
    require(metadata_doc["snapshot_date"] == activity_doc["snapshot_date"] == snapshot.isoformat(), "Mixed GitHub snapshots")
    require(activity_doc["query_contract"] == "single_inclusive_github_date_range_v1", "Invalid date query contract")
    start = (snapshot - timedelta(days=89)).isoformat()
    start365 = (snapshot - timedelta(days=364)).isoformat()
    end = (snapshot + timedelta(days=1)).isoformat()
    require(activity_doc["windows"] == {
        "start90_inclusive": start, "start365_inclusive": start365, "end_exclusive": end,
    }, "Invalid calendar windows")
    require(selection["criteria"]["PR_total_minimum"] == 1000
            and selection["criteria"]["PR_merged90_minimum"] == 20
            and selection["criteria"]["default_branch_commit_in_window"] == [start, end], "Invalid source thresholds")

    canonical = {}
    raw_resolution = {}
    for raw, observation in metadata.items():
        repository = observation["repository"]
        if repository:
            canonical[repository["nameWithOwner"]] = repository
            raw_resolution[raw.lower()] = repository["nameWithOwner"]
    require(all(metadata.get(raw, {}).get("resolved") for raw in census["projects"]), "Unresolved benchmark identity")
    union = set()
    inverse = defaultdict(dict)
    official_files = {}
    variant_counts = {}
    prefix_files = set()
    hashed_files = set()
    rehashed_files = set()
    for variant, record in census["variants"].items():
        label = variant.split("/", 1)[0]
        dataset = snapshots[label]
        require(record["dataset_id"] == dataset["dataset_id"] and record["revision"] == dataset["revision"], f"Revision mismatch: {variant}")
        index = {item["rfilename"]: item for item in dataset["files"]}
        projects = record["project_counts"]
        require(record["repositories"] == len(projects), f"Project count mismatch: {variant}")
        union.update(projects)
        current = {raw_resolution[raw.lower()] for raw in projects}
        variant_counts[variant] = {"raw_repository_identities": len(projects), "canonical_projects": len(current),
                                   "raw_rows": record["raw_rows"], "unique_tasks": record["unique_tasks"]}
        for raw, count in projects.items():
            inverse[raw][variant] = count
        if record["task_counts_not_computed"]:
            require(record["raw_rows"] is None and record["unique_tasks"] is None, f"Uncounted tasks labeled counted: {variant}")
            require(all(value is None for value in projects.values()), f"Partial task counts: {variant}")
        else:
            require(sum(projects.values()) == record["unique_tasks"] <= record["raw_rows"], f"Task count mismatch: {variant}")
            require(sum(item["raw_rows"] for item in record["files"]) == record["raw_rows"], f"Raw row sum mismatch: {variant}")
        for file in record["files"]:
            official = index[file["file"]]
            key = file["source_url"]
            require(key == f"https://huggingface.co/datasets/{dataset['dataset_id']}/resolve/{dataset['revision']}/{file['file']}", f"Unpinned file source: {variant}")
            require(file["bytes"] == official["size"], f"File size mismatch: {variant}")
            if key in official_files:
                continue
            official_files[key] = file
            expected_sha256 = (official.get("lfs") or {}).get("sha256")
            if file["full_content_hash_verified"]:
                hashed_files.add(key)
                if expected_sha256:
                    require(file["sha256"] == expected_sha256, f"Recorded LFS hash mismatch: {variant}")
                else:
                    require(file["integrity_verified_by"] == "official_git_blob_sha1", f"Unexpected integrity method: {variant}")
                if args.cache:
                    path = args.cache / label / dataset["revision"] / file["file"]
                    require(path.is_file(), f"Missing full cached file: {variant}/{file['file']}")
                    require(path.stat().st_size == file["bytes"], f"Cached file size mismatch: {variant}")
                    with path.open("rb") as stream:
                        digest = hashlib.file_digest(stream, "sha256").hexdigest()
                    require(digest == file["sha256"], f"Cached SHA256 mismatch: {variant}")
                    if not expected_sha256:
                        blob_digest = hashlib.sha1(f"blob {file['bytes']}\0".encode())
                        with path.open("rb") as stream:
                            for block in iter(lambda: stream.read(1024 * 1024), b""):
                                blob_digest.update(block)
                        require(blob_digest.hexdigest() == official["blobId"], f"Cached Git blob mismatch: {variant}")
                    rehashed_files.add(key)
            else:
                prefix_files.add(key)
                require(file["integrity_verified_by"] == "revision_pinned_official_file_index_and_http_root_identity", f"Unexpected partial method: {variant}")
                require(file["official_blob_id"] == official["blobId"] and file["official_lfs_sha256"] == expected_sha256, f"Prefix index mismatch: {variant}")
                stem = Path(file["file"]).stem.removesuffix("_dataset").replace("__", "/", 1)
                require(stem.lower() == file["repository_identity"].lower(), f"Prefix identity mismatch: {variant}")
                require(file["repository_identity"] in projects and 0 < file["prefix_bytes_observed"] <= 4096, f"Invalid prefix observation: {variant}")
                require(re.fullmatch(r"[0-9a-f]{64}", file["prefix_sha256"]) is not None, f"Invalid prefix hash: {variant}")
    require(dict(inverse) == census["projects"], "Census inverse membership mismatch")
    require(len(union) == census["unique_raw_repositories"] == len(census["projects"]), "Raw union mismatch")
    benchmark_names = {raw_resolution[raw.lower()] for raw in union}
    require(benchmark_names == set(selection["projects"]), "Pool-external project or missing benchmark project")
    require(len(benchmark_names) == selection["canonical_benchmark_projects"], "Canonical union mismatch")
    for i, variant in enumerate(("Full/test", "Lite/test", "Verified/test")):
        require(census["variants"][variant]["project_counts"] == {name: counts[i] for name, counts in ORIGINAL_COUNTS.items()}, f"Original twelve-project regression: {variant}")
    for variant in ("Live/full", "Live/verified"):
        record = census["variants"][variant]
        require(record["raw_rows"] - record["unique_tasks"] == 1, f"Live duplicate-ID disclosure mismatch: {variant}")

    date_samples = 0
    for name, row in activity.items():
        require(row["merged90"] <= row["merged365"], f"Nonmonotonic merge counts: {name}")
        for metric, date_key, minimum, sample_key in (
            ("created90", "createdAt", start, "created90_validation_sample"),
            ("merged90", "mergedAt", start, "merged90_sample"),
            ("merged365", "mergedAt", start365, "merged365_validation_sample"),
        ):
            samples = row[sample_key]
            require(isinstance(row[metric], int) and row[metric] >= 0, f"Invalid PR count: {name}")
            require(len(samples) == min(row[metric], 25 if metric == "merged90" else 1), f"PR sample cardinality mismatch: {name}/{metric}")
            require(len({item["number"] for item in samples}) == len(samples), f"Duplicate sample PR: {name}/{metric}")
            for item in samples:
                require(minimum <= item[date_key][:10] < end, f"PR date outside query window: {name}/{metric}")
                require(item["url"].startswith("https://github.com/") and "/pull/" in item["url"], f"Invalid PR sample URL: {name}")
                date_samples += 1
    for row in rest:
        require(not row["incomplete_results"], f"REST incomplete result: {row['repository']}")
        require(row["query"] == f"repo:{row['repository']} is:pr is:merged merged:{start}..{snapshot}", "REST window differs")
        require(row["REST_total_count"] == activity[row["repository"]]["merged90"], f"REST/GraphQL mismatch: {row['repository']}")
    for name, decision in manual.items():
        require(any(item["file"] == decision["source_file"] and item["ref"] == decision["source_ref"]
                    and item["url"] == decision["source_url"] and item["text"].strip()
                    for item in license_sources[name]), f"Manual license evidence missing: {name}")

    group_members = {}
    for group in source_groups:
        group_members[group["id"]] = {raw_resolution.get(raw.lower(), raw) for raw in group["members"]}
    group_details = {group["id"]: group for group in source_groups}

    def maintained(repository: dict) -> bool:
        commit = ((repository.get("defaultBranchRef") or {}).get("target") or {}).get("committedDate")
        return bool(not repository["isPrivate"] and not repository["isArchived"] and not repository["isDisabled"]
                    and commit and start <= commit[:10] < end)

    def open_license(name: str) -> bool:
        decision = manual.get(name)
        return bool(decision["open_source_accepted"] if decision else
                    (canonical[name].get("licenseInfo") or {}).get("spdxId") in SHORTLIST_OPEN_LICENSES)

    recommended = {name: row for name, row in selection["projects"].items() if row["status"] == "recommended"}
    require(len(recommended) == selection["recommended_projects"], "Recommended count mismatch")
    require(dict(Counter(row["status"] for row in selection["projects"].values())) == selection["status_counts"], "Status count mismatch")
    for name, row in selection["projects"].items():
        repository = canonical[name]
        require(row["PR_total"] == repository["allPR"]["totalCount"]
                and row["PR_merged_total"] == repository["mergedPR"]["totalCount"]
                and row["PR_open"] == repository["openPR"]["totalCount"], f"Inventory PR fields mismatch: {name}")
        if name in activity:
            require(all(row["PR_" + metric] == activity[name][metric] for metric in ("created90", "merged90", "merged365")), f"Inventory recent activity mismatch: {name}")
    peer_edges = 0
    for name, row in recommended.items():
        repository = canonical[name]
        require(maintained(repository), f"Unmaintained recommended source: {name}")
        require(row["PR_total"] == repository["allPR"]["totalCount"] >= 1000, f"Historical PR gate failed: {name}")
        require(row["PR_merged90"] == activity[name]["merged90"] >= 20, f"Recent PR gate failed: {name}")
        require(row["license_review"]["confirmed"] and row["license_review"]["open_source_accepted"]
                and open_license(name), f"License gate failed: {name}")
        require(bool(row["similar_projects"]), f"Missing similar project: {name}")
        for peer in row["similar_projects"]:
            peer_name = peer["repository"]
            require(peer_name != name and maintained(canonical[peer_name]), f"Invalid maintained peer: {name}")
            require(open_license(peer_name), f"Unconfirmed peer license: {peer_name}")
            require({name, peer_name} <= group_members[peer["group"]], f"Peer lacks functional-group membership: {name}")
            require(peer["basis"] == group_details[peer["group"]]["shared_scope"] and peer["limits"] == group_details[peer["group"]]["limits"], f"Similarity boundary mismatch: {name}")
            require(peer["in_benchmark_census"] == (peer_name in benchmark_names), f"Pool-external label mismatch: {peer_name}")
            peer_edges += 1
    table_rows = 0
    links = 0
    reports = [args.analysis / "swebench-project-selection-20261003.md", args.analysis / "swebench-project-inventory-20261003.md"]
    for report in reports:
        content = report.read_text(encoding="utf-8")
        columns = None
        for line in content.splitlines():
            if line.startswith("|"):
                width = len(re.split(r"(?<!\\)\|", line)) - 2
                if columns is None:
                    columns = width
                require(width == columns, f"Malformed Markdown table: {report.name}")
                table_rows += 1
            else:
                columns = None
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            if not target.startswith(("https://", "http://", "#")):
                path = (report.parent / target).resolve()
                require(path.exists() or path == output.resolve(), f"Broken local report link: {report.name}")
            links += 1
    inputs = sorted([path for path in args.data.glob("*.json") if path != output]
                    + list((args.analysis / "scripts").glob("*.py")) + reports)
    manifest = {str(path.relative_to(args.analysis)): hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs}
    result = {
        "schema": "swebench-project-data-audit-v1", "audited_at": datetime.now(UTC).isoformat(),
        "result": "passed", "snapshot_date": snapshot.isoformat(),
        "checks": ["census membership and canonical union", "frozen official file index",
                   "original twelve-project task counts", "Live duplicate IDs",
                   "all returned PR date samples and sample cardinalities", "independent REST count agreement",
                   "manual license source references", "recommended project and maintained peer gates",
                   "functional-group membership and pool-external labels", "Markdown table shape and local links"],
        "counts": {"datasets": len(snapshots), "variants": len(census["variants"]), "raw_identities": len(union),
                   "canonical_benchmark_projects": len(benchmark_names), "activity_projects": len(activity),
                   "PR_date_samples": date_samples, "REST_crosschecks": len(rest),
                   "manual_license_decisions": len(manual), "recommended_projects": len(recommended),
                   "recommended_peer_edges": peer_edges, "unique_official_files": len(official_files),
                   "recorded_complete_hash_files": len(hashed_files), "cached_complete_files_rehashed": len(rehashed_files),
                   "prefix_only_files": len(prefix_files), "markdown_table_rows": table_rows, "report_links": links},
        "scope_limit": "Prefix-only JSONL full contents and their task totals were not independently rehashed/recounted. Functional similarity is manually scoped; cross-project repair transfer remains untested.",
        "variant_counts": variant_counts, "input_sha256": manifest,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"result": result["result"], **result["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
