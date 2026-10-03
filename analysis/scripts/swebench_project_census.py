#!/usr/bin/env python3
"""Freeze public benchmark revisions and count their actual repository fields.

Requires duckdb==1.4.0. On WSL, PowerShell supplies Windows HTTP transport;
only public Hugging Face endpoints are contacted. Credentials are never read.
Raw task files stay in an external cache; only census/provenance enters the repo.
"""

from __future__ import annotations

import argparse
import base64
import fnmatch
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

DATASETS = {
    "Full": "SWE-bench/SWE-bench",
    "Lite": "SWE-bench/SWE-bench_Lite",
    "Verified": "SWE-bench/SWE-bench_Verified",
    "Multilingual": "SWE-bench/SWE-bench_Multilingual",
    "Multimodal": "SWE-bench/SWE-bench_Multimodal",
    "Live": "SWE-bench-Live/SWE-bench-Live",
    "Live-MultiLang": "SWE-bench-Live/MultiLang",
    "Pro": "ScaleAI/SWE-bench_Pro",
    "Multi-SWE-bench": "ByteDance-Seed/Multi-SWE-bench",
    "SWE-rebench-leaderboard": "nebius/SWE-rebench-leaderboard",
}

SPLITS = {
    "Full": {"test": "data/test-*.parquet"},
    "Lite": {"test": "data/test-*.parquet"},
    "Verified": {"test": "data/test-*.parquet"},
    "Multilingual": {"test": "data/test-*.parquet"},
    "Multimodal": {"test": "data/test-*.parquet", "dev": "data/dev-*.parquet"},
    "Live": {name: f"data/{name}-*.parquet" for name in ("full", "test", "lite", "verified")},
    "Live-MultiLang": {"all-public": "data/*.parquet"},
    "Pro": {name: f"data/{name}/test-*.parquet" for name in ("default", "hard", "v1")},
    "Multi-SWE-bench": {
        "released-7-languages": [f"{language}/*.jsonl" for language in ("c", "cpp", "go", "java", "js", "rust", "ts")],
        "kotlin-additional-files": "kotlin/*.jsonl",
        "python-additional-files": "python/*.jsonl",
    },
    "SWE-rebench-leaderboard": {"test": "data/test-*.parquet"},
}


def now() -> str:
    return datetime.now(UTC).isoformat()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def powershell(code: str, timeout: int = 120) -> str:
    prefix = (
        "$ErrorActionPreference='Stop'; $ProgressPreference='SilentlyContinue'; "
        "[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false); "
    )
    encoded = base64.b64encode((prefix + code).encode("utf-16le")).decode("ascii")
    command = [
        "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe",
        "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded,
    ]
    result = subprocess.run(command, capture_output=True, encoding="utf-8", timeout=timeout, check=False)
    if result.returncode:
        # Do not echo native error bodies, redirect URLs, or environment details.
        raise RuntimeError(f"Public HTTP request failed (exit {result.returncode})")
    return result.stdout.lstrip("\ufeff").strip()


def ps_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def public_json(url: str) -> object:
    return json.loads(powershell(
        f"Invoke-RestMethod -Uri {ps_literal(url)} -TimeoutSec 60 | ConvertTo-Json -Depth 100 -Compress"
    ))


def freeze_dataset(item: tuple[str, str]) -> tuple[str, dict]:
    label, dataset_id = item
    metadata_url = f"https://huggingface.co/api/datasets/{dataset_id}?blobs=true"
    value = public_json(metadata_url)
    result = {
        "dataset_id": dataset_id,
        "revision": value["sha"],
        "observed_at": now(),
        "last_modified": value.get("lastModified"),
        "downloads_snapshot": value.get("downloads"),
        "metadata_url": metadata_url,
        "card_data": value.get("cardData"),
        "files": value["siblings"],
    }
    print(json.dumps({"frozen": label, "revision": result["revision"]}), flush=True)
    return label, result


