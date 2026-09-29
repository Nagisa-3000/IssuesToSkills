#!/usr/bin/env python3
"""Validate universal problem classes, split hygiene, and issue manifest shape."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASSES = ROOT / "experiments" / "manifests" / "universal-problem-classes-v1.json"
DEFAULT_SEEDS = ROOT / "experiments" / "manifests" / "universal-issue-seeds-v1.json"
DEFAULT_MANIFEST = ROOT / "experiments" / "manifests" / "universal-issue-manifest-v1.json"


def validate(classes_path: Path, seeds_path: Path, manifest_path: Path) -> dict[str, object]:
    class_doc = json.loads(classes_path.read_text(encoding="utf-8"))
    seed_doc = json.loads(seeds_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    classes = {str(item["id"]): item for item in class_doc["classes"]}
    repositories = [str(item) for item in seed_doc["repositories"]]
    cases = list(manifest["cases"])
    errors: list[str] = []
    warnings: list[str] = []
    if len(classes) != 10:
        errors.append(f"expected 10 universal classes, got {len(classes)}")
    if len(repositories) != 6:
        errors.append(f"expected 6 repositories, got {len(repositories)}")
    if "deepseek-ai/deepseek-harness" in repositories:
        errors.append("DeepSeek Harness must not be in the six-harness study")
    keys: set[tuple[str, int]] = set()
    buckets: dict[tuple[str, str], set[str]] = defaultdict(set)
    split_keys: dict[str, set[tuple[str, int]]] = {"train_candidate": set(), "holdout_candidate": set()}
    for case in cases:
        repo = str(case.get("repository", ""))
        issue = int(case.get("issue", 0))
        category = str(case.get("category", ""))
        role = str(case.get("role", ""))
        key = (repo, issue)
        if key in keys:
            errors.append(f"duplicate issue key: {repo}#{issue}")
        keys.add(key)
        if repo not in repositories:
            errors.append(f"case repository outside scope: {repo}")
        if category not in classes:
            errors.append(f"unknown category: {category}")
        if role not in split_keys:
            errors.append(f"unknown role: {role}")
        else:
            split_keys[role].add(key)
        buckets[(repo, category)].add(role)
        state = str((case.get("verification") or {}).get("issue_state", "unverified"))
        if state == "open":
            errors.append(f"open issue in candidate manifest: {repo}#{issue}")
        if state == "unverified":
            warnings.append(f"state not fetched yet: {repo}#{issue}")
    overlap = split_keys["train_candidate"] & split_keys["holdout_candidate"]
    if overlap:
        errors.append(f"train/holdout issue leakage: {sorted(overlap)[:5]}")
    expected = {(repo, category) for repo in repositories for category in classes}
    if set(buckets) != expected:
        errors.append(f"repository/category bucket mismatch: missing={sorted(expected-set(buckets))[:5]}")
    incomplete = {key: roles for key, roles in buckets.items() if roles != {"train_candidate", "holdout_candidate"}}
    if incomplete:
        errors.append(f"incomplete train/holdout buckets: {list(incomplete.items())[:5]}")
    for category, value in classes.items():
        workflow = value.get("workflow") or []
        if not workflow or any(not isinstance(step, str) for step in workflow):
            errors.append(f"class {category} has no generic workflow steps")
        if not value.get("genericity"):
            errors.append(f"class {category} has no genericity statement")
    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "case_count": len(cases),
        "repository_counts": dict(Counter(str(case["repository"]) for case in cases)),
        "category_counts": dict(Counter(str(case["category"]) for case in cases)),
        "train_candidates": len(split_keys["train_candidate"]),
        "holdout_candidates": len(split_keys["holdout_candidate"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classes", type=Path, default=DEFAULT_CLASSES)
    parser.add_argument("--seeds", type=Path, default=DEFAULT_SEEDS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    report = validate(args.classes, args.seeds, args.manifest)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