def download_file(job: tuple[str, dict, dict, Path]) -> tuple[tuple[str, str], dict]:
    label, dataset, metadata, cache = job
    relative = metadata["rfilename"]
    destination = cache / label / dataset["revision"] / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    expected = metadata.get("lfs", {}).get("sha256")
    url = f"https://huggingface.co/datasets/{dataset['dataset_id']}/resolve/{dataset['revision']}/{relative}"
    if relative.endswith(".jsonl") and "__" in Path(relative).name:
        # Several files contain hundreds of MB of test logs. Repository census
        # needs identity, not hidden patches/logs: verify the root identity from
        # an HTTP prefix and match it to the official, revision-pinned index.
        observation_path = Path("/tmp/arex-swebench-identity-probes") / (hashlib.sha256(url.encode()).hexdigest() + ".json")
        if observation_path.exists():
            observation = json.loads(observation_path.read_text(encoding="utf-8"))
            if observation.get("official_blob_id") == metadata["blobId"] and observation.get("source_url") == url:
                return (label, relative), observation
        prefix = powershell(
            f"$r=[System.Net.HttpWebRequest]::Create({ps_literal(url)}); "
            "$r.Timeout=45000; $r.ReadWriteTimeout=45000; $r.AddRange(0,4095); "
            "$response=$r.GetResponse(); $stream=$response.GetResponseStream(); "
            "$buffer=New-Object byte[] 4096; $n=0; "
            "while($n -lt 4096) { $got=$stream.Read($buffer,$n,4096-$n); if($got -eq 0){break}; $n+=$got }; "
            "$stream.Dispose(); $response.Dispose(); "
            "[Convert]::ToBase64String($buffer,0,$n)", timeout=60,
        )
        raw_prefix = base64.b64decode(prefix)
        identity = re.match(rb'\s*\{\s*"org"\s*:\s*"([^"\\]+)"\s*,\s*"repo"\s*:\s*"([^"\\]+)"', raw_prefix)
        if identity is None:
            raise ValueError(f"JSONL root identity missing: {relative}")
        repository = identity.group(1).decode() + "/" + identity.group(2).decode()
        expected_repository = Path(relative).stem.removesuffix("_dataset").replace("__", "/", 1)
        if repository.lower() != expected_repository.lower():
            raise ValueError(f"JSONL root and filename disagree: {relative}")
        observation = {
            "source_url": url, "bytes": metadata["size"], "repository_identity": repository,
            "integrity_verified_by": "revision_pinned_official_file_index_and_http_root_identity",
            "official_blob_id": metadata["blobId"], "official_lfs_sha256": expected,
            "prefix_bytes_observed": len(raw_prefix), "prefix_sha256": hashlib.sha256(raw_prefix).hexdigest(),
            "full_content_hash_verified": False,
            "observed_at": now(),
        }
        write_json(observation_path, observation)
        return (label, relative), observation
    existing_size_ok = destination.exists() and destination.stat().st_size == metadata["size"]
    if not existing_size_ok:
        temporary = destination.with_name(destination.name + ".download")
        windows_path = subprocess.run(
            ["wslpath", "-w", str(temporary)], check=True, capture_output=True, text=True
        ).stdout.strip()
        try:
            powershell(
                f"Invoke-WebRequest -UseBasicParsing -Uri {ps_literal(url)} "
                f"-OutFile {ps_literal(windows_path)} -TimeoutSec 35", timeout=45,
            )
        except RuntimeError:
            # A transport mirror is accepted only after matching the official
            # immutable revision's LFS digest or Git blob digest below.
            mirror_url = url.replace("https://huggingface.co/", "https://hf-mirror.com/", 1)
            result = subprocess.run([
                "/mnt/c/Windows/System32/curl.exe", "--silent", "--show-error", "--fail",
                "--location", "--max-time", "60", "--output", windows_path, mirror_url,
            ], capture_output=True, timeout=70, check=False)
            if result.returncode:
                raise RuntimeError(f"Verified mirror transport also failed: {label}/{relative}")
        temporary.replace(destination)
    data = destination.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if expected:
        if digest != expected:
            raise ValueError(f"LFS SHA-256 mismatch: {label}/{relative}")
        verification = "official_lfs_sha256"
    else:
        git_digest = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if git_digest != metadata["blobId"]:
            raise ValueError(f"Git blob mismatch: {label}/{relative}")
        verification = "official_git_blob_sha1"
    return (label, relative), {
        "path": str(destination), "source_url": url, "sha256": digest,
        "bytes": len(data), "integrity_verified_by": verification, "full_content_hash_verified": True,
    }


def repository_identity(value: object, fallback: str | None) -> str:
    if isinstance(value, dict):
        owner = value.get("owner", value.get("org"))
        name = value.get("name", value.get("repo"))
        if isinstance(owner, dict):
            owner = owner.get("login")
        value = value.get("full_name") or (f"{owner}/{name}" if owner and name else name)
    if isinstance(value, str):
        value = value.removeprefix("https://github.com/").removesuffix(".git").strip("/")
        if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
            return value
    if fallback:
        if value and str(value).lower() not in {fallback.lower(), fallback.split("/")[1].lower()}:
            raise ValueError(f"Repository identity disagrees with filename: {fallback}")
        return fallback
    raise ValueError("Unrecognized repository identity in benchmark data")


def read_identity_rows(path: Path, relative: str) -> tuple[list[tuple[str, str]], dict]:
    import duckdb

    connection = duckdb.connect(":memory:")
    reader = "read_parquet(?)" if path.suffix == ".parquet" else "read_json_auto(?, format='newline_delimited', union_by_name=true)"
    columns = {row[0]: row[1] for row in connection.execute(f"DESCRIBE SELECT * FROM {reader}", [str(path)]).fetchall()}
    repo_column = next((name for name in ("repo", "repository", "repo_name") if name in columns), None)
    id_column = next((name for name in ("instance_id", "pull_number", "number", "id") if name in columns), None)
    fallback = None
    stem = Path(relative).stem.removesuffix("_dataset")
    if "__" in stem:
        fallback = stem.replace("__", "/", 1)
    if not repo_column or not id_column:
        raise ValueError(f"Required identity columns missing in {relative}: {sorted(columns)}")
    rows = connection.execute(
        f'SELECT to_json("{repo_column}"), CAST("{id_column}" AS VARCHAR), '
        + ('CAST("org" AS VARCHAR)' if "org" in columns else 'NULL')
        + f' FROM {reader}', [str(path)]
    ).fetchall()
    selected = []
    for repository_json, task_id, organization in rows:
        repository = repository_identity(json.loads(repository_json), fallback or (
            f"{organization}/{json.loads(repository_json)}" if organization else None
        ))
        if task_id is None:
            raise ValueError(f"Missing task ID in {relative}")
        selected.append((repository, f"{repository.lower()}:{task_id}"))
    connection.close()
    return selected, {"repo_column": repo_column, "id_column": id_column, "raw_rows": len(rows)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--phase", choices=("metadata", "census"), required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    snapshot_path = args.output / "dataset-snapshots.json"
    if args.phase == "metadata":
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            datasets = dict(pool.map(freeze_dataset, DATASETS.items()))
        write_json(snapshot_path, {"schema": "swebench-dataset-snapshots-v1", "observed_at": now(), "datasets": datasets})
        return
    datasets = json.loads(snapshot_path.read_text(encoding="utf-8"))["datasets"]
    jobs = []
    chosen = {}
    for label, splits in SPLITS.items():
        dataset = datasets[label]
        for split, pattern in splits.items():
            patterns = pattern if isinstance(pattern, list) else [pattern]
            files = [file for file in dataset["files"] if any(fnmatch.fnmatch(file["rfilename"], item) for item in patterns)]
            if not files:
                raise ValueError(f"No files found for {label}/{split}")
            chosen[(label, split)] = files
            for file in files:
                job = (label, dataset, file, args.cache)
                if job not in jobs:
                    jobs.append(job)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        downloaded = {}
        for key, value in pool.map(download_file, jobs):
            downloaded[key] = value
            print(json.dumps({"verified_file": "/".join(key), "bytes": value["bytes"]}), flush=True)
    variants = {}
    projects = defaultdict(dict)
    for (label, split), files in chosen.items():
        variant = f"{label}/{split}"
        task_repository = {}
        file_reports = []
        raw_rows = 0
        membership_only = {}
        for metadata in files:
            relative = metadata["rfilename"]
            provenance = downloaded[(label, relative)]
            if "repository_identity" in provenance:
                membership_only[provenance["repository_identity"]] = None
                file_reports.append({"file": relative, **provenance})
                continue
            rows, extraction = read_identity_rows(Path(provenance["path"]), relative)
            raw_rows += len(rows)
            for repository, task_id in rows:
                if task_id in task_repository and task_repository[task_id] != repository:
                    raise ValueError(f"Conflicting task repository: {variant}")
                task_repository[task_id] = repository
            file_reports.append({"file": relative, **{key: value for key, value in provenance.items() if key != "path"}, **extraction})
        counts = dict(Counter(task_repository.values()))
        counts.update(membership_only)
        variants[variant] = {
            "dataset_id": datasets[label]["dataset_id"], "revision": datasets[label]["revision"],
            "raw_rows": None if membership_only else raw_rows,
            "unique_tasks": None if membership_only else len(task_repository), "repositories": len(counts),
            "project_counts": dict(sorted(counts.items())), "files": file_reports,
            "identity_set_sha256": None if membership_only else hashlib.sha256("\n".join(sorted(task_repository)).encode()).hexdigest(),
            "task_counts_not_computed": bool(membership_only),
        }
        for repository, count in counts.items():
            projects[repository][variant] = count
        print(json.dumps({"variant": variant, "tasks": variants[variant]["unique_tasks"], "repositories": len(counts)}), flush=True)
    write_json(args.output / "benchmark-project-census.json", {
        "schema": "swebench-project-census-v1", "observed_at": now(),
        "variants": variants, "unique_raw_repositories": len(projects),
        "projects": dict(sorted(projects.items())),
        "scope": "Published evaluation splits and public Multi-SWE-bench files; no training corpus or private Pro projects.",
    })


if __name__ == "__main__":
    main()
